(function(){
  'use strict';
  var prompts = {
    'taxonomy-generation': ['Generate a taxonomy', 'resources/taxonomy_generation_prompt.md'],
    'taxonomy-classification': ['Classify a corpus with a taxonomy', 'resources/taxonomy_classification_prompt.md'],
    'report-writing': ['Write an evidence-grounded report', 'resources/report_writing_prompt.md'],
    'day4-prompts': ['Day 4 prompts', 'resources/day4_prompts.md'],
    'mdtdf': ['Multi-Dimensional Taxonomy Development Framework prompt', 'resources/MDTDF_PROMPT.md']
  };
  var id = new URLSearchParams(location.search).get('id') || 'taxonomy-generation';
  var selected = prompts[id];
  var title = document.getElementById('promptTitle');
  var text = document.getElementById('promptText');
  var download = document.getElementById('downloadPrompt');
  var copy = document.getElementById('copyPrompt');
  var status = document.getElementById('copyStatus');
  var raw = '';

  if(!selected){
    title.textContent = 'Prompt not found';
    text.textContent = 'Use the Materials page to open one of the workshop prompts.';
    text.classList.add('error');
    copy.disabled = true;
    return;
  }

  title.textContent = selected[0];
  document.title = selected[0] + ' · Georgia Tech workshop';
  download.href = selected[1];
  fetch(selected[1], {cache:'no-store'})
    .then(function(response){ if(!response.ok) throw new Error('HTTP ' + response.status); return response.text(); })
    .then(function(value){ raw = value; text.textContent = raw; })
    .catch(function(){ text.textContent = 'The prompt could not be loaded. Return to Materials and use the Markdown download.'; text.classList.add('error'); copy.disabled = true; });

  copy.addEventListener('click', function(){
    if(!raw) return;
    navigator.clipboard.writeText(raw).then(function(){
      status.textContent = 'Copied.';
      window.setTimeout(function(){ status.textContent = ''; }, 2500);
    }).catch(function(){ status.textContent = 'Copy failed – select the prompt text and copy it manually.'; });
  });
})();
