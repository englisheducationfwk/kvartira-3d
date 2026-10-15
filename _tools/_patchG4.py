"""G4: кухня — дубли-раковину и плиту убрать (пункты-предметы переезжают на их место),
половинка шкафчика из стены, домовая круглая вытяжка, пожарный датчик на западной
стене, стол +30 см со скруглением, два табурета на 4 ножках (светлые)."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:120]
    s = s.replace(old, new, count)


# --- светлое дерево для табуретов
rep("  woodDark:  new THREE.MeshStandardMaterial({ color:0x8a6a48, roughness:.7 }),",
    "  woodDark:  new THREE.MeshStandardMaterial({ color:0x8a6a48, roughness:.7 }),\n  woodLight: new THREE.MeshStandardMaterial({ color:0xdcc19b, roughness:.7 }),")

# --- половинка фасада у стены (шкафчик «в стене»): прижать к ряду
rep("""  front(KX-0.61, BASE+LOWH/2, 2.86, 0.22, LOWH-0.04);
  var h4 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.02, 0.11), M.handleOld);
  h4.position.set(mx(KX-0.63), BASE+LOWH-0.10, 2.86); h4.castShadow = true; handles.push(h4); doorsGrp.add(h4);""",
    """  front(KX-0.61, BASE+LOWH/2, 2.74, 0.30, LOWH-0.04);
  var h4 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.02, 0.11), M.handleOld);
  h4.position.set(mx(KX-0.63), BASE+LOWH-0.10, 2.74); h4.castShadow = true; handles.push(h4); doorsGrp.add(h4);""")

# --- старая декоративная мойка (не-предмет!) — убрать, предмет «Мойка» переезжает сюда
rep("""  /* мойка в углу у эркера */
  (function(){
    var rim = new THREE.Mesh(new THREE.BoxGeometry(0.50, 0.012, 0.44), M.steel);
    rim.position.set(mx(KX-0.31), WT+0.006, 2.44); gKitchen.add(rim);
    var basin = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.34), M.dark);
    basin.geometry.rotateX(-Math.PI/2); basin.position.set(mx(KX-0.31), WT+0.013, 2.44); gKitchen.add(basin);
    function cyl(r1,r2,h,mat,x,y,z,rx,rz){ var c = new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,14), mat);
      c.position.set(mx(x), y, z); if (rx) c.rotation.x = rx; if (rz) c.rotation.z = rz; c.castShadow = true; gKitchen.add(c); return c; }
    cyl(0.022,0.026,0.05, M.chrome, KX-0.31, WT+0.025, 2.70);
    cyl(0.015,0.015,0.26, M.chrome, KX-0.31, WT+0.16, 2.70);
    cyl(0.013,0.013,0.20, M.chrome, KX-0.31, WT+0.29, 2.59, Math.PI/2);
  })();
  /* варочная */
  (function(){
    var ct = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.013, 0.50), M.black);
    ct.position.set(mx(KX-0.31), WT+0.006, 1.05); gKitchen.add(ct);
    [[KX-0.17,0.94],[KX-0.45,0.94],[KX-0.17,1.17],[KX-0.45,1.17]].forEach(function(b){
      var ring = new THREE.Mesh(new THREE.CylinderGeometry(0.072,0.072,0.004,24), M.dark);
      ring.position.set(mx(b[0]), WT+0.014, b[1]); gKitchen.add(ring);
      var core = new THREE.Mesh(new THREE.CylinderGeometry(0.026,0.026,0.005,18), M.steel);
      core.position.set(mx(b[0]), WT+0.015, b[1]); gKitchen.add(core);
    });
    [0.87,0.99,1.11,1.23].forEach(function(z){
      var k2 = new THREE.Mesh(new THREE.CylinderGeometry(0.015,0.015,0.022,12), M.black);
      k2.position.set(mx(KX-0.055), WT+0.011, z); gKitchen.add(k2);
    });
  })();""",
    """  /* (декоративные дубли мойки и плиты убраны — всё живёт в предметах ниже) */
  /* домовая круглая вытяжка у потолка южной стены кухни */
  (function(){
    var vr = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.085, 0.05, 24), M.steel);
    vr.rotation.x = Math.PI/2; vr.position.set(mx(4.93), 2.36, K.z1-0.022); gKitchen.add(vr);
    var vd = new THREE.Mesh(new THREE.CircleGeometry(0.062, 22), M.dark);
    vd.rotation.y = Math.PI; vd.position.set(mx(4.93), 2.36, K.z1-0.048); gKitchen.add(vd);
    for (var vi=0; vi<3; vi++){
      var vb = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.008, 0.006), M.steel);
      vb.position.set(mx(4.93), 2.36, K.z1-0.049); vb.rotation.z = vi*Math.PI/3; gKitchen.add(vb);
    }
  })();
  /* пожарный датчик на западной стене кухни */
  (function(){
    var fd = new THREE.Mesh(new THREE.CylinderGeometry(0.058, 0.058, 0.035, 20), M.frame);
    fd.rotation.z = Math.PI/2; fd.position.set(mx(K.x0)+0.0175, 2.36, 2.08);
    fd.castShadow = true; gKitchen.add(fd);
    var fl2 = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.012, 12),
      new THREE.MeshStandardMaterial({ color:0xc0392b, roughness:.4 }));
    fl2.rotation.z = Math.PI/2; fl2.position.set(mx(K.x0)+0.036, 2.36, 2.08); gKitchen.add(fl2);
  })();""")

# --- предмет «Мойка»: с висящего места на своё (южный конец столешницы)
rep("""  IT = item('Мойка', '🚰', 0.26, 0.23, gProps);   /* южный конец столешницы */
  (function(){
    var rim = new THREE.Mesh(new THREE.BoxGeometry(0.50, 0.012, 0.44), M.steel);
    rim.position.set(mx(KX-0.31), WT+0.006, 0.30); rim.castShadow = true; IT.add(rim);
    var basin = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.34), M.dark);
    basin.geometry.rotateX(-Math.PI/2); basin.position.set(mx(KX-0.31), WT+0.013, 0.30); IT.add(basin);
    function cyl(r1,r2,h,mat,x,y,z,rx,rz){ var c = new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,14), mat);
      c.position.set(mx(x), y, z); if (rx) c.rotation.x = rx; if (rz) c.rotation.z = rz; c.castShadow = true; IT.add(c); return c; }
    cyl(0.022,0.026,0.05, M.chrome, KX-0.31, WT+0.025, 0.04);
    cyl(0.015,0.015,0.26, M.chrome, KX-0.31, WT+0.16, 0.04);
    cyl(0.013,0.013,0.20, M.chrome, KX-0.31, WT+0.29, 0.15, Math.PI/2);
  })();""",
    """  IT = item('Мойка', '🚰', 0.26, 0.23, gProps);   /* южный конец столешницы */
  (function(){
    var rim = new THREE.Mesh(new THREE.BoxGeometry(0.50, 0.012, 0.44), M.steel);
    rim.position.set(mx(KX-0.31), WT+0.006, 2.44); rim.castShadow = true; IT.add(rim);
    var basin = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.34), M.dark);
    basin.geometry.rotateX(-Math.PI/2); basin.position.set(mx(KX-0.31), WT+0.013, 2.44); IT.add(basin);
    function cyl(r1,r2,h,mat,x,y,z,rx,rz){ var c = new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,14), mat);
      c.position.set(mx(x), y, z); if (rx) c.rotation.x = rx; if (rz) c.rotation.z = rz; c.castShadow = true; IT.add(c); return c; }
    cyl(0.022,0.026,0.05, M.chrome, KX-0.31, WT+0.025, 2.70);
    cyl(0.015,0.015,0.26, M.chrome, KX-0.31, WT+0.16, 2.70);
    cyl(0.013,0.013,0.20, M.chrome, KX-0.31, WT+0.29, 2.59, Math.PI/2);
  })();""")

# --- предмет «Варочная панель»: на своё место + ручки
rep("""  IT = item('Варочная панель', '🔥', 0.29, 0.26, gProps);
  (function(){
    var ct = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.013, 0.50), M.black);
    ct.position.set(mx(KX-0.31), WT+0.006, 1.80); IT.add(ct);
    [[KX-0.17,1.69],[KX-0.45,1.69],[KX-0.17,1.92],[KX-0.45,1.92]].forEach(function(b){
      var ring = new THREE.Mesh(new THREE.CylinderGeometry(0.072,0.072,0.004,24), M.dark);
      ring.position.set(mx(b[0]), WT+0.014, b[1]); IT.add(ring);
      var core = new THREE.Mesh(new THREE.CylinderGeometry(0.026,0.026,0.005,18), M.steel);
      core.position.set(mx(b[0]), WT+0.015, b[1]); IT.add(core);
    });
  })();""",
    """  IT = item('Варочная панель', '🔥', 0.29, 0.26, gProps);
  (function(){
    var ct = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.013, 0.50), M.black);
    ct.position.set(mx(KX-0.31), WT+0.006, 1.05); IT.add(ct);
    [[KX-0.17,0.94],[KX-0.45,0.94],[KX-0.17,1.17],[KX-0.45,1.17]].forEach(function(b){
      var ring = new THREE.Mesh(new THREE.CylinderGeometry(0.072,0.072,0.004,24), M.dark);
      ring.position.set(mx(b[0]), WT+0.014, b[1]); IT.add(ring);
      var core = new THREE.Mesh(new THREE.CylinderGeometry(0.026,0.026,0.005,18), M.steel);
      core.position.set(mx(b[0]), WT+0.015, b[1]); IT.add(core);
    });
    [0.87,0.99,1.11,1.23].forEach(function(z){
      var k2 = new THREE.Mesh(new THREE.CylinderGeometry(0.015,0.015,0.022,12), M.black);
      k2.position.set(mx(KX-0.055), WT+0.011, z); IT.add(k2);
    });
  })();""")

# --- стол кухонный: +30 см, скруглённые края
rep("""  IT = item('Стол кухонный', '🪑', 0.45, 0.40);
  ibox(IT, 3.90, 1.70, 0.80, 0.70, 0.72, 0.76, M.wood);
  (function(){
    [[3.56,1.41],[4.24,1.41],[3.56,1.99],[4.24,1.99]].forEach(function(lg){
      ibox(IT, lg[0]+0.02, lg[1], 0.05, 0.05, 0, 0.72, M.woodDark);
    });
  })();""",
    """  IT = item('Стол кухонный', '🪑', 0.42, 0.52);
  (function(){
    var sh = new THREE.Shape();
    var w2 = 0.40, d2 = 0.50, r2 = 0.055;
    sh.moveTo(-w2+r2, -d2);
    sh.lineTo(w2-r2, -d2); sh.quadraticCurveTo(w2, -d2, w2, -d2+r2);
    sh.lineTo(w2, d2-r2); sh.quadraticCurveTo(w2, d2, w2-r2, d2);
    sh.lineTo(-w2+r2, d2); sh.quadraticCurveTo(-w2, d2, -w2, d2-r2);
    sh.lineTo(-w2, -d2+r2); sh.quadraticCurveTo(-w2, -d2, -w2+r2, -d2);
    var g2 = new THREE.ExtrudeGeometry(sh, { depth: 0.034, bevelEnabled: true,
      bevelSize: 0.006, bevelThickness: 0.006, bevelSegments: 2, curveSegments: 8 });
    var top = new THREE.Mesh(g2, M.wood);
    top.rotation.x = -Math.PI/2;
    top.position.set(mx(3.98), 0.72, 1.70);
    top.castShadow = top.receiveShadow = true; IT.add(top);
    [[3.64,1.31],[4.32,1.31],[3.64,2.09],[4.32,2.09]].forEach(function(lg){
      ibox(IT, lg[0], lg[1], 0.05, 0.05, 0, 0.72, M.woodDark);
    });
  })();""")

# --- табуреты: два, на четырёх ножках, светлые
rep("""  IT = item('Табурет кухонный', '🪑', 0.17, 0.17, gProps);
  ibox(IT, 4.42, 1.25, 0.32, 0.32, 0.42, 0.46, M.wood);
  ibox(IT, 4.42, 1.25, 0.06, 0.06, 0, 0.42, M.woodDark);""",
    """  function stool(cx, cz){
    var ITt = item('Табурет кухонный', '🪑', 0.17, 0.17, gProps);
    ibox(ITt, cx, cz, 0.32, 0.32, 0.42, 0.46, M.woodLight);
    [[cx-0.12, cz-0.12],[cx+0.12, cz-0.12],[cx-0.12, cz+0.12],[cx+0.12, cz+0.12]].forEach(function(lg){
      ibox(ITt, lg[0], lg[1], 0.038, 0.038, 0, 0.42, M.woodLight);
    });
  }
  stool(4.46, 1.42); stool(4.46, 1.98);""")

p.write_text(s, encoding='utf-8')
print('G4 ok')
