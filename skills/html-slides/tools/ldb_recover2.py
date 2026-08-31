#!/usr/bin/env python3
"""Second pass: recover EVERY version of the review comments, from every origin.

The first pass had three holes, and each could hide comments:
  * it kept only the single largest recovered array, so an older or a
    differently-scoped snapshot holding comments the biggest one lacks was thrown away;
  * it never parsed the write-ahead .log, which is exactly where the MOST RECENT
    writes live before compaction;
  * it did not separate origins, so comments made against the github.io site and
    against 127.0.0.1 were indistinguishable.
This pass unions every array it can parse, from .ldb tables AND .log files, and
reports which origin and which file each came from.
"""
import glob, json, os, struct, sys

MAGIC = 0xdb4775248b80fb57


def uncompress(src):
    n = shift = p = 0
    while True:
        c = src[p]; p += 1
        n |= (c & 0x7f) << shift; shift += 7
        if not (c & 0x80): break
        if shift > 32: raise ValueError('preamble')
    out = bytearray()
    while p < len(src):
        tag = src[p]; p += 1
        t = tag & 3
        if t == 0:
            ln = tag >> 2
            if ln >= 60:
                extra = ln - 59
                ln = int.from_bytes(src[p:p + extra], 'little'); p += extra
            ln += 1
            out += src[p:p + ln]; p += ln
        else:
            if t == 1:
                ln = 4 + ((tag >> 2) & 7); off = ((tag >> 5) << 8) | src[p]; p += 1
            elif t == 2:
                ln = (tag >> 2) + 1; off = int.from_bytes(src[p:p + 2], 'little'); p += 2
            else:
                ln = (tag >> 2) + 1; off = int.from_bytes(src[p:p + 4], 'little'); p += 4
            if off == 0 or off > len(out): raise ValueError('offset')
            for _ in range(ln): out.append(out[-off])
    if len(out) != n: raise ValueError('length')
    return bytes(out)


def varint(b, p):
    r = shift = 0
    while True:
        c = b[p]; p += 1
        r |= (c & 0x7f) << shift
        if not (c & 0x80): return r, p
        shift += 7


def read_block(f, off, size):
    f.seek(off); raw = f.read(size + 5)
    return uncompress(raw[:size]) if raw[size] == 1 else raw[:size]


def block_entries(blk):
    if len(blk) < 4: return
    nres = struct.unpack('<I', blk[-4:])[0]
    end = len(blk) - 4 - 4 * nres
    p, prev = 0, b''
    while p < end:
        sh, p = varint(blk, p); ns, p = varint(blk, p); vl, p = varint(blk, p)
        key = prev[:sh] + blk[p:p + ns]; p += ns
        val = blk[p:p + vl]; p += vl
        prev = key
        yield key, val


def sst_pairs(path):
    with open(path, 'rb') as f:
        f.seek(0, 2); size = f.tell()
        if size < 48: return
        f.seek(size - 48); footer = f.read(48)
        if struct.unpack('<Q', footer[40:48])[0] != MAGIC: return
        p = 0
        _, p = varint(footer, p); _, p = varint(footer, p)
        ioff, p = varint(footer, p); isize, p = varint(footer, p)
        for _, handle in block_entries(read_block(f, ioff, isize)):
            q = 0; off, q = varint(handle, q); sz, q = varint(handle, q)
            try: blk = read_block(f, off, sz)
            except Exception: continue
            yield from block_entries(blk)


def wal_pairs(path):
    """LevelDB write-ahead log: 32KB blocks, 7-byte record headers, then batches."""
    data = open(path, 'rb').read()
    payload, p = bytearray(), 0
    while p + 7 <= len(data):
        if p % 32768 > 32768 - 7:
            p += 32768 - (p % 32768); continue
        ln = struct.unpack('<H', data[p + 4:p + 6])[0]
        typ = data[p + 6]; p += 7
        if ln == 0 and typ == 0:
            p += 32768 - (p % 32768) if p % 32768 else 0
            continue
        payload += data[p:p + ln]; p += ln
    b, q = bytes(payload), 0
    while q + 12 <= len(b):
        count = struct.unpack('<I', b[q + 8:q + 12])[0]; q += 12
        for _ in range(count):
            if q >= len(b): return
            t = b[q]; q += 1
            kl, q = varint(b, q); key = b[q:q + kl]; q += kl
            if t == 1:
                vl, q = varint(b, q); val = b[q:q + vl]; q += vl
            else:
                val = b''
            yield key, val


def as_text(v):
    if not v: return ''
    if v[0] == 0: return v[1:].decode('utf-16-le', 'ignore')
    if v[0] == 1: return v[1:].decode('latin-1', 'ignore')
    return v.decode('utf-8', 'ignore')


def main(dirs, outpath):
    union, seen_sources = {}, []
    for d in dirs:
        for path in sorted(glob.glob(os.path.join(d, '*'))):
            base = os.path.basename(path)
            if not (base.endswith('.ldb') or base.endswith('.log')): continue
            gen = wal_pairs if base.endswith('.log') else sst_pairs
            try: pairs = list(gen(path))
            except Exception: continue
            for k, v in pairs:
                kt = k.decode('latin-1', 'ignore')
                if 'gtreview' not in kt: continue
                origin = kt.split('\x00')[0].lstrip('_') or '(unknown)'
                txt = as_text(v)
                if '[' not in txt: continue
                try: items = json.loads(txt[txt.index('['):txt.rindex(']') + 1])
                except Exception: continue
                if not isinstance(items, list) or not items: continue
                seen_sources.append((base, origin, len(items)))
                for c in items:
                    if not isinstance(c, dict): continue
                    i = c.get('id') or (str(c.get('ts')) + str(c.get('comment'))[:40])
                    if i not in union or str(c.get('ts', '')) >= str(union[i].get('ts', '')):
                        union[i] = c
    for s in seen_sources:
        print(f'  snapshot: {s[0]:16s} origin={s[1]:38s} {s[2]} comments')
    out = sorted(union.values(), key=lambda c: str(c.get('ts', '')))
    print(f'\nUNION across every snapshot: {len(out)} distinct comments')
    if out:
        json.dump({'items': out}, open(outpath, 'w'), ensure_ascii=False, indent=1)
        print('wrote', outpath, '| latest', out[-1].get('ts'))


if __name__ == '__main__':
    main(sys.argv[1:-1], sys.argv[-1])
