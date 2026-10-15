"""G7: кухня — ящики/холодильник открываются кликом, все фасады низа одинаковые,
гарнитур вплотную к стене (верх и низ), кран у плитки, обои на вентшахте,
разделочная доска удалена, фасад эркера — 3 створки; тени потолков (солнечное
пятно), табуреты от ножек стола, стиралка плоская с большим люком."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:120]
    s = s.replace(old, new, count)


# ---------- 1) система петель для ящиков и холодильника ----------
rep("var SOFAS = [], sofaParts = [];",
    "var SOFAS = [], sofaParts = [];\nvar HINGES = [], hingeParts = [];")
rep("  pickables = []; inv = []; held = -1; WIN_SASHES = []; SOFAS = []; sofaParts = [];",
    "  pickables = []; inv = []; held = -1; WIN_SASHES = []; SOFAS = []; sofaParts = [];\n  HINGES = []; hingeParts = [];")
rep("""function toggleSofa(so){
  so.open = !so.open;
  so.anim = { t:0, dur:0.9 };
  toast(so.open ? 'Разложил диван 🛏 — можно спать' : 'Сложил диван 🛋');
}""",
    """function toggleSofa(so){
  so.open = !so.open;
  so.anim = { t:0, dur:0.9 };
  toast(so.open ? 'Разложил диван 🛏 — можно спать' : 'Сложил диван 🛋');
}
/* петли: ящики гарнитура и дверца холодильника открываются кликом */
function mkHinge(panel, hx, hz, name, a1, parent){
  var grp = new THREE.Group();
  grp.position.set(hx, 0, hz);
  panel.position.x -= hx; panel.position.z -= hz;
  grp.add(panel);
  var h = { kind:'hinge', grp:grp, cur:0, a0:0, a1:(a1 === undefined ? -1.8 : a1),
            open:false, anim:null, name:name };
  panel.userData.hinge = h;
  HINGES.push(h); hingeParts.push(panel);
  (parent || gKitchen).add(grp);
  return h;
}
function toggleHinge(h){
  h.open = !h.open;
  h.anim = { t:0, dur:0.4, from:h.cur, to: h.open ? h.a1 : h.a0 };
  toast((h.open ? 'Открыл: ' : 'Закрыл: ') + (h.name || 'ящик'));
}""")
rep("""  SOFAS.forEach(function(so){
    if (!so.anim) return;
    so.anim.t = Math.min(1, so.anim.t + dt/so.anim.dur);
    var e2 = so.anim.t<0.5 ? 2*so.anim.t*so.anim.t : -1+(4-2*so.anim.t)*so.anim.t;
    var k2 = so.open ? e2 : 1-e2;
    so.seat.position.x = so.seatX0 + so.dir*0.64*k2;
    so.back.rotation.z = so.rot0 + (so.rot1 - so.rot0)*k2;
    if (so.anim.t >= 1) so.anim = null;
  });
}""",
    """  SOFAS.forEach(function(so){
    if (!so.anim) return;
    so.anim.t = Math.min(1, so.anim.t + dt/so.anim.dur);
    var e2 = so.anim.t<0.5 ? 2*so.anim.t*so.anim.t : -1+(4-2*so.anim.t)*so.anim.t;
    var k2 = so.open ? e2 : 1-e2;
    so.seat.position.x = so.seatX0 + so.dir*0.64*k2;
    so.back.rotation.z = so.rot0 + (so.rot1 - so.rot0)*k2;
    if (so.anim.t >= 1) so.anim = null;
  });
  HINGES.forEach(function(h){
    if (!h.anim) return;
    h.anim.t = Math.min(1, h.anim.t + dt/h.anim.dur);
    var e3 = h.anim.t<0.5 ? 2*h.anim.t*h.anim.t : -1+(4-2*h.anim.t)*h.anim.t;
    h.cur = h.anim.from + (h.anim.to - h.anim.from)*e3;
    h.grp.rotation.y = h.cur;
    if (h.anim.t >= 1) h.anim = null;
  });
}""")
rep("  var hits = raycaster.intersectObjects(doorLeaves.concat(sofaParts), false);\n  if (!hits.length) return null;\n  var u = hits[0].object.userData;\n  return u.door || u.sofa || null;",
    "  var hits = raycaster.intersectObjects(doorLeaves.concat(sofaParts, hingeParts), false);\n  if (!hits.length) return null;\n  var u = hits[0].object.userData;\n  return u.door || u.sofa || u.hinge || null;")
rep("  if (d && held < 0){ if (d.kind === 'sofa') toggleSofa(d); else toggleDoor(d); return; }",
    "  if (d && held < 0){ if (d.kind === 'sofa') toggleSofa(d); else if (d.kind === 'hinge') toggleHinge(d); else toggleDoor(d); return; }")
rep("""    var d = doorUnder(0, 0);
    if (d && held < 0){ if (d.kind === 'sofa') toggleSofa(d); else toggleDoor(d); return; }
    var g = itemUnder(0, 0);
    if (g) pickUp(g);
  } else if (e.button === 2){
    var d2 = doorUnder(0, 0);
    if (d2){ if (d2.kind === 'sofa') toggleSofa(d2); else toggleDoor(d2); return; }
    placeHeld(0, 0);
  }""",
    """    var d = doorUnder(0, 0);
    if (d && held < 0){ if (d.kind === 'sofa') toggleSofa(d); else if (d.kind === 'hinge') toggleHinge(d); else toggleDoor(d); return; }
    var g = itemUnder(0, 0);
    if (g) pickUp(g);
  } else if (e.button === 2){
    var d2 = doorUnder(0, 0);
    if (d2){ if (d2.kind === 'sofa') toggleSofa(d2); else if (d2.kind === 'hinge') toggleHinge(d2); else toggleDoor(d2); return; }
    placeHeld(0, 0);
  }""")
rep("    if (q.userData && q.userData.sofa) return 'Диван (раскладной)';",
    "    if (q.userData && q.userData.sofa) return 'Диван (раскладной)';\n    if (q.userData && q.userData.hinge) return 'Дверца/ящик';")

# ---------- 2) гарнитур: вплотную к стене, все фасады равные, петли ----------
rep("  solidBox(KX-0.60, KX-0.01, 0.50, 2.90, BASE, BASE+LOWH, { nx:M.carcass, side:M.carcass }, 1, ITcnt);",
    "  solidBox(KX-0.60, KX-0.01, 0.50, 2.99, BASE, BASE+LOWH, { nx:M.carcass, side:M.carcass }, 1, ITcnt);")
rep("  solidBox(KX-0.60, KX-0.01, 0.50, 2.90, 0, BASE, { side:M.dark }, 1, ITcnt);",
    "  solidBox(KX-0.60, KX-0.01, 0.50, 2.99, 0, BASE, { side:M.dark }, 1, ITcnt);")
rep("  var ITwt = item('Столешница', '▭', 0.31, 1.22, gKitchen);",
    "  var ITwt = item('Столешница', '▭', 0.31, 1.27, gKitchen);")
rep("""  var wt1 = new THREE.Mesh(new THREE.BoxGeometry(0.62, WT_T, 2.46), M.work);
  fixBoxUV(wt1.geometry, 0.62, WT_T, 2.46, 1); wt1.position.set(mx(KX-0.31), WT-WT_T/2, 1.70); wt1.castShadow = wt1.receiveShadow = true; ITwt.add(wt1);
  /* фасады низа: 5 по восточной стене + угловой + ½ */
  doorsGrp = new THREE.Group();
  function front(x, y, z, w, h){
    var m = new THREE.Mesh(new THREE.BoxGeometry(0.02, h, w), M.front);
    m.position.set(mx(x), y, z); m.castShadow = m.receiveShadow = true;
    doorsGrp.add(m); return m;
  }
  for (var i2=0;i2<4;i2++){
    var z2 = 0.50 + FW/2 + i2*FW;
    front(KX-0.61, BASE+LOWH/2, z2, FW-0.02, LOWH-0.04);
    var h2 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.02, 0.13), M.handleOld);
    h2.position.set(mx(KX-0.63), BASE+LOWH-0.10, z2); h2.castShadow = true; handles.push(h2); doorsGrp.add(h2);
  }
  front(KX-0.61, BASE+LOWH/2, 2.74, 0.30, LOWH-0.04);
  var h4 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.02, 0.11), M.handleOld);
  h4.position.set(mx(KX-0.63), BASE+LOWH-0.10, 2.74); h4.castShadow = true; handles.push(h4); doorsGrp.add(h4);
  gKitchen.add(doorsGrp);""",
    """  var wt1 = new THREE.Mesh(new THREE.BoxGeometry(0.62, WT_T, 2.49), M.work);
  fixBoxUV(wt1.geometry, 0.62, WT_T, 2.49, 1); wt1.position.set(mx(KX-0.31), WT-WT_T/2, 1.745); wt1.castShadow = wt1.receiveShadow = true; ITwt.add(wt1);
  /* фасады низа: 4 одинаковых, все открываются кликом (петли) */
  doorsGrp = new THREE.Group();
  var LWD = (2.99 - 0.50) / 4;
  for (var i2=0;i2<4;i2++){
    var z2 = 0.50 + LWD/2 + i2*LWD;
    var pd = new THREE.Mesh(new THREE.BoxGeometry(0.02, LOWH-0.04, LWD-0.02), M.front);
    pd.position.set(mx(KX-0.61), BASE+LOWH/2, z2); pd.castShadow = pd.receiveShadow = true;
    var hd = mkHinge(pd, mx(KX-0.61), z2 - (LWD-0.02)/2 + 0.01, 'ящик', -1.8, doorsGrp);
    var h2 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.02, 0.13), M.handleOld);
    h2.position.set(-0.025, BASE+LOWH-0.10, LWD-0.02-0.075);
    h2.castShadow = true; handles.push(h2); hd.grp.add(h2);
  }
  gKitchen.add(doorsGrp);""")
rep("""    var t1 = new THREE.Mesh(new THREE.BoxGeometry(0.02, bsH, 2.40), M.tile);
    fixBoxUV(t1.geometry, 0.02, bsH, 2.40, 1.65);
    t1.position.set(mx(KX-0.02), WT+bsH/2, 1.70); t1.receiveShadow = true; gKitchen.add(t1);""",
    """    var t1 = new THREE.Mesh(new THREE.BoxGeometry(0.02, bsH, 2.49), M.tile);
    fixBoxUV(t1.geometry, 0.02, bsH, 2.49, 1.65);
    t1.position.set(mx(KX-0.02), WT+bsH/2, 1.745); t1.receiveShadow = true; gKitchen.add(t1);""")
rep("""  /* верхние шкафы: 4 фасада */
  upGrp = new THREE.Group();
  var up = new THREE.Mesh(new THREE.BoxGeometry(0.34, UPH, 2.08), M.carcass);
  up.position.set(mx(KX-0.17), WT+AH+UPH/2, 1.70); up.castShadow = up.receiveShadow = true; upGrp.add(up);
  for (var i3=0;i3<4;i3++){
    var uz = 0.66 + FW/2 + i3*FW;
    var d2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH-0.04, FW-0.02), M.front);
    d2.position.set(mx(KX-0.35), WT+AH+UPH/2, uz); d2.castShadow = true; upGrp.add(d2);
    var uh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
    uh.position.set(mx(KX-0.37), WT+AH+UPH/2-(UPH/2)+0.09, uz+FW/2-0.045); uh.castShadow = true; handles.push(uh); upGrp.add(uh);
  }
  boxCol(KX-0.36, 0.66, KX, 2.74);
  gKitchen.add(upGrp);""",
    """  /* верхние шкафы: 4 одинаковых фасада до самой стены, тоже открываются */
  upGrp = new THREE.Group();
  var up = new THREE.Mesh(new THREE.BoxGeometry(0.34, UPH, 2.33), M.carcass);
  up.position.set(mx(KX-0.17), WT+AH+UPH/2, 1.825); up.castShadow = up.receiveShadow = true; upGrp.add(up);
  var UZD = (2.99 - 0.66) / 4;
  for (var i3=0;i3<4;i3++){
    var uz = 0.66 + UZD/2 + i3*UZD;
    var d2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH-0.04, UZD-0.02), M.front);
    d2.position.set(mx(KX-0.35), WT+AH+UPH/2, uz); d2.castShadow = d2.receiveShadow = true;
    var hu = mkHinge(d2, mx(KX-0.35), uz - (UZD-0.02)/2 + 0.01, 'шкафчик', -1.8, upGrp);
    var uh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
    uh.position.set(-0.025, WT+AH+UPH/2-(UPH/2)+0.09, UZD-0.02-0.055);
    uh.castShadow = true; handles.push(uh); hu.grp.add(uh);
  }
  boxCol(KX-0.36, 0.66, KX, 2.99);
  gKitchen.add(upGrp);""")
rep("  tape('x',[KX-0.04, WT+bsH, 0.50],[KX-0.04, WT+bsH, 2.90], 0.05);",
    "  tape('x',[KX-0.04, WT+bsH, 0.50],[KX-0.04, WT+bsH, 2.99], 0.05);")
rep("""  filmW = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.008, 2.40), M.film);
  filmW.position.set(mx(KX-0.30), WT+0.006, 1.70); gTape.add(filmW);""",
    """  filmW = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.008, 2.49), M.film);
  filmW.position.set(mx(KX-0.30), WT+0.006, 1.745); gTape.add(filmW);""")

# ---------- 3) вентшахта — обои как у стены ----------
rep("  ventMesh = solidBox(6.07, 6.47, 0.06, 0.46, 0, P.HC, { px:M.concrete, nx:null, pz:M.concrete, nz:null, staged:['nx','nz'] });",
    "  ventMesh = solidBox(6.07, 6.47, 0.06, 0.46, 0, P.HC, { px:M.concrete, nx:null, pz:null, nz:null, staged:['nx','nz','pz'] });")

# ---------- 4) мойка: кран у плитки (фон), а не сбоку ----------
rep("""    cyl(0.022,0.026,0.05, M.chrome, KX-0.31, WT+0.025, 2.70);
    cyl(0.015,0.015,0.26, M.chrome, KX-0.31, WT+0.16, 2.70);
    cyl(0.013,0.013,0.20, M.chrome, KX-0.31, WT+0.29, 2.59, Math.PI/2);""",
    """    cyl(0.022,0.026,0.05, M.chrome, KX-0.07, WT+0.025, 2.44);
    cyl(0.015,0.015,0.26, M.chrome, KX-0.07, WT+0.16, 2.44);
    cyl(0.013,0.013,0.20, M.chrome, KX-0.17, WT+0.29, 2.44, null, Math.PI/2);""")

# ---------- 5) табуреты — не в ножках стола ----------
rep("  stool(4.46, 1.42); stool(4.46, 1.98);",
    "  stool(4.62, 1.42); stool(4.62, 1.98);")

# ---------- 6) разделочная доска — убрать ----------
rep("""  IT = item('Разделочная доска', '🪵', 0, 0, gProps);
  (function(){ var bd = new THREE.Mesh(new THREE.BoxGeometry(0.016, 0.23, 0.32), M.wood);
    bd.position.set(mx(KX-0.10), WT+0.115, 0.62); bd.rotation.z = 0.13;
    bd.castShadow = true; IT.add(bd); })();
""", "")

# ---------- 7) эркер: три створки (не одна широкая) ----------
rep("    var parts = [ [1.00, 0.00], [0.70, 1.00] ];",
    "    var parts = [ [0.50, 0.00], [0.50, 0.50], [0.70, 1.00] ];")

# ---------- 8) холодильник: дверца открывается ----------
rep("""  IT = item('Холодильник', '🧊', 0.31, 0.33);
  ibox(IT, 3.89, 0.62, 0.60, 0.64, 0, 1.85, M.white);
  (function(){
    var ln = new THREE.Mesh(new THREE.BoxGeometry(0.02, 1.60, 0.02), M.steel);
    ln.position.set(mx(4.19), 1.05, 0.62); IT.add(ln);
    var hh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.30, 0.03), M.steel);
    hh.position.set(mx(4.20), 1.55, 0.44); IT.add(hh);
  })();""",
    """  IT = item('Холодильник', '🧊', 0.31, 0.33);
  ibox(IT, 3.89, 0.62, 0.60, 0.64, 0, 1.85, M.white);
  (function(){
    var door2 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 1.80, 0.62), M.white);
    door2.position.set(mx(4.205), 0.93, 0.62); door2.castShadow = door2.receiveShadow = true;
    var fh = mkHinge(door2, mx(4.205), 0.32, 'холодильник', 1.9, IT);
    var ln = new THREE.Mesh(new THREE.BoxGeometry(0.02, 1.60, 0.02), M.steel);
    ln.position.set(0.018, 1.05, 0.30); fh.grp.add(ln);
    var hh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.30, 0.03), M.steel);
    hh.position.set(0.02, 1.55, 0.12); fh.grp.add(hh);
  })();""")

# ---------- 9) стиралка: плоская, люк большой ----------
rep("""  IT = item('Стиральная машинка', '🧺', 0.30, 0.30);
  ibox(IT, 4.82, 3.52, 0.60, 0.60, 0, 0.85, M.white);
  (function(){ var dr = new THREE.Mesh(new THREE.CylinderGeometry(0.17,0.17,0.02,20), M.dark);
    dr.rotation.x = Math.PI/2; dr.position.set(mx(4.82), 0.45, 3.83); IT.add(dr); })();""",
    """  IT = item('Стиральная машинка', '🧺', 0.30, 0.24);
  ibox(IT, 4.82, 3.44, 0.60, 0.44, 0, 0.85, M.white);
  (function(){ var dr = new THREE.Mesh(new THREE.CylinderGeometry(0.21,0.21,0.03,22), M.dark);
    dr.rotation.x = Math.PI/2; dr.position.set(mx(4.82), 0.44, 3.67); IT.add(dr);
    var rim2 = new THREE.Mesh(new THREE.CylinderGeometry(0.235,0.235,0.015,24), M.steel);
    rim2.rotation.x = Math.PI/2; rim2.position.set(mx(4.82), 0.44, 3.665); IT.add(rim2); })();""")

# ---------- 10) тумбы низа/столешница: коллайдер по новой длине ----------
rep("  var ITcnt = item('Тумба низ', '🗄', 0.30, 1.20, gKitchen);",
    "  var ITcnt = item('Тумба низ', '🗄', 0.30, 1.27, gKitchen);")

# ---------- 11) солнце сквозь потолки — тени двухсторонние ----------
rep("""    var m = new THREE.Mesh(g, M.ceil);
    m.position.set((x0+x1)/2, P.HC, (r.z0+r.z1)/2); gRoom.add(m);
  }""",
    """    var m = new THREE.Mesh(g, M.ceil);
    m.castShadow = true;                      /* пусть потолок держит солнце */
    m.position.set((x0+x1)/2, P.HC, (r.z0+r.z1)/2); gRoom.add(m);
  }""")
rep("  glass:     new THREE.MeshStandardMaterial({ color:0xdfeef4, roughness:.08, metalness:.1, transparent:true, opacity:.16 }),",
    "  glass:     new THREE.MeshStandardMaterial({ color:0xdfeef4, roughness:.08, metalness:.1, transparent:true, opacity:.16 }),\n  /* потолки: тень с двух сторон, лицевая — одна (дом сверху видно) */")
rep("  hole:      new THREE.MeshBasicMaterial({ color:0x8d8578 })\n};",
    "  hole:      new THREE.MeshBasicMaterial({ color:0x8d8578 })\n};\nM.ceil.shadowSide = THREE.DoubleSide;\nM.ceilB.shadowSide = THREE.DoubleSide;")

p.write_text(s, encoding='utf-8')
print('G7 ok')
