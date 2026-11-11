(function(){
  // Seeded RNG so a given seed always produces the same "kid coloring"
  var seed = (window.CRAYON_SEED != null) ? window.CRAYON_SEED : Math.floor(Math.random()*1e9);
  function rng(){ seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }

  // Make every region its own crayon fill layer, slightly off the lines (like a real kid)
  document.querySelectorAll('svg.art').forEach(function(svg){
    svg.querySelectorAll('g.r').forEach(function(g){
      var c = g.cloneNode(true);
      c.setAttribute('class','wax');
      c.setAttribute('fill', g.getAttribute('data-c'));
      var dx = (rng()*9-4.5).toFixed(1), dy = (rng()*9-4.5).toFixed(1), rot = (rng()*3-1.5).toFixed(2);
      c.setAttribute('transform','translate('+dx+' '+dy+') rotate('+rot+' 300 190)');
      g.parentNode.insertBefore(c, g);
      g.setAttribute('class','line');
    });
  });
  // Rainbow, wobbly crayon titles
  var cols = ['#e53935','#fb8c00','#f2b705','#43a047','#1e88e5','#8e24aa'];
  document.querySelectorAll('.rb').forEach(function(el){
    var words = el.textContent.split(' '); el.textContent = ''; var i = 0;
    words.forEach(function(w, wi){
      var ws = document.createElement('span'); ws.style.whiteSpace = 'nowrap'; ws.style.display = 'inline-block';
      w.split('').forEach(function(ch){
        var s = document.createElement('span');
        s.textContent = ch; s.style.color = cols[i++ % cols.length]; s.style.display = 'inline-block';
        s.style.transform = 'rotate(' + (rng()*10-5).toFixed(1) + 'deg) translateY(' + (rng()*6-3).toFixed(1) + 'px)';
        ws.appendChild(s);
      });
      el.appendChild(ws);
      if(wi < words.length-1){ el.appendChild(document.createTextNode(' ')); }
    });
  });
})();
