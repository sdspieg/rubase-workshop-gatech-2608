"""Build sarah.html - the standalone 75-minute guest lecture for Sarah Bidgood's
INTA 4803/8803 open-source-intelligence class, Wed 2 Sep 15:30-16:45, Skiles 254.

Cut FROM deck.html so the CSS, the obuild machinery, autofit, the notes and every
gate apply unchanged. Slides are copied verbatim by data-sid; only the DAYS array,
the welcome screen and the title are rewritten, plus two new slides for her room.
"""
import re, pathlib, sys

HOST = "rubase.org"
PAPER = "red-lines paper"
DECK = pathlib.Path("deck.html")
OUT = pathlib.Path("sarah.html")

ORDER = [
    "NEW_TITLE",
    "592826",   # Flashback in time - RAND/UCLA, expertise built and then lost
    "0cae47",   # Russia is back. We are not.
    "d385e0",   # What this has actually produced - incl. the paper they read
    "1f47ad",   # The scholarly record on your topic - guess the number
    "1d4b51",   # How search is typically done today
    "10f148",   # Precision and recall
    "e18c1e",   # Broad versus narrow
    "256149",   # McNamara's first law
    "84f368",   # Where to get the data
    "17306f",   # Three places to ask - and they do not agree
    "lensq1",   # HANDS-ON 1: run your own query, three services
    "0734c8",   # An epistemic MRI - the deterrence literature
    "9ce288",   # Slicing and dicing - and what is missing
    "a7f3c2",   # One object, and the cuts you make in it
    "b6d914",   # But real topics are not tidy cubes
    "4b7fb0",   # What are ontologies and taxonomies?
    "mdtq01",   # HANDS-ON 2: build one for your own topic
    "48a61f",   # The murderboard
    "e631a8",   # Now measure whether it worked
    "4e7a9c",   # What your instrument cannot see
    "NEW_CLOSE",
]

TITLE = (
 '<section class="slide" data-t="Title" data-sid="sar001" '
 'data-n="&lt;b&gt;Skiles 254, 15:30&ndash;16:45.&lt;/b&gt; Meet Sarah at Habersham '
 'around 15:00.&lt;ul&gt;'
 '&lt;li&gt;They have read the ' + PAPER + ' and have ' + HOST + ' access '
 '(GT-RuBase) through 6 December.&lt;/li&gt;'
 '&lt;li&gt;&lt;b&gt;Two hands-on stops&lt;/b&gt; &ndash; the query slide and the '
 'taxonomy prompt. Both need laptops open; say so at the start so nobody has one '
 'shut.&lt;/li&gt;'
 '&lt;li&gt;This is an OSINT course, early semester. The through-line is: open '
 'source is not a place you look, it is an instrument you build and then '
 'measure.&lt;/li&gt;'
 '&lt;li&gt;Invite them to the workshop &ndash; 11:00&ndash;13:30 daily through '
 'Friday, lunch provided.&lt;/li&gt;&lt;/ul&gt;">'
 '<h2>Open source, at the scale it actually exists</h2>'
 '<p class="sub">Building an instrument for a literature you cannot read '
 '&middot; and being honest about what it misses</p>'
 '<div class="sar-hero"><div class="sar-title">'
 '<div class="sar-row"><span class="sar-k">Class</span>'
 '<span class="sar-v">INTA 4803 / 8803 &middot; Open Source Intelligence</span></div>'
 '<div class="sar-row"><span class="sar-k">Guest</span>'
 '<span class="sar-v">Stephan De Spiegeleire &middot; HCSS</span></div>'
 '<div class="sar-row"><span class="sar-k">You read</span>'
 '<span class="sar-v">the ' + PAPER + ' &middot; this hour is the machinery '
 'behind it</span></div>'
 '<div class="sar-row"><span class="sar-k">Bring</span>'
 '<span class="sar-v">a laptop, and a topic you actually care about</span></div>'
 '</div>'
 '<div class="sar-qr"><img src="img/qr_dashboard.png" alt="">'
 '<div class="sar-qrc">log in now &middot; <b>GT-RuBase</b><br>'
 'you will need it in ten minutes</div></div>'
 '</div></section>')

CLOSE = (
 '<section class="slide" data-t="What to take" data-sid="sar999" '
 'data-n="&lt;b&gt;Close and hand over.&lt;/b&gt;&lt;ul&gt;'
 '&lt;li&gt;The credentials run through 6 December &ndash; long enough to use RuBase '
 'for a term paper, which is the point of giving them.&lt;/li&gt;'
 '&lt;li&gt;End on the recall line, not on the tooling. The one thing an OSINT '
 'student should leave with is that the number you cannot see is the one that '
 'decides whether the finding is real.&lt;/li&gt;'
 '&lt;li&gt;Workshop: 11:00&ndash;13:30 daily, Nunn Conference Room, through Friday, '
 'lunch provided. Thursday is the measurement day and the most relevant to '
 'them.&lt;/li&gt;&lt;/ul&gt;">'
 '<h2>Four things to take out of this room</h2>'
 '<p class="sub">None of them needs our infrastructure, and all four survive the '
 'next change of tools</p>'
 '<div class="sar-take">'
 '<div class="sar-item"><div class="sar-n">1</div><div class="sar-b">'
 '<b>Ask what your query could not have returned.</b> Precision you can see by '
 'reading your own hits. Recall you cannot see at all &ndash; and it is the number '
 'that decides whether a finding is real or an artifact of your search string.'
 '</div></div>'
 '<div class="sar-item"><div class="sar-n">2</div><div class="sar-b">'
 '<b>Ask three sources, not one.</b> The same question put to three free databases '
 'returns three different literatures. Where they disagree is information, not '
 'noise.</div></div>'
 '<div class="sar-item"><div class="sar-n">3</div><div class="sar-b">'
 '<b>Write the instrument down before you use it.</b> A scheme you can hand to '
 'someone else is the difference between a finding and an impression, and it is '
 'what makes disagreement productive instead of personal.</div></div>'
 '<div class="sar-item"><div class="sar-n">4</div><div class="sar-b">'
 '<b>Report the number that embarrasses you.</b> Agreement corrected for chance, the '
 'cases the scheme could not hold, the cell with nothing in it. That paragraph is '
 'what makes the rest of the paper believable.</div></div>'
 '</div>'
 '<p class="sar-foot">' + HOST + ' &middot; login <b>GT-RuBase</b> &middot; access '
 'through 6&nbsp;December &middot; the workshop runs 11:00&ndash;13:30 daily in the '
 'Nunn Conference Room, lunch provided</p>'
 '</section>')

CSS = """
/* ---- sarah.html only: the two slides written for this class ---- */
.sar-hero{margin-top:2.4cqh;display:flex;align-items:center;gap:4cqw}
.sar-title{flex:1 1 auto;display:flex;flex-direction:column;gap:1.15cqh}
.sar-row{display:flex;align-items:baseline;gap:1.4cqw}
.sar-k{flex:0 0 12cqw;text-align:right;color:var(--gold);font-weight:700;
  font-size:1.62cqw;letter-spacing:.10em;text-transform:uppercase}
.sar-v{color:var(--wh);font-size:1.92cqw;line-height:1.3}
.sar-take{margin-top:1.6cqh;display:flex;flex-direction:column;gap:1.1cqh}
.sar-item{display:flex;gap:1.5cqw;align-items:flex-start;
  background:rgba(19,47,89,.5);border-left:3px solid var(--gold);
  border-radius:var(--r);padding:.85cqh 1.4cqw}
.sar-n{flex:0 0 auto;color:var(--gold);font-weight:700;font-size:2.4cqw;
  line-height:1;min-width:2.1cqw}
.sar-b{color:var(--wh);font-size:1.50cqw;line-height:1.40}
.sar-b b{color:#ffd98a}
.sar-foot{margin-top:1.5cqh;color:var(--lb);font-size:1.30cqw;line-height:1.4}
.sar-foot b{color:var(--gold)}
.sar-qr{flex:0 0 auto;text-align:center}
.sar-qr img{width:19cqw;height:auto;display:block;background:#fff;padding:1cqw;border-radius:var(--r)}
.sar-qrc{margin-top:.9cqh;color:var(--lb);font-size:1.28cqw;line-height:1.35}
.sar-qrc b{color:var(--gold)}
"""

DAYS = """var DAYS=[
 {n:1,label:"Part 1",title:"The problem",when:"15:30",time:"~20 min",
  desc:"A literature nobody can read, and the search habits we still use on it.",
  items:["What was built, and lost","How much is out there","How we search now","Precision and recall"]},
 {n:2,label:"Part 2",title:"Where to look",when:"15:50",time:"~20 min",
  desc:"Three free databases, three different answers &ndash; and your own query, live.",
  items:["Where to get the data","Three places to ask","Run your own","An epistemic MRI"]},
 {n:3,label:"Part 3",title:"The instrument",when:"16:10",time:"~22 min",
  desc:"Cutting a topic into positions you can count, and arguing about the cuts.",
  items:["One object, many cuts","Not tidy cubes","Ontologies and taxonomies","Build one, then murderboard it"]},
 {n:4,label:"Part 4",title:"Honesty",when:"16:32",time:"~13 min",
  desc:"Measuring whether it worked, and naming what the instrument cannot see.",
  items:["Measure it","What your instrument cannot see","Four things to take"]}
];"""


def main():
    h = DECK.read_text(encoding="utf-8")
    secs = {}
    for m in re.finditer(r'<section class="slide[^"]*"[^>]*data-sid="([^"]+)".*?</section>',
                         h, re.S):
        secs[m.group(1)] = m.group(0)
    missing = [s for s in ORDER if s not in secs and not s.startswith("NEW_")]
    if missing:
        sys.exit("missing sids: " + ", ".join(missing))

    first = h.index('<section class="slide')
    last = h.rindex("</section>") + len("</section>")
    head, tail = h[:first], h[last:]
    body = [TITLE if s == "NEW_TITLE" else CLOSE if s == "NEW_CLOSE" else secs[s]
            for s in ORDER]

    old = re.search(r"var DAYS=\[.*?\];", tail, re.S)
    assert old, "DAYS array not found"
    tail = tail[:old.start()] + DAYS + tail[old.end():]

    head = head.replace("<title>Out of the Dark Ages? &middot; slides</title>",
                        "<title>Open source, at the scale it actually exists "
                        "&middot; INTA 4803/8803</title>")
    head = head.replace('content="RuBase / StratBase Methods Workshop, Georgia Tech, '
                        '31 August to 4 September 2026."',
                        'content="Guest lecture for INTA 4803/8803 Open Source '
                        'Intelligence, Sam Nunn School, 2 September 2026."')
    anchor = "/* ---- FROM DARKNESS TO LIGHT"
    head = head[:head.index(anchor)] + CSS + head[head.index(anchor):]

    # exact literals: the earlier regex assumed a concatenation that is not there
    tail = tail.replace("Out of the Dark Ages? Your help is needed!",
                        "Open source, at the scale it actually exists")
    tail = tail.replace(
        "Supercharging your research workflow with LLMs. Five lunchtime sessions "
        "&ndash; lunch provided. We take one research pipeline apart&nbsp;&ndash; "
        "from the question, through the corpus and the instrument, to a result you "
        "can defend&nbsp;&ndash; and put it back together with tools that did not "
        "exist when most of our methods were written.",
        "Guest lecture for INTA 4803/8803. Open source is not a place you look "
        "&ndash; it is an instrument you build, point at a literature far too large "
        "to read, and then measure honestly. Four movements, two of them with your "
        "laptop open.")
    tail = tail.replace(
        "Sam Nunn School of International Affairs &#183; 31 August &ndash; "
        "4 September 2026 &#183; 11:00&ndash;13:30 daily &#183; Nunn Conference Room",
        "Sam Nunn School of International Affairs &#183; Skiles 254 &#183; "
        "Wednesday 2 September 2026 &#183; 15:30&ndash;16:45")
    head = head.replace(
        'Out of the Dark Ages?&nbsp;&ndash; <span>slides for the Georgia Tech '
        'edition</span>',
        'Open source, at the scale it actually exists&nbsp;&ndash; '
        '<span>INTA 4803/8803, 2 September 2026</span>')

    OUT.write_text(head + "".join(body) + tail, encoding="utf-8")
    print("sarah.html: %d slides, %d KB" % (len(ORDER), OUT.stat().st_size // 1024))


main()
