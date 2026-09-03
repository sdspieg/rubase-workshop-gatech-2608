(function(){
  'use strict';
  var routes = {
    'resources/taxonomy_generation_prompt.md': 'prompt.html?id=taxonomy-generation',
    'resources/taxonomy_classification_prompt.md': 'prompt.html?id=taxonomy-classification',
    'resources/report_writing_prompt.md': 'prompt.html?id=report-writing',
    'resources/day4_prompts.md': 'prompt.html?id=day4-prompts',
    'resources/MDTDF_PROMPT.md': 'prompt.html?id=mdtdf'
  };
  document.querySelectorAll('a[href]').forEach(function(link){
    var target = link.getAttribute('href');
    if(routes[target] && !link.hasAttribute('download')) link.setAttribute('href', routes[target]);
  });
})();
