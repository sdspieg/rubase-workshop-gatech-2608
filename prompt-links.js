(function(){
  var style = document.createElement('style');
  style.textContent = '.slide.has-prompt-qr h2,.slide.has-prompt-qr>.sub{max-width:82%}' +
    '.prompt-qr-card{position:absolute;z-index:18;top:1.25%;right:1.6%;width:11.5%;padding:.45%;background:#fff;border:2px solid var(--gold);border-radius:.45cqw;text-decoration:none;box-shadow:0 .35cqw 1.2cqw rgba(0,0,0,.28);line-height:1}' +
    '.prompt-qr-card img{display:block;width:100%;height:auto;image-rendering:pixelated}' +
    '.prompt-qr-card span{display:block;padding:.38cqw .15cqw .1cqw;color:#09182f;font:700 .78cqw/1.1 "Titillium Web",system-ui,sans-serif;text-align:center;letter-spacing:.08em}' +
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
    link.href = p.url;
    link.target = '_blank';
    link.rel = 'noopener';
    link.setAttribute('aria-label', 'Open the full prompt');
    link.innerHTML = '<img src="' + p.qr + '" alt="QR code linking to the full prompt">' +
      '<span>' + p.label + '</span>';
    slide.appendChild(link);
  });

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
