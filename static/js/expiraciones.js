// expiaciones.js - populate expirations lists
(function(){
  function fetchList(url, listSelector, toggleButtonSelector, extraListSelector){
    const list = document.querySelector(listSelector);
    const extra = document.querySelector(extraListSelector);
    const toggle = document.querySelector(toggleButtonSelector);
    if(!list) return;
    list.innerHTML = '';

    fetch(url).then(r => {
      if(!r.ok){
        // Mostrar un elemento de error en la lista
        const li = document.createElement('li');
        li.textContent = `Error cargando vencimientos: HTTP ${r.status}`;
        li.style.color = '#6c757d';
        list.appendChild(li);
        if(toggle) toggle.style.display = 'none';
        return null;
      }
      return r.json();
    }).then(data=>{
      if(!data) return;
      const items = data.items || [];
      const visible = items.slice(0,5);
      const hidden = items.slice(5);
      visible.forEach(i=>{
        const li = document.createElement('li');
        li.textContent = `${i.nombre} — ${i.caducidad}`;
        list.appendChild(li);
      });
      if(extra){
        extra.innerHTML = '';
        hidden.forEach(i=>{
          const li = document.createElement('li');
          li.textContent = `${i.nombre} — ${i.caducidad}`;
          extra.appendChild(li);
        });
      }
      if(toggle){
        if(hidden.length>0){
          toggle.style.display = '';
          toggle.addEventListener('click', function(){
            if(extra.style.display === 'none' || extra.style.display === ''){
              extra.style.display = 'block';
              toggle.textContent = 'Ver menos';
            } else {
              extra.style.display = 'none';
              toggle.textContent = 'Ver más';
            }
          });
        } else {
          toggle.style.display = 'none';
        }
      }
    }).catch(err=>{
      const li = document.createElement('li');
      li.textContent = `Error cargando vencimientos: ${err.message}`;
      li.style.color = '#6c757d';
      list.appendChild(li);
      if(toggle) toggle.style.display = 'none';
      console.warn('expiraciones fetch error',err);
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    fetchList('/ventas/api/productos_por_vencer/7/', '#vencimientos-list', '#vencimientos-toggle', '#vencimientos-extra-list');
    fetchList('/ventas/api/productos_por_vencer/14/', '#vencimientos-14-list', '#vencimientos-14-toggle', '#vencimientos-14-extra-list');
    fetchList('/ventas/api/productos_por_vencer/30/', '#vencimientos-30-list', '#vencimientos-30-toggle', '#vencimientos-30-extra-list');
  });
})();
