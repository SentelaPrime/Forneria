// Minimal dashboard_charts.js - provides initGaugeChart fallback so template doesn't break
function initGaugeChart(selector, dataUrl, maxValue, title){
  var container = document.querySelector(selector);
  if(!container) return;

  // helper to show error message inside the container
  function showError(msg){
    container.innerHTML = '';
    var err = document.createElement('div');
    err.className = 'gauge-error';
    err.style.color = '#d9534f';
    err.style.textAlign = 'center';
    err.style.padding = '20px';
    err.textContent = msg;
    container.appendChild(err);
  }

  // If no dataUrl provided, render a simple placeholder
  if(!dataUrl || dataUrl === '#' ){
    var el = document.createElement('div');
    el.className = 'gauge-placeholder';
    el.style.minHeight = '120px';
    el.style.display = 'flex';
    el.style.alignItems = 'center';
    el.style.justifyContent = 'center';
    el.style.border = '1px dashed #ddd';
    el.style.borderRadius = '8px';
    el.style.background = '#fff';
    el.textContent = title + ' (gráfico)';
    container.appendChild(el);
    return;
  }

  // If a real dataUrl is given, try to fetch it and show error on failure
  fetch(dataUrl).then(function(resp){
    if(!resp.ok) throw new Error('HTTP ' + resp.status);
    return resp.json();
  }).then(function(data){
    // TODO: render D3 chart using `data`. For now show placeholder with value if present
    container.innerHTML = '';
    var el = document.createElement('div');
    el.className = 'gauge-placeholder';
    el.style.minHeight = '120px';
    el.style.display = 'flex';
    el.style.alignItems = 'center';
    el.style.justifyContent = 'center';
    el.style.border = '1px dashed #ddd';
    el.style.borderRadius = '8px';
    el.style.background = '#fff';
    var value = (data && data.value) ? data.value : '—';
    el.textContent = title + ': ' + value;
    container.appendChild(el);
  }).catch(function(err){
    console.warn('gauge load error', err);
    showError('No se pudo cargar el gráfico.');
  });
}
