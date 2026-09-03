(function(){
  'use strict';

  var DATA_URL = 'resources/glossary.json';
  var SKIP = 'script,style,noscript,textarea,input,select,option,button,a,code,pre,kbd,samp,svg,math,.gloss,.glossary-block,.glossary-tooltip,.glossary-term,[data-no-glossary]';
  var linked = 0;
  var matcher;
  var byLabel = new Map();
  var panel;
  var panelTerm;
  var panelDefinition;
  var active;

  function key(value){ return String(value || '').trim().toLocaleLowerCase('en-US'); }
  function escapeRegExp(value){ return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  function addStyles(){
    if(document.getElementById('glossaryTooltipStyles')) return;
    var style = document.createElement('style');
    style.id = 'glossaryTooltipStyles';
    style.textContent = [
      '.glossary-term{color:inherit;text-decoration-line:underline;text-decoration-style:dotted;text-decoration-color:rgba(219,173,80,.72);text-decoration-thickness:1px;text-underline-offset:3px;cursor:help;border-radius:2px}',
      '.glossary-term:hover,.glossary-term:focus-visible{color:#f3f6fb;background:rgba(219,173,80,.14);outline:1px solid rgba(219,173,80,.44);outline-offset:2px}',
      '.glossary-tooltip{position:fixed;z-index:20000;width:min(390px,calc(100vw - 24px));padding:13px 15px 14px;background:#132f59;color:#f3f6fb;border:1px solid #dbad50;border-left:4px solid #dbad50;border-radius:6px;box-shadow:0 12px 34px rgba(0,0,0,.48);font-family:system-ui,-apple-system,"Segoe UI",Helvetica,sans-serif;text-align:left;pointer-events:none}',
      '.glossary-tooltip[hidden]{display:none}',
      '.glossary-tooltip strong{display:block;margin:0 0 5px;color:#dbad50;font-size:.92rem;line-height:1.25}',
      '.glossary-tooltip p{margin:0;color:#c2d4e8;font-size:.82rem;line-height:1.48}',
      '.glossary-tooltip small{display:block;margin-top:8px;color:#9db8d6;font-size:.67rem;letter-spacing:.02em}',
      '@media(max-width:620px){.glossary-tooltip{width:calc(100vw - 20px);left:10px!important}}'
    ].join('');
    document.head.appendChild(style);
  }

  function buildPanel(){
    panel = document.createElement('aside');
    panel.id = 'glossaryTooltip';
    panel.className = 'glossary-tooltip';
    panel.setAttribute('role', 'tooltip');
    panel.hidden = true;
    panelTerm = document.createElement('strong');
    panelDefinition = document.createElement('p');
    var hint = document.createElement('small');
    hint.textContent = 'Plain-English definition from “The words we use”';
    panel.append(panelTerm, panelDefinition, hint);
    document.body.appendChild(panel);
  }

  function place(anchor){
    var rect = anchor.getBoundingClientRect();
    panel.hidden = false;
    panel.style.visibility = 'hidden';
    var box = panel.getBoundingClientRect();
    var left = Math.max(12, Math.min(rect.left, window.innerWidth - box.width - 12));
    var above = rect.top - box.height - 10;
    var top = above >= 10 ? above : Math.min(window.innerHeight - box.height - 10, rect.bottom + 10);
    panel.style.left = Math.round(left) + 'px';
    panel.style.top = Math.round(Math.max(10, top)) + 'px';
    panel.style.visibility = 'visible';
  }

  function show(anchor){
    active = anchor;
    panelTerm.textContent = anchor.dataset.glossaryTerm;
    panelDefinition.textContent = anchor.dataset.glossaryDefinition;
    anchor.setAttribute('aria-describedby', panel.id);
    place(anchor);
  }

  function hide(anchor){
    if(anchor && active !== anchor) return;
    if(active) active.removeAttribute('aria-describedby');
    active = null;
    panel.hidden = true;
  }

  function makeTerm(text, entry){
    var span = document.createElement('span');
    span.className = 'glossary-term';
    span.tabIndex = 0;
    span.textContent = text;
    span.dataset.glossaryTerm = entry.term;
    span.dataset.glossaryDefinition = entry.definition;
    span.setAttribute('aria-label', text + ': ' + entry.definition);
    span.addEventListener('mouseenter', function(){ show(span); });
    span.addEventListener('mouseleave', function(){ hide(span); });
    span.addEventListener('focus', function(){ show(span); });
    span.addEventListener('blur', function(){ hide(span); });
    span.addEventListener('click', function(event){ event.stopPropagation(); show(span); });
    linked += 1;
    return span;
  }

  function eligible(node){
    var parent = node.parentElement;
    if(!parent || !node.nodeValue || node.nodeValue.trim().length < 2) return false;
    return !parent.closest(SKIP);
  }

  function linkTextNode(node){
    if(!eligible(node)) return;
    var text = node.nodeValue;
    matcher.lastIndex = 0;
    var matches = Array.from(text.matchAll(matcher));
    if(!matches.length) return;
    var fragment = document.createDocumentFragment();
    var cursor = 0;
    matches.forEach(function(match){
      var prefix = match[1] || '';
      var label = match[2];
      var labelStart = match.index + prefix.length;
      if(labelStart > cursor) fragment.appendChild(document.createTextNode(text.slice(cursor, labelStart)));
      fragment.appendChild(makeTerm(text.slice(labelStart, labelStart + label.length), byLabel.get(key(label))));
      cursor = labelStart + label.length;
    });
    if(cursor < text.length) fragment.appendChild(document.createTextNode(text.slice(cursor)));
    node.replaceWith(fragment);
  }

  function process(root){
    if(!root || (root.nodeType === 1 && root.matches && root.matches(SKIP))) return;
    if(root.nodeType === Node.TEXT_NODE){ linkTextNode(root); return; }
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    var nodes = [];
    while(walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(linkTextNode);
    window.__GLOSSARY_TOOLTIP_STATS__ = {linkedOccurrences: linked, glossaryLabels: byLabel.size};
  }

  function start(data){
    (data.entries || []).forEach(function(entry){
      [entry.term].concat(entry.aliases || []).forEach(function(label){
        label = String(label || '').trim();
        if(label.length < 2 || label.length > 90 || !/[A-Za-zÀ-ÖØ-öø-ÿ]/.test(label)) return;
        var normalized = key(label);
        if(!byLabel.has(normalized)) byLabel.set(normalized, entry);
      });
    });
    var labels = Array.from(byLabel.keys()).sort(function(a,b){ return b.length - a.length; });
    matcher = new RegExp('(^|[^\\p{L}\\p{N}])(' + labels.map(escapeRegExp).join('|') + ')(?=$|[^\\p{L}\\p{N}])', 'giu');
    addStyles();
    buildPanel();
    process(document.body);
    document.documentElement.dataset.glossaryReady = 'true';
    document.dispatchEvent(new CustomEvent('glossary:linked', {detail: window.__GLOSSARY_TOOLTIP_STATS__}));

    var observer = new MutationObserver(function(records){
      records.forEach(function(record){
        record.addedNodes.forEach(function(node){
          if(node !== panel && !panel.contains(node)) process(node);
        });
      });
    });
    observer.observe(document.body, {childList:true, subtree:true});
    document.addEventListener('click', function(event){ if(!event.target.closest('.glossary-term')) hide(); });
    document.addEventListener('keydown', function(event){ if(event.key === 'Escape') hide(); });
    window.addEventListener('scroll', function(){ if(active) place(active); }, {passive:true});
    window.addEventListener('resize', function(){ if(active) place(active); });
  }

  fetch(DATA_URL, {cache:'no-store'})
    .then(function(response){ if(!response.ok) throw new Error('HTTP ' + response.status); return response.json(); })
    .then(start)
    .catch(function(error){ console.warn('Glossary tooltips unavailable:', error); });
})();
