"""I1: коридор +30 см (перегородка санузла на восток, санузел перекомпонован),
входная дверь по центру (4,74), комод в 2 раза шире + вешалка над ним, белая полка
на западной стене, люстра в центр коридора, зеркало на стену санузла,
полы — без «дурки» (стык ламината)."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    s = s.replace(old, new, count)


# --- план: коридор шире на 30 см
rep("  hall:  { x0:3.57, x1:4.45, z0:3.16, z1:7.44 },",
    "  hall:  { x0:3.57, x1:4.75, z0:3.16, z1:7.44 },")
rep("  bath:  { x0:4.53, x1:6.47, z0:3.16, z1:5.52 },",
    "  bath:  { x0:4.83, x1:6.47, z0:3.16, z1:5.52 },")
# входная дверь по центру (4,74)
rep("    ent:  { x0:3.62, x1:4.52, h:2.10 }",
    "    ent:  { x0:4.29, x1:5.19, h:2.10 }")

# --- полы: стык ламинат/ламинат без щели и наложений
rep("  floorBox({ x0:HA.x0, x1:4.41, z0:HA.z0, z1:HA.z1 }, M.lam, 0.5);",
    "  floorBox({ x0:HA.x0, x1:4.71, z0:HA.z0, z1:HA.z1 }, M.lam, 0.5);")
rep("  floorBox({ x0:4.57, x1:BA.x1, z0:BA.z0, z1:BA.z1 }, M.bathFloor, 4);",
    "  floorBox({ x0:4.87, x1:BA.x1, z0:BA.z0, z1:BA.z1 }, M.bathFloor, 4);")
rep("  floorBox({ x0:4.61, x1:6.47, z0:5.60, z1:7.44 }, M.lam, 0.5);   /* коридор за санузлом */",
    "  floorBox({ x0:4.87, x1:6.47, z0:5.60, z1:7.44 }, M.lam, 0.5);   /* коридор за санузлом */")

# --- санузел: ванна уже (1,50), машинка и унитаз переставлены под новую ширину
rep("  IT = item('Ванна', '🛁', 0.85, 0.35);\n  ibox(IT, 5.48, 5.17, 1.66, 0.70, 0, 0.13, M.white);              /* дно */\n  ibox(IT, 5.48, 4.865, 1.66, 0.09, 0.13, 0.55, M.white);          /* борт север */\n  ibox(IT, 5.48, 5.475, 1.66, 0.09, 0.13, 0.55, M.white);          /* борт юг */\n  ibox(IT, 4.695, 5.17, 0.09, 0.70, 0.13, 0.55, M.white);          /* борт запад */\n  ibox(IT, 6.265, 5.17, 0.09, 0.70, 0.13, 0.55, M.white);          /* борт восток */",
    "  IT = item('Ванна', '🛁', 0.78, 0.35);\n  ibox(IT, 5.70, 5.17, 1.50, 0.70, 0, 0.13, M.white);              /* дно */\n  ibox(IT, 5.70, 4.865, 1.50, 0.09, 0.13, 0.55, M.white);          /* борт север */\n  ibox(IT, 5.70, 5.475, 1.50, 0.09, 0.13, 0.55, M.white);          /* борт юг */\n  ibox(IT, 4.995, 5.17, 0.09, 0.70, 0.13, 0.55, M.white);          /* борт запад */\n  ibox(IT, 6.405, 5.17, 0.09, 0.70, 0.13, 0.55, M.white);          /* борт восток */")
rep("    var wtr = new THREE.Mesh(new THREE.PlaneGeometry(1.42, 0.50), M.bathFloor);\n    wtr.geometry.rotateX(-Math.PI/2);\n    wtr.position.set(mx(5.48), 0.135, 5.17); wtr.receiveShadow = true; IT.add(wtr);",
    "    var wtr = new THREE.Mesh(new THREE.PlaneGeometry(1.26, 0.50), M.bathFloor);\n    wtr.geometry.rotateX(-Math.PI/2);\n    wtr.position.set(mx(5.70), 0.135, 5.17); wtr.receiveShadow = true; IT.add(wtr);")
rep("""  IT = item('Унитаз', '🚽', 0.19, 0.28);
  ibox(IT, 5.42, 3.45, 0.38, 0.56, 0, 0.40, M.white);
  ibox(IT, 5.42, 3.24, 0.38, 0.18, 0.40, 0.78, M.white);""",
    """  IT = item('Унитаз', '🚽', 0.19, 0.28);
  ibox(IT, 5.95, 3.45, 0.38, 0.56, 0, 0.40, M.white);
  ibox(IT, 5.95, 3.24, 0.38, 0.18, 0.40, 0.78, M.white);""")
rep("""  IT = item('Стиральная машинка', '🧺', 0.30, 0.24);
  ibox(IT, 4.82, 3.44, 0.60, 0.44, 0, 0.85, M.white);
  (function(){ var dr = new THREE.Mesh(new THREE.CylinderGeometry(0.21,0.21,0.03,22), M.dark);
    dr.rotation.x = Math.PI/2; dr.position.set(mx(4.82), 0.44, 3.67); IT.add(dr);
    var rim2 = new THREE.Mesh(new THREE.CylinderGeometry(0.235,0.235,0.015,24), M.steel);
    rim2.rotation.x = Math.PI/2; rim2.position.set(mx(4.82), 0.44, 3.665); IT.add(rim2); })();""",
    """  IT = item('Стиральная машинка', '🧺', 0.30, 0.24);
  ibox(IT, 5.16, 3.44, 0.60, 0.44, 0, 0.85, M.white);
  (function(){ var dr = new THREE.Mesh(new THREE.CylinderGeometry(0.21,0.21,0.03,22), M.dark);
    dr.rotation.x = Math.PI/2; dr.position.set(mx(5.16), 0.44, 3.67); IT.add(dr);
    var rim2 = new THREE.Mesh(new THREE.CylinderGeometry(0.235,0.235,0.015,24), M.steel);
    rim2.rotation.x = Math.PI/2; rim2.position.set(mx(5.16), 0.44, 3.665); IT.add(rim2); })();""")
# вода в ванне — уже
rep("    var wl = new THREE.Mesh(new THREE.PlaneGeometry(1.44, 0.48), M.water);\n    wl.geometry.rotateX(-Math.PI/2); wl.position.set(mx(5.48), 0.15, 5.17); wl.visible = false; gRoom.add(wl);",
    "    var wl = new THREE.Mesh(new THREE.PlaneGeometry(1.30, 0.48), M.water);\n    wl.geometry.rotateX(-Math.PI/2); wl.position.set(mx(5.70), 0.15, 5.17); wl.visible = false; gRoom.add(wl);")

# --- комод в 2 раза шире и на новое место + вешалка над ним
rep("""  IT = item('Комод', '🗄', 0.13, 0.24);
  ibox(IT, 6.32, 6.56, 0.26, 0.48, 0, 0.85, M.wood);
  for (var ci=0; ci<3; ci++){
    ibox(IT, 6.178, 6.56, 0.012, 0.42, 0.10+ci*0.25, 0.30+ci*0.25, M.woodDark);
    ibox(IT, 6.17, 6.56, 0.012, 0.10, 0.205+ci*0.25, 0.235+ci*0.25, M.steel);
  }""",
    """  IT = item('Комод', '🗄', 0.13, 0.50);
  ibox(IT, 6.34, 6.86, 0.26, 0.96, 0, 0.85, M.wood);
  for (var ci=0; ci<3; ci++){
    ibox(IT, 6.198, 6.86, 0.012, 0.90, 0.10+ci*0.25, 0.30+ci*0.25, M.woodDark);
    ibox(IT, 6.19, 6.86, 0.012, 0.14, 0.205+ci*0.25, 0.235+ci*0.25, M.steel);
  }
  /* вешалка над комодом */
  (function(){
    var bar = new THREE.Mesh(new THREE.CylinderGeometry(0.012,0.012,0.90,10), M.chrome);
    bar.rotation.x = Math.PI/2; bar.position.set(mx(6.42), 1.72, 6.86); gRoom.add(bar);
    [6.46, 6.86, 7.26].forEach(function(zz){
      var hk = new THREE.Mesh(new THREE.TorusGeometry(0.025, 0.006, 8, 14, Math.PI), M.chrome);
      hk.rotation.y = Math.PI/2; hk.position.set(mx(6.42), 1.72, zz); gRoom.add(hk);
    });
    var br = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.03, 0.03), M.chrome);
    br.position.set(mx(6.45), 1.72, 6.42); gRoom.add(br);
    var br2 = br.clone(); br2.position.z = 7.30; gRoom.add(br2);
  })();
  /* белая полка на западной стене коридора */
  IT = item('Полка', '🗄', 0.18, 0.36);
  ibox(IT, 3.77, 6.85, 0.34, 0.70, 0.76, 0.80, M.white);
  ibox(IT, 3.77, 6.85, 0.34, 0.70, 0.36, 0.40, M.white);
  ibox(IT, 3.77, 6.85, 0.34, 0.70, 0, 0.04, M.white);
  ibox(IT, 3.77, 6.51, 0.34, 0.02, 0.04, 0.80, M.white);
  ibox(IT, 3.77, 7.19, 0.34, 0.02, 0.04, 0.80, M.white);""")

# --- люстра коридора — в центр (4,20 · 6,69)
rep("""  var corLight = new THREE.PointLight(0xffe8c0, 0.0, 7, 2);
  corLight.position.set(mx(4.45), 2.30, 5.73); gRoom.add(corLight);
  (function(){
    var bx = mx(4.45);""",
    """  var corLight = new THREE.PointLight(0xffe8c0, 0.0, 7, 2);
  corLight.position.set(mx(4.20), 2.30, 6.69); gRoom.add(corLight);
  (function(){
    var bx = mx(4.20);""")
rep("""    base.position.set(bx, P.HC-0.018, 5.73); gRoom.add(base);
    var bar = new THREE.Mesh(new THREE.BoxGeometry(0.64, 0.02, 0.02), M.chrome);
    bar.position.set(bx, P.HC-0.09, 5.73); gRoom.add(bar);
    [-0.24, 0, 0.24].forEach(function(dx){
      var hook = new THREE.Mesh(new THREE.TorusGeometry(0.045, 0.007, 8, 16, Math.PI*1.2), M.chrome);
      hook.rotation.y = Math.PI/2; hook.position.set(bx+dx, P.HC-0.135, 5.73); gRoom.add(hook);
      var cup = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.04, 0.11, 16, 1, true), M.lampGlass);
      cup.position.set(bx+dx, P.HC-0.245, 5.73); gRoom.add(cup);
      var bulb = new THREE.Mesh(new THREE.SphereGeometry(0.034, 12, 10), M.bulb);
      bulb.position.set(bx+dx, P.HC-0.285, 5.73); gRoom.add(bulb);
    });
  })();""",
    """    base.position.set(bx, P.HC-0.018, 6.69); gRoom.add(base);
    var bar = new THREE.Mesh(new THREE.BoxGeometry(0.64, 0.02, 0.02), M.chrome);
    bar.position.set(bx, P.HC-0.09, 6.69); gRoom.add(bar);
    [-0.24, 0, 0.24].forEach(function(dx){
      var hook = new THREE.Mesh(new THREE.TorusGeometry(0.045, 0.007, 8, 16, Math.PI*1.2), M.chrome);
      hook.rotation.y = Math.PI/2; hook.position.set(bx+dx, P.HC-0.135, 6.69); gRoom.add(hook);
      var cup = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.04, 0.11, 16, 1, true), M.lampGlass);
      cup.position.set(bx+dx, P.HC-0.245, 6.69); gRoom.add(cup);
      var bulb = new THREE.Mesh(new THREE.SphereGeometry(0.034, 12, 10), M.bulb);
      bulb.position.set(bx+dx, P.HC-0.285, 6.69); gRoom.add(bulb);
    });
  })();""")

# --- зеркало — на стену санузла (лицом на юг, в коридор)
rep("""    var mirr = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 1.2), M.mirror);
    mirr.rotation.y = faceRY(Math.PI/2); mirr.position.set(mx(3.581), 1.45, 5.90); IT.add(mirr);
    var fr = new THREE.Mesh(new THREE.BoxGeometry(0.02, 1.24, 0.54), M.woodDark);
    fr.position.set(mx(3.565), 1.45, 5.90); IT.add(fr);""",
    """    var mirr = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 1.2), M.mirror);
    mirr.rotation.y = faceRY(0); mirr.position.set(mx(5.21), 1.45, 5.682); IT.add(mirr);
    var fr = new THREE.Mesh(new THREE.BoxGeometry(0.54, 1.24, 0.02), M.woodDark);
    fr.position.set(mx(5.21), 1.45, 5.668); IT.add(fr);""")

# --- подписи входа по новой двери
rep("  entrance: [ [4.05, 1.55, 8.30],        [0,0,-1] ]",
    "  entrance: [ [4.74, 1.55, 8.30],        [0,0,-1] ]")
rep("  { p:[4.05, 1.55, 8.45], t:'площадка · стена · кв. 278' }",
    "  { p:[4.74, 1.55, 8.45], t:'площадка · стена · кв. 278' }")

p.write_text(s, encoding='utf-8')
print('I1 ok')

# data.json: спавн/телепорты под новую дверь
d = pathlib.Path('_tools/data.json')
t = d.read_text(encoding='utf-8')
t = t.replace('"x": 4.2,\n      "z": 8.3,', '"x": 4.74,\n      "z": 8.3,', 1)
d.write_text(t, encoding='utf-8')
import json; json.loads(t)
print('I1 data ok')
