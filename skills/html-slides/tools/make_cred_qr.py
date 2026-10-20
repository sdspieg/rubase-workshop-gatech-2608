#!/usr/bin/env python3
"""Build a QR for a site with HTTP Basic credentials baked into the URL.

    python3 tools/make_cred_qr.py --host example.org --user USER --out img/qr_site.png

The password is read from an environment variable (--pw-env, default SITE_PW) or
prompted for interactively. It is NEVER passed on the command line, because argv
lands in shell history, in process listings, and in this session's transcript.

Verification decodes the finished PNG and compares it to the intended URL, then
reports MATCH / MISMATCH. It never prints the URL or the password.

Two things to know before using this at all:
  * It only works where the site answers with HTTP Basic auth (a 401 carrying a
    WWW-Authenticate header). Against a login FORM the credentials in the URL are
    simply ignored, and the QR takes the scanner to a login page.
  * The password is recoverable from the image by anyone who photographs it. A QR
    on a projector is a permanent, silent credential leak.
"""
import argparse, getpass, os, sys, urllib.parse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', required=True, help='host only, no scheme')
    ap.add_argument('--user', required=True)
    ap.add_argument('--path', default='/')
    ap.add_argument('--out', required=True)
    ap.add_argument('--pw-env', default='SITE_PW', help='env var holding the password')
    a = ap.parse_args()

    pw = os.environ.get(a.pw_env) or getpass.getpass(f'password for {a.user}@{a.host}: ')
    if not pw:
        sys.exit('no password given')

    # percent-encode both halves: an @ or : in either one silently breaks the URL
    url = 'https://{}:{}@{}{}'.format(
        urllib.parse.quote(a.user, safe=''), urllib.parse.quote(pw, safe=''),
        a.host, a.path)

    import qrcode
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=14, border=3)
    q.add_data(url)
    q.make(fit=True)
    q.make_image(fill_color='black', back_color='white').save(a.out)

    try:
        import cv2
        got, _, _ = cv2.QRCodeDetector().detectAndDecode(cv2.imread(a.out))
        print('decode check:', 'MATCH' if got == url else 'MISMATCH')
    except ImportError:
        print('decode check: SKIPPED (opencv missing) - do not trust this QR unscanned')

    print(f'wrote {a.out} ({os.path.getsize(a.out)} bytes), '
          f'{len(url)} chars encoded, QR version {q.version}')
    print('NOTE: the password is inside this image. Anyone who photographs it has the login.')


if __name__ == '__main__':
    main()
