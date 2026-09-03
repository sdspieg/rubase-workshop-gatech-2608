(function(){
  var valid = ['prompts','data','tools','records'];

  window.showMaterialTab = function(id,writeHash){
    if(valid.indexOf(id) < 0) id = 'prompts';
    document.querySelectorAll('.materials-panel').forEach(function(panel){
      var active = panel.id === 'materials-' + id;
      panel.classList.toggle('active',active);
      panel.hidden = !active;
    });
    document.querySelectorAll('.materials-tab').forEach(function(button){
      var active = button.id === 'materials-tab-' + id;
      button.classList.toggle('active',active);
      button.setAttribute('aria-selected',active ? 'true' : 'false');
    });
    var area = document.querySelector('.content-area');
    if(area) area.scrollTop = 0;
    if(writeHash !== false) history.replaceState(null,'','#materials/' + id);
  };

  var hash = (location.hash || '').replace('#','');
  if(window.__requestedMaterialsTab || hash.indexOf('materials/') === 0){
    var id = window.__requestedMaterialsTab || hash.split('/')[1] || 'prompts';
    if(typeof showBlock === 'function') showBlock('materials');
    window.showMaterialTab(id,true);
  }
})();
