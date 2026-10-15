"""L2: вода — раковины наполняются как ванна (уровень в чаше), душ наполняет ванну,
кухонная раковина к стенке (кран у стены, чаша перед ним)."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    s = s.replace(old, new, count)


# ---------- 1) тик: у кранов-раковин уровень воды в чаше ----------
rep("""  /* вода: наполнение ванны и струя из смесителя */
  TAPS.forEach(function(t){
    if (t.sub !== 'tub') return;
    var target = t.fill ? 1 : 0;
    if (t.level < target) t.level = Math.min(target, t.level + dt*0.11);
    else if (t.level > target) t.level = Math.max(target, t.level - dt*0.22);
    var y = t.y0 + t.level*(t.y1 - t.y0);
    t.mesh.visible = t.level > 0.02;
    t.mesh.position.y = y;
    t.stream.visible = t.fill;
    if (t.stream.visible){
      t.stream.scale.y = Math.max(0.06, (0.70 - y) / 0.42);
      t.stream.position.y = y + (0.70 - y)/2;
    }
  });""",
    """  /* вода: наполнение ванны и чаш раковин, струи из смесителей */
  TAPS.forEach(function(t){
    if (t.sub !== 'tub' && !t.pool) return;
    var target = t.fill ? 1 : 0;
    if (t.level < target) t.level = Math.min(target, t.level + dt*(t.sub === 'tub' ? 0.11 : 0.14));
    else if (t.level > target) t.level = Math.max(target, t.level - dt*0.22);
    var y = t.y0 + t.level*(t.y1 - t.y0);
    if (t.sub === 'tub'){
      t.mesh.visible = t.level > 0.02;
      t.mesh.position.y = y;
      t.stream.visible = t.fill;
      if (t.stream.visible){
        t.stream.scale.y = Math.max(0.06, (0.70 - y) / 0.42);
        t.stream.position.y = y + (0.70 - y)/2;
      }
    } else {
      t.pool.visible = t.level > 0.02;
      t.pool.position.y = y;
      t.mesh.visible = t.fill;
    }
  });""")

# ---------- 2) переключатель: струя-кран наполняет чашу; душ наполняет ванну ----------
rep("""  if (t.sub === 'tub'){ t.fill = !t.fill; toast(t.fill ? 'Наливаю ванну 💧' : 'Сливаю воду…'); }
  else if (t.sub === 'shower'){ t.on = !t.on; t.mesh.visible = t.on; toast(t.on ? 'Душ включён 🚿' : 'Душ выключен'); }
  else if (t.sub === 'stream'){ t.on = !t.on; t.mesh.visible = t.on; toast((t.name || 'Кран') + (t.on ? ': вода пошла 💦' : ': вода закрыта')); }""",
    """  if (t.sub === 'tub'){ t.fill = !t.fill; toast(t.fill ? 'Наливаю ванну 💧' : 'Сливаю воду…'); }
  else if (t.sub === 'shower'){
    t.on = !t.on; t.mesh.visible = t.on;
    if (t.tub) t.tub.fill = t.on;                 /* душ наполняет ванну */
    toast(t.on ? 'Душ включён 🚿 — ванна наполняется' : 'Душ выключен');
  }
  else if (t.sub === 'stream'){
    t.on = !t.on; t.mesh.visible = t.on; t.fill = t.on;
    toast((t.name || 'Кран') + (t.on ? ': вода пошла 💦' : ': вода закрыта'));
  }""")

# ---------- 3) раковина в санузле: чаша с выемкой + вода ----------
rep("""  IT = item('Раковина', '🚰', 0.28, 0.21);
  ibox(IT, 6.18, 4.20, 0.54, 0.42, 0.70, 0.82, M.white);
  (function(){
    var bw = new THREE.Mesh(new THREE.PlaneGeometry(0.46, 0.34), M.white);
    bw.geometry.rotateX(-Math.PI/2); bw.position.set(mx(6.18), 0.826, 4.20); IT.add(bw);
    var bdr = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.006, 14), M.dark);
    bdr.position.set(mx(6.18), 0.827, 4.20); IT.add(bdr);""",
    """  IT = item('Раковина', '🚰', 0.28, 0.21);
  ibox(IT, 6.18, 4.20, 0.54, 0.42, 0.70, 0.74, M.white);              /* дно чаши */
  ibox(IT, 6.18, 4.025, 0.54, 0.07, 0.74, 0.83, M.white);             /* борта */
  ibox(IT, 6.18, 4.375, 0.54, 0.07, 0.74, 0.83, M.white);
  ibox(IT, 5.945, 4.20, 0.07, 0.28, 0.74, 0.83, M.white);
  ibox(IT, 6.415, 4.20, 0.07, 0.28, 0.74, 0.83, M.white);
  (function(){
    var bdr = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.006, 14), M.dark);
    bdr.position.set(mx(6.18), 0.742, 4.20); IT.add(bdr);""")
rep("""    var sStream = new THREE.Mesh(new THREE.CylinderGeometry(0.0075, 0.006, 0.15, 10), M.water);
    sStream.position.set(mx(6.23), 0.90, 4.20); sStream.visible = false; IT.add(sStream);
    var sTap = { kind:'tap', sub:'stream', on:false, mesh:sStream, name:'Санузел' };""",
    """    var sStream = new THREE.Mesh(new THREE.CylinderGeometry(0.0075, 0.006, 0.13, 10), M.water);
    sStream.position.set(mx(6.23), 0.90, 4.20); sStream.visible = false; IT.add(sStream);
    var sPool = new THREE.Mesh(new THREE.PlaneGeometry(0.40, 0.28), M.water);
    sPool.geometry.rotateX(-Math.PI/2); sPool.position.set(mx(6.18), 0.745, 4.20);
    sPool.visible = false; IT.add(sPool);
    var sTap = { kind:'tap', sub:'stream', on:false, mesh:sStream, name:'Санузел',
                 fill:false, level:0, pool:sPool, y0:0.745, y1:0.815 };""")

# ---------- 4) кухонная мойка: к стенке (кран у стены) + чаша с водой ----------
rep("""  IT = item('Мойка', '🚰', 0.26, 0.23, gProps);   /* южный конец столешницы */
  (function(){
    var rim = new THREE.Mesh(new THREE.BoxGeometry(0.50, 0.012, 0.44), M.steel);
    rim.position.set(mx(KX-0.31), WT+0.006, 2.44); rim.castShadow = true; IT.add(rim);
    var basin = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.34), M.white);
    basin.geometry.rotateX(-Math.PI/2); basin.position.set(mx(KX-0.31), WT+0.013, 2.44); IT.add(basin);
    var bdr2 = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.006, 14), M.dark);
    bdr2.position.set(mx(KX-0.31), WT+0.014, 2.44); IT.add(bdr2);
    function cyl(r1,r2,h,mat,x,y,z,rx,rz){ var c = new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,14), mat);
      c.position.set(mx(x), y, z); if (rx) c.rotation.x = rx; if (rz) c.rotation.z = rz; c.castShadow = true; IT.add(c); return c; }
    var ck1 = cyl(0.022,0.026,0.05, M.chrome, KX-0.07, WT+0.025, 2.44);
    var ck2 = cyl(0.015,0.015,0.26, M.chrome, KX-0.07, WT+0.16, 2.44);
    var ck3 = cyl(0.013,0.013,0.20, M.chrome, KX-0.17, WT+0.29, 2.44, null, Math.PI/2);
    var kStream = new THREE.Mesh(new THREE.CylinderGeometry(0.0075, 0.006, 0.26, 10), M.water);
    kStream.position.set(mx(KX-0.27), WT+0.155, 2.44); kStream.visible = false; IT.add(kStream);
    var kTap = { kind:'tap', sub:'stream', on:false, mesh:kStream, name:'Кухня' };""",
    """  IT = item('Мойка', '🚰', 0.26, 0.23, gProps);   /* южный конец столешницы, у стены */
  (function(){
    ibox(IT, 6.12, 2.44, 0.48, 0.44, WT, WT+0.04, M.white);            /* чаша: дно */
    ibox(IT, 6.12, 2.245, 0.48, 0.06, WT+0.04, WT+0.13, M.white);      /* борта */
    ibox(IT, 6.12, 2.635, 0.48, 0.06, WT+0.04, WT+0.13, M.white);
    ibox(IT, 5.91, 2.44, 0.06, 0.32, WT+0.04, WT+0.13, M.white);
    ibox(IT, 6.33, 2.44, 0.06, 0.32, WT+0.04, WT+0.13, M.white);
    [[6.12, 2.245, 0.52, 0.05], [6.12, 2.635, 0.52, 0.05], [5.90, 2.44, 0.05, 0.40], [6.34, 2.44, 0.05, 0.40]].forEach(function(rr){
      var st = new THREE.Mesh(new THREE.BoxGeometry(rr[2], 0.012, rr[3]), M.steel);
      st.position.set(mx(rr[0]), WT+0.136, rr[1]); IT.add(st);
    });
    var bdr2 = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.006, 14), M.dark);
    bdr2.position.set(mx(6.12), WT+0.042, 2.44); IT.add(bdr2);
    function cyl(r1,r2,h,mat,x,y,z,rx,rz){ var c = new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,14), mat);
      c.position.set(mx(x), y, z); if (rx) c.rotation.x = rx; if (rz) c.rotation.z = rz; c.castShadow = true; IT.add(c); return c; }
    var ck1 = cyl(0.022,0.026,0.05, M.chrome, KX-0.06, WT+0.025, 2.44);
    var ck2 = cyl(0.015,0.015,0.26, M.chrome, KX-0.06, WT+0.16, 2.44);
    var ck3 = cyl(0.013,0.013,0.22, M.chrome, KX-0.16, WT+0.29, 2.44, null, Math.PI/2);
    var kStream = new THREE.Mesh(new THREE.CylinderGeometry(0.0075, 0.006, 0.24, 10), M.water);
    kStream.position.set(mx(6.26), WT+0.155, 2.44); kStream.visible = false; IT.add(kStream);
    var kPool = new THREE.Mesh(new THREE.PlaneGeometry(0.38, 0.30), M.water);
    kPool.geometry.rotateX(-Math.PI/2); kPool.position.set(mx(6.12), WT+0.045, 2.44);
    kPool.visible = false; IT.add(kPool);
    var kTap = { kind:'tap', sub:'stream', on:false, mesh:kStream, name:'Кухня',
                 fill:false, level:0, pool:kPool, y0:WT+0.045, y1:WT+0.115 };""")

# ---------- 5) душ наполняет ванну ----------
rep("""    var tTub = { kind:'tap', sub:'tub', fill:false, level:0, mesh:wl, stream:stream,
                 y0:0.15, y1:0.50, name:'Ванна' };
    wm(tap, tTub); wm(spout, tTub);
    TAPS.push(tSh); TAPS.push(tTub);""",
    """    var tTub = { kind:'tap', sub:'tub', fill:false, level:0, mesh:wl, stream:stream,
                 y0:0.15, y1:0.50, name:'Ванна' };
    tSh.tub = tTub;                              /* душ тоже наполняет ванну */
    wm(tap, tTub); wm(spout, tTub);
    TAPS.push(tSh); TAPS.push(tTub);""")

p.write_text(s, encoding='utf-8')
print('L2 ok')
