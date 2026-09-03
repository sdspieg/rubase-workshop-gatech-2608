(function(){
  'use strict';

  var alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  var state = { entries: [], query: '' };

  function buildShell(){
    var block = document.getElementById('block-glossary');
    if(!block) return false;

    block.classList.add('glossary-block');
    block.replaceChildren();

    var back = make('button', 'back-home', '← Back to overview');
    back.type = 'button';
    back.addEventListener('click', function(){ window.showHome(); });
    block.appendChild(back);

    var header = make('div', 'block-header');
    header.appendChild(make('h2', '', 'The words we use'));
    var status = make('div', 'block-time-range', 'Loading the full glossary…');
    status.id = 'glossaryStatus';
    status.setAttribute('aria-live', 'polite');
    header.appendChild(status);
    header.appendChild(make('p', '', 'Search a word or abbreviation, or jump straight to its first letter. These definitions cover the language used across the entire workshop app, its slides, cases, prompts and guides – including every term in the AIRA glossary.'));
    block.appendChild(header);

    var tools = make('div', 'glossary-tools');
    var label = make('label', '', 'Find a word or abbreviation');
    label.htmlFor = 'glossarySearch';
    tools.appendChild(label);
    var row = make('div', 'glossary-search-row');
    var input = make('input', 'glossary-search');
    input.id = 'glossarySearch';
    input.type = 'search';
    input.autocomplete = 'off';
    input.placeholder = 'Try “abstract coverage”, “LLM”, “kappa” or “SWOT”';
    var clear = make('button', 'glossary-clear', 'Clear');
    clear.id = 'glossaryClear';
    clear.type = 'button';
    row.appendChild(input);
    row.appendChild(clear);
    tools.appendChild(row);
    var nav = make('nav', 'glossary-alphabet');
    nav.id = 'glossaryAlphabet';
    nav.setAttribute('aria-label', 'Jump to a glossary letter');
    tools.appendChild(nav);
    block.appendChild(tools);

    var root = make('div', 'glossary-list-root');
    root.id = 'glossaryList';
    root.setAttribute('aria-live', 'polite');
    root.appendChild(make('p', 'glossary-loading', 'Loading the glossary…'));
    block.appendChild(root);

    var callout = make('div', 'callout');
    var strong = make('strong', '', 'If a word is used in the room and you do not know it, say so. ');
    callout.appendChild(strong);
    callout.appendChild(document.createTextNode('Every term here was jargon to everyone present at some point, and the person who asks is usually asking for four other people as well.'));
    block.appendChild(callout);

    var badge = document.querySelector('.sidebar-item[data-block="glossary"] .sidebar-badge');
    if(badge) badge.classList.add('glossary-badge');
    return true;
  }

  function normalize(value){
    return String(value || '')
      .normalize('NFKD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase();
  }

  function firstLetter(term){
    var match = String(term || '').normalize('NFKD').match(/[A-Za-z]/);
    return match ? match[0].toUpperCase() : '#';
  }

  function searchable(entry){
    return normalize([
      entry.term,
      (entry.aliases || []).join(' '),
      entry.definition,
      (entry.aira_source_terms || []).join(' '),
      (entry.workshop_required_terms || []).join(' '),
      (entry.sweep_terms || []).join(' ')
    ].join(' '));
  }

  function make(tag, className, text){
    var node = document.createElement(tag);
    if(className) node.className = className;
    if(text !== undefined) node.textContent = text;
    return node;
  }

  function renderAlphabet(lettersPresent){
    var nav = document.getElementById('glossaryAlphabet');
    nav.replaceChildren();
    alphabet.forEach(function(letter){
      var button = make('button', 'glossary-letter', letter);
      button.type = 'button';
      button.disabled = !lettersPresent.has(letter);
      button.setAttribute('aria-label', button.disabled ? 'No visible terms beginning with ' + letter : 'Jump to terms beginning with ' + letter);
      if(!button.disabled){
        button.addEventListener('click', function(){
          var target = document.getElementById('glossary-' + letter);
          var header = document.querySelector('.header');
          if(target){
            var top = window.scrollY + target.getBoundingClientRect().top;
            var offset = (header ? header.offsetHeight : 0) + 18;
            window.scrollTo({top: Math.max(0, top - offset), behavior:'auto'});
          }
        });
      }
      nav.appendChild(button);
    });
  }

  function render(){
    var query = normalize(state.query.trim());
    var visible = state.entries.filter(function(entry){
      return !query || searchable(entry).indexOf(query) !== -1;
    });
    var groups = new Map();
    visible.forEach(function(entry){
      var letter = firstLetter(entry.term);
      if(!groups.has(letter)) groups.set(letter, []);
      groups.get(letter).push(entry);
    });

    var root = document.getElementById('glossaryList');
    root.replaceChildren();
    Array.from(groups.keys()).sort().forEach(function(letter){
      var section = make('section', 'glossary-group');
      section.id = 'glossary-' + letter;
      section.setAttribute('aria-labelledby', 'glossary-heading-' + letter);
      var heading = make('h3', 'glossary-group-heading', letter);
      heading.id = 'glossary-heading-' + letter;
      section.appendChild(heading);
      var list = make('dl', 'glossary-list');
      groups.get(letter).sort(function(a, b){ return a.term.localeCompare(b.term, 'en', {sensitivity:'base'}); }).forEach(function(entry){
        var item = make('div', 'glossary-entry');
        item.appendChild(make('dt', '', entry.term));
        if(entry.aliases && entry.aliases.length){
          item.appendChild(make('div', 'glossary-aliases', 'Also: ' + entry.aliases.join(' · ')));
        }
        item.appendChild(make('dd', '', entry.definition));
        list.appendChild(item);
      });
      section.appendChild(list);
      root.appendChild(section);
    });

    if(!visible.length){
      root.appendChild(make('p', 'glossary-empty', 'No term matches “' + state.query.trim() + '”. Try an abbreviation, a shorter word, or a related term.'));
    }
    renderAlphabet(new Set(groups.keys()));
    var status = document.getElementById('glossaryStatus');
    status.textContent = query ? 'Showing ' + visible.length + ' of ' + state.entries.length + ' terms' : state.entries.length + ' terms, in plain English';
  }

  function start(data){
    state.entries = data.entries || [];
    var badge = document.querySelector('.glossary-badge');
    if(badge) badge.textContent = String(state.entries.length);
    var input = document.getElementById('glossarySearch');
    var clear = document.getElementById('glossaryClear');
    input.addEventListener('input', function(){ state.query = input.value; render(); });
    clear.addEventListener('click', function(){ input.value = ''; state.query = ''; input.focus(); render(); });
    render();
  }

  function fail(){
    var root = document.getElementById('glossaryList');
    root.replaceChildren(make('p', 'glossary-empty', 'The glossary could not be loaded. Reload the page or use the Materials link to report the problem.'));
  }

  if(!buildShell()) return;

  fetch('resources/glossary.json', {cache:'no-store'})
    .then(function(response){ if(!response.ok) throw new Error('HTTP ' + response.status); return response.json(); })
    .then(start)
    .catch(fail);
})();
