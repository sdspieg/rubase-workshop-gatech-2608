(function(){
  var style = document.createElement('style');
  style.textContent = '.slide.has-prompt-qr h2,.slide.has-prompt-qr>.sub{max-width:82%}' +
    '.slide.has-prompt-qr>.sub{font-size:1.35cqw}' +
    '.prompt-qr-card{position:absolute;z-index:18;top:1.25%;right:1.6%;width:11.5%;padding:.45%;background:#fff;border:2px solid var(--gold);border-radius:.45cqw;text-decoration:none;box-shadow:0 .35cqw 1.2cqw rgba(0,0,0,.28);line-height:1}' +
    '.prompt-qr-card img{display:block;width:100%;height:auto;image-rendering:pixelated}' +
    '.prompt-qr-card span{display:block;padding:.38cqw .15cqw .1cqw;color:#09182f;font:700 1.22cqw/1.1 "Titillium Web",system-ui,sans-serif;text-align:center;letter-spacing:.03em}' +
    '.prompt-qr-card:hover{transform:translateY(-.12cqw);box-shadow:0 .5cqw 1.4cqw rgba(0,0,0,.36)}';
  document.head.appendChild(style);

  var prompts = [
    {
      sid: '2f0173',
      title: 'The taxonomic classification prompt',
      url: 'resources/taxonomy_classification_prompt.md',
      qr: 'img/qr_taxonomy_classification_prompt.png',
      label: 'SCAN · CLASSIFY'
    },
    {
      sid: '994544',
      title: 'The report-writing prompt',
      url: 'resources/report_writing_prompt.md',
      qr: 'img/qr_report_writing_prompt.png',
      label: 'SCAN · WRITE'
    }
  ];

  prompts.forEach(function(p){
    var slide = document.querySelector('section.slide[data-sid="' + p.sid + '"]');
    if(!slide) return;
    slide.dataset.t = p.title.replace(/^The /, '');
    var heading = slide.querySelector('h2');
    if(heading) heading.textContent = p.title;
    slide.classList.add('has-prompt-qr');
    var link = document.createElement('a');
    link.className = 'prompt-qr-card';
    link.dataset.frag = '1';
    link.href = p.url;
    link.target = '_blank';
    link.rel = 'noopener';
    link.setAttribute('aria-label', 'Open the full prompt');
    link.innerHTML = '<img src="' + p.qr + '" alt="QR code linking to the full prompt">' +
      '<span>' + p.label + '</span>';
    slide.appendChild(link);
  });

  var swot = document.querySelector('section.slide[data-sid="09b478"]');
  if(swot){
    swot.dataset.t = 'A SWOT-style analysis of Russian regeneration potential';
    swot.dataset.n = 'This is condensed from the regeneration report, pp. 122-124. Reveal one quadrant at a time. The earlier version wrongly left opportunities and threats empty; the report contains a full four-quadrant analysis.';
    swot.innerHTML = `<h2>A SWOT-style analysis of Russian regeneration potential</h2>
      <p class="sub">Condensed from the report, pp. 122&ndash;124 &ndash; every quadrant is grounded in the written analysis.</p>
      <div class="ob-pic"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1770 750" role="img" aria-label="A complete SWOT grid drawn from the regeneration report. Each of the four quadrants contains three report-grounded findings.">
        <style>.sw-ax{font:700 24px system-ui,sans-serif;fill:#6f8bab;letter-spacing:.2em}.sw-qh{font:700 26px system-ui,sans-serif;letter-spacing:.14em}.sw-it{font:700 22px system-ui,sans-serif;fill:#f3f6fb}</style>
        <rect width="1770" height="750" fill="#09182f"/><rect x="196" y="70" width="1542" height="435" rx="8" fill="#0d1e39" stroke="#3c5a86" stroke-width="2.4"/>
        <line x1="967" y1="70" x2="967" y2="505" stroke="#3c5a86" stroke-width="2.4"/><line x1="196" y1="292" x2="1738" y2="292" stroke="#3c5a86" stroke-width="2.4"/>
        <text x="582" y="50" class="sw-ax" text-anchor="middle">HELPFUL</text><text x="1352" y="50" class="sw-ax" text-anchor="middle">HARMFUL</text>
        <text x="164" y="181" class="sw-ax" text-anchor="middle" transform="rotate(-90 164 181)">INTERNAL</text><text x="164" y="398" class="sw-ax" text-anchor="middle" transform="rotate(-90 164 398)">EXTERNAL</text>
        <text x="218" y="108" class="sw-qh" fill="#dbad50">STRENGTHS</text><text x="989" y="108" class="sw-qh" fill="#e2915f">WEAKNESSES</text>
        <text x="218" y="330" class="sw-qh" fill="#70a9d7">OPPORTUNITIES FOR NATO</text><text x="989" y="330" class="sw-qh" fill="#e2915f">THREATS</text>
        <g class="sw-lg sw-lg1"><rect x="216" y="122" width="731" height="50" rx="6" fill="#16294a" stroke="#dbad50" stroke-width="1.8"/><rect x="216" y="122" width="6" height="50" fill="#dbad50"/><text x="242" y="155" class="sw-it">Scalable manpower generation</text><rect x="216" y="178" width="731" height="50" rx="6" fill="#16294a" stroke="#dbad50" stroke-width="1.8"/><rect x="216" y="178" width="6" height="50" fill="#dbad50"/><text x="242" y="211" class="sw-it">Wartime industrial continuity</text><rect x="216" y="234" width="731" height="50" rx="6" fill="#16294a" stroke="#dbad50" stroke-width="1.8"/><rect x="216" y="234" width="6" height="50" fill="#dbad50"/><text x="242" y="267" class="sw-it">Doctrine and logistics adapt in combat</text></g>
        <g class="sw-lg sw-lg2"><rect x="987" y="122" width="731" height="50" rx="6" fill="#26243f" stroke="#e2915f" stroke-width="1.8"/><rect x="987" y="122" width="6" height="50" fill="#e2915f"/><text x="1013" y="155" class="sw-it">Uneven training and morale</text><rect x="987" y="178" width="731" height="50" rx="6" fill="#26243f" stroke="#e2915f" stroke-width="1.8"/><rect x="987" y="178" width="6" height="50" fill="#e2915f"/><text x="1013" y="211" class="sw-it">Dependence on advanced components</text><rect x="987" y="234" width="731" height="50" rx="6" fill="#26243f" stroke="#e2915f" stroke-width="1.8"/><rect x="987" y="234" width="6" height="50" fill="#e2915f"/><text x="1013" y="267" class="sw-it">Fragmented command and allocation</text></g>
        <g class="sw-lg sw-lg3"><rect x="216" y="346" width="731" height="44" rx="6" fill="#132b4a" stroke="#70a9d7" stroke-width="1.8"/><rect x="216" y="346" width="6" height="44" fill="#70a9d7"/><text x="242" y="375" class="sw-it">Equip partners against mass formations</text><rect x="216" y="398" width="731" height="44" rx="6" fill="#132b4a" stroke="#70a9d7" stroke-width="1.8"/><rect x="216" y="398" width="6" height="44" fill="#70a9d7"/><text x="242" y="427" class="sw-it">Expose rail and supply choke points</text><rect x="216" y="450" width="731" height="44" rx="6" fill="#132b4a" stroke="#70a9d7" stroke-width="1.8"/><rect x="216" y="450" width="6" height="44" fill="#70a9d7"/><text x="242" y="479" class="sw-it">Tighten export controls; integrate training</text></g>
        <g class="sw-lg sw-lg4"><rect x="987" y="346" width="731" height="44" rx="6" fill="#26243f" stroke="#e2915f" stroke-width="1.8"/><rect x="987" y="346" width="6" height="44" fill="#e2915f"/><text x="1013" y="375" class="sw-it">Attritional mass can exhaust smaller rivals</text><rect x="987" y="398" width="731" height="44" rx="6" fill="#26243f" stroke="#e2915f" stroke-width="1.8"/><rect x="987" y="398" width="6" height="44" fill="#e2915f"/><text x="1013" y="427" class="sw-it">EW, cyber and A2/AD innovation leaps</text><rect x="987" y="450" width="731" height="44" rx="6" fill="#26243f" stroke="#e2915f" stroke-width="1.8"/><rect x="987" y="450" width="6" height="44" fill="#e2915f"/><text x="1013" y="479" class="sw-it">Irregular forces create instability</text></g>
      </svg>
      <div class="ob-step s1" data-frag="1"><div class="ob-note wide" style="--x:5%;--y:70%;--w:90%"><div class="k">Strengths</div><div class="d">The report identifies three mutually reinforcing assets: mass manpower pipelines, a defense industry able to produce essential materiel at wartime scale, and adaptation driven by combat experience in doctrine, logistics and repair.</div></div></div>
      <div class="ob-step s2" data-frag="1"><div class="ob-note wide" style="--x:5%;--y:70%;--w:90%"><div class="k">Weaknesses</div><div class="d">Scale does not guarantee quality. Uneven training and welfare erode morale; sanctions expose dependence on advanced electronics, optics and alloys; and multiple military, regional and private power centers impede coherent command and resource allocation.</div></div></div>
      <div class="ob-step s3" data-frag="1"><div class="ob-note wide" style="--x:5%;--y:70%;--w:90%"><div class="k">Opportunities for NATO</div><div class="d">The report names concrete openings: equip partners to defeat mass formations and older hardware, use open-source intelligence to expose logistical choke points, tighten export controls, and integrate partner training and command platforms.</div></div></div>
      <div class="ob-step s4" data-frag="1"><div class="ob-note wide" style="--x:5%;--y:70%;--w:90%"><div class="k">Threats</div><div class="d">Russia can still prolong attritional war, concentrate innovation into dangerous EW, cyber or A2/AD advances, and use irregular formations in ways that make conflict less predictable and conventional deterrence harder to apply.</div></div></div></div>`;
  }

  if(typeof paintSidebar === 'function') paintSidebar();
  var title = document.getElementById('slidetitle');
  if(title && typeof slides !== 'undefined' && typeof cur !== 'undefined'){
    title.textContent = slides[cur].dataset.t || '';
  }
  if(typeof fitted !== 'undefined' && typeof autofit === 'function'){
    fitted = [];
    autofit(cur);
  }
})();
