"""G3: санузел — раковина без тумбы (зеркало над ней по росту), машинку и унитаз
местами, ванна с настоящей выемкой; коридорное зеркало удалено, в мини-коридоре
зеркало и комод."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:120]
    s = s.replace(old, new, count)


# --- зеркало в коридоре: удалить, вместо него зеркало + комод в мини-коридоре
rep("""  /* коридор: зеркало на стене */
  IT = item('Зеркало в коридоре', '🪞', 0, 0);
  (function(){
    var mirr = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 1.2), M.glass);
    mirr.rotation.y = faceRY(Math.PI/2); mirr.position.set(mx(4.435), 1.55, 4.75); IT.add(mirr);
    var fr = new THREE.Mesh(new THREE.BoxGeometry(0.02, 1.24, 0.54), M.woodDark);
    fr.position.set(mx(4.425), 1.55, 4.75); IT.add(fr);
  })();""",
    """  /* мини-коридор у входа: зеркало на западной стене + комод */
  IT = item('Зеркало', '🪞', 0, 0);
  (function(){
    var mirr = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 1.2), M.glass);
    mirr.rotation.y = faceRY(Math.PI/2); mirr.position.set(mx(3.575), 1.45, 5.90); IT.add(mirr);
    var fr = new THREE.Mesh(new THREE.BoxGeometry(0.02, 1.24, 0.54), M.woodDark);
    fr.position.set(mx(3.565), 1.45, 5.90); IT.add(fr);
  })();
  IT = item('Комод', '🗄', 0.15, 0.23);
  ibox(IT, 4.28, 5.97, 0.28, 0.45, 0, 0.85, M.wood);
  for (var ci=0; ci<3; ci++){
    ibox(IT, 4.132, 5.97, 0.012, 0.40, 0.10+ci*0.25, 0.30+ci*0.25, M.woodDark);
    ibox(IT, 4.124, 5.97, 0.012, 0.10, 0.205+ci*0.25, 0.235+ci*0.25, M.steel);
  }""")

# --- ванна: настоящая выемка (борта + дно), больше не «закрытая коробка»
rep("""  IT = item('Ванна', '🛁', 0.85, 0.35);
  ibox(IT, 5.48, 5.17, 1.66, 0.70, 0, 0.55, M.white);
  ibox(IT, 5.48, 5.17, 1.52, 0.56, 0.55, 0.65, M.fabric2);""",
    """  IT = item('Ванна', '🛁', 0.85, 0.35);
  ibox(IT, 5.48, 5.17, 1.66, 0.70, 0, 0.13, M.white);              /* дно */
  ibox(IT, 5.48, 4.865, 1.66, 0.09, 0.13, 0.55, M.white);          /* борт север */
  ibox(IT, 5.48, 5.475, 1.66, 0.09, 0.13, 0.55, M.white);          /* борт юг */
  ibox(IT, 4.695, 5.17, 0.09, 0.70, 0.13, 0.55, M.white);          /* борт запад */
  ibox(IT, 6.265, 5.17, 0.09, 0.70, 0.13, 0.55, M.white);          /* борт восток */
  (function(){
    var wtr = new THREE.Mesh(new THREE.PlaneGeometry(1.42, 0.50), M.bathFloor);
    wtr.geometry.rotateX(-Math.PI/2);
    wtr.position.set(mx(5.48), 0.135, 5.17); wtr.receiveShadow = true; IT.add(wtr);
  })();""")

# --- унитаз и стиральная машинка местами
rep("""  IT = item('Унитаз', '🚽', 0.19, 0.28);
  ibox(IT, 4.82, 3.45, 0.38, 0.56, 0, 0.40, M.white);
  ibox(IT, 4.82, 3.24, 0.38, 0.18, 0.40, 0.78, M.white);
  IT = item('Стиральная машинка', '🧺', 0.30, 0.30);
  ibox(IT, 5.42, 3.52, 0.60, 0.60, 0, 0.85, M.white);
  (function(){ var dr = new THREE.Mesh(new THREE.CylinderGeometry(0.17,0.17,0.02,20), M.dark);
    dr.rotation.x = Math.PI/2; dr.position.set(mx(5.42), 0.45, 3.83); IT.add(dr); })();""",
    """  IT = item('Унитаз', '🚽', 0.19, 0.28);
  ibox(IT, 5.42, 3.45, 0.38, 0.56, 0, 0.40, M.white);
  ibox(IT, 5.42, 3.24, 0.38, 0.18, 0.40, 0.78, M.white);
  IT = item('Стиральная машинка', '🧺', 0.30, 0.30);
  ibox(IT, 4.82, 3.52, 0.60, 0.60, 0, 0.85, M.white);
  (function(){ var dr = new THREE.Mesh(new THREE.CylinderGeometry(0.17,0.17,0.02,20), M.dark);
    dr.rotation.x = Math.PI/2; dr.position.set(mx(4.82), 0.45, 3.83); IT.add(dr); })();""")

# --- раковина: убрать тумбу, зеркало над ней уже по росту
rep("""  IT = item('Раковина', '🚰', 0.28, 0.21);
  ibox(IT, 6.18, 4.20, 0.54, 0.42, 0.70, 0.82, M.white);
  ibox(IT, 6.18, 4.20, 0.48, 0.36, 0, 0.70, M.fabric2);""",
    """  IT = item('Раковина', '🚰', 0.28, 0.21);
  ibox(IT, 6.18, 4.20, 0.54, 0.42, 0.70, 0.82, M.white);
  (function(){
    var bw = new THREE.Mesh(new THREE.PlaneGeometry(0.46, 0.34), M.dark);
    bw.geometry.rotateX(-Math.PI/2); bw.position.set(mx(6.18), 0.826, 4.20); IT.add(bw);
    var sf = new THREE.Mesh(new THREE.CylinderGeometry(0.014,0.014,0.17,12), M.chrome);
    sf.position.set(mx(6.36), 0.90, 4.20); IT.add(sf);
    var sn = new THREE.Mesh(new THREE.CylinderGeometry(0.011,0.011,0.14,12), M.chrome);
    sn.rotation.z = Math.PI/2; sn.position.set(mx(6.30), 0.985, 4.20); IT.add(sn);
  })();""")

p.write_text(s, encoding='utf-8')
print('G3 ok')
