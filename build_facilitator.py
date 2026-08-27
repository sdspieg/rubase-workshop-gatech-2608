# -*- coding: utf-8 -*-
"""The facilitator half of the app, on its own page.

The site proper is for STUDENTS (SDS, 2026-08-27). Design rationale, what to cut
when the room runs late, and the edition lineage are all useful - to whoever is
running the week, not to whoever is attending it. So they live here, and nothing
in the student site links to this page."""
import re, sys
sys.path.insert(0, ".")
import build_site as B
from data import DAYS, DECK

def page():
    body = [B.programme(), B.design(), B.facilitator(), B.editions()]
    # re-key the first block so the page opens on the facilitator kit
    body = [b.replace('class="block-content"', 'class="block-content active"', 1)
            if 'id="block-facilitator"' in b else b for b in body]
    nav = ('<button onclick="showBlock(\'facilitator\')">Facilitator kit</button>'
           '<button onclick="showBlock(\'programme\')">Programme</button>'
           '<button onclick="showBlock(\'design\')">Design decisions</button>'
           '<button onclick="showBlock(\'editions\')">All editions</button>'
           f'<a href="{DECK}">Slides</a>'
           '<a href="index.html">Student site &#8599;</a>'
           '<select onchange="goEdition(this.value)" aria-label="Workshop edition">'
           '<option value="facilitator.html" selected>Edition: GaTech 5 &times; 2.5&#8239;h</option>'
           '<option value="https://sdspieg.github.io/rubase-workshop-5day/">Edition: 5-day full</option>'
           '<option value="https://sdspieg.github.io/rubase-workshop/">Edition: 3-day</option>'
           '</select>')
    side = ('<div class="sidebar-section"><div class="sidebar-section-title">Running the week</div>'
      '<div class="sidebar-item" data-block="facilitator" onclick="showBlock(\'facilitator\')">'
      '<span class="sidebar-item-title">Facilitator kit</span><span class="sidebar-badge">Run</span></div>'
      '<div class="sidebar-item" data-block="programme" onclick="showBlock(\'programme\')">'
      '<span class="sidebar-item-title">Programme</span><span class="sidebar-badge badge-time">12.5 h</span></div>'
      '<div class="sidebar-item" data-block="design" onclick="showBlock(\'design\')">'
      '<span class="sidebar-item-title">Design decisions</span><span class="sidebar-badge badge-time">why</span></div>'
      '<div class="sidebar-item" data-block="editions" onclick="showBlock(\'editions\')">'
      '<span class="sidebar-item-title">All editions</span><span class="sidebar-badge">4</span></div>'
      '</div><div class="sidebar-section"><div class="sidebar-section-title">The days</div>'
      + ''.join(f'<a class="sidebar-item" href="index.html#{d["id"]}">'
                f'<span class="sidebar-item-title">{d["n"]} &middot; {d["name"]}</span>'
                f'<span class="sidebar-badge badge-external">&#8599;</span></a>' for d in DAYS)
      + '</div><div class="sidebar-section"><div class="sidebar-section-title">Records</div>'
      '<a class="sidebar-item" href="https://drive.google.com/file/d/128iNBS792NqV2bH0sE_Q6q5auo2xA22F/view?usp=drivesdk" '
      'target="_blank" rel="noopener"><span class="sidebar-item-title">Five-day run sheets</span>'
      '<span class="sidebar-badge badge-external">&#8599;</span></a>'
      '<a class="sidebar-item" href="https://drive.google.com/file/d/1a-BRA2-Z8d5KEL7_LCvx7H6ROe2CNHwf/view?usp=drivesdk" '
      'target="_blank" rel="noopener"><span class="sidebar-item-title">The 2.5-hour redesign</span>'
      '<span class="sidebar-badge badge-external">&#8599;</span></a></div>')

    head = (B.HEAD.replace("__TIMELINE__", B.timeline())
                  .replace("__SIDEBAR__", side)
                  .replace("__DECK__", DECK)
                  .replace("<title>RuBase Methods Workshop &middot; Georgia Tech</title>",
                           "<title>Facilitator kit &middot; Georgia Tech</title>")
                  .replace("RuBase / StratBase Methods Workshop &ndash; <span>Georgia Tech, "
                           "31 August &ndash; 4 September 2026</span>",
                           "Facilitator kit &ndash; <span>Georgia Tech, 31 August &ndash; "
                           "4 September 2026</span>"))
    # swap the student nav for the facilitator one
    head = re.sub(r'<button onclick="showHome\(\)">Home</button>.*?</nav>', nav + '</nav>', head, flags=re.S)
    tail = B.TAIL.replace("""      RuBase / StratBase Methods Workshop &middot; Georgia Tech edition &middot;
      Stephan De Spiegeleire, The Hague Centre for Strategic Studies &middot;
      Sam Nunn School of International Affairs, 31 August &ndash; 4 September 2026.""",
      """      Facilitator kit &middot; not linked from the student site.""")
    # showHome() has no home screen here; send it to the kit instead
    tail = tail.replace("document.getElementById('homeScreen').classList.add('active');",
                        "var f=document.getElementById('block-facilitator'); if(f)f.classList.add('active');")
    html = head + "\n".join(body) + tail
    parts = re.split(r'(<[^>]*>)', html)
    for i in range(0, len(parts), 2):
        parts[i] = parts[i].replace(" - ", "&nbsp;&ndash; ")
    html = "".join(parts)
    open("facilitator.html", "w", encoding="utf-8").write(html)
    print("wrote facilitator.html", len(html), "bytes | views:", html.count('class="block-content'))
    print("  non-ascii:", sum(1 for c in html if ord(c) > 127), "| em-dashes:", html.count(chr(8212)))

page()
