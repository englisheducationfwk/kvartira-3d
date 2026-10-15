"""K1: пожарная кнопка — красная квадратная как в РФ (с текстурой «ПОЖАР») и после
выключателя; дверь соседа убрать; двери не проходят сквозь стены (петли подтянуты);
низ разрезного ящика убрать (обратно целая дверца); площадка без щелей под стенами."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    s = s.replace(old, new, count)


# --- текстура пожарной кнопки (красная квадратная, как в РФ) ---
rep("var M = {",
    """var texFire = ctex(128, 128, function(g,w,h){
  g.fillStyle = '#b32a1c'; g.fillRect(0, 0, w, h);
  g.strokeStyle = '#8f1f14'; g.lineWidth = 8; g.strokeRect(4, 4, w-8, h-8);
  g.fillStyle = '#d74836'; g.beginPath(); g.arc(64, 54, 26, 0, 6.29); g.fill();
  g.strokeStyle = '#e8b0a6'; g.lineWidth = 3; g.beginPath(); g.arc(64, 54, 26, 0, 6.29); g.stroke();
  g.fillStyle = '#ffffff'; g.font = 'bold 20px Arial'; g.textAlign = 'center';
  g.fillText('ПОЖАР', 64, 96);
  g.fillStyle = '#f2d9d4'; g.fillRect(24, 108, 80, 8);
});
var M = {""")
rep("  redBtn:    new THREE.MeshStandardMaterial({ color:0xcc2a1e, roughness:.45 }),",
    """  redBtn:    new THREE.MeshStandardMaterial({ color:0xcc2a1e, roughness:.45 }),
  fire:      new THREE.MeshStandardMaterial({ map:texFire, roughness:.5 }),""")

# --- пожарная кнопка: квадратная красная, после выключателя (5,62), прижата к стене ---
rep("""  (function(){
    var bx = mx(5.07);
    var pl = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.11, 0.016), M.frame);
    pl.position.set(bx, 1.54, HA.z1-0.012); gRoom.add(pl);
    var btn = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.032, 0.02, 16), M.redBtn);
    btn.rotation.x = Math.PI/2; btn.position.set(bx, 1.54, HA.z1-0.027); gRoom.add(btn);
  })();""",
    """  (function(){
    var bx = mx(5.62);
    var fw = new THREE.Mesh(new THREE.BoxGeometry(0.17, 0.17, 0.03),
      [M.redBtn, M.redBtn, M.redBtn, M.redBtn, M.fire, M.redBtn]);
    fixBoxUV(fw.geometry, 0.17, 0.17, 0.03, 1);
    fw.position.set(bx, 1.52, HA.z1-0.017); fw.castShadow = true; gRoom.add(fw);
    var pl = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.20, 0.012), M.frame);
    pl.position.set(bx, 1.52, HA.z1-0.007); gRoom.add(pl);
  })();""")

# --- дверь соседа — убрать ---
rep("""    /* просто стены (лифты убраны по отметке) + дверь соседа на западной стене */
    (function(){
      var nf = new THREE.Mesh(new THREE.BoxGeometry(0.05, 2.14, 1.00), M.frame);
      nf.position.set(L0+0.015, 1.07, 7.83); g.add(nf);
      var nd = new THREE.Mesh(new THREE.BoxGeometry(0.05, 2.05, 0.88), M.doorMetal);
      nd.position.set(L0+0.055, 1.025, 7.83); nd.castShadow = true; g.add(nd);
      var nh = new THREE.Mesh(new THREE.CylinderGeometry(0.012,0.012,0.10,10), M.chrome);
      nh.rotation.x = Math.PI/2; nh.position.set(L0+0.09, 1.02, 7.52); g.add(nh);
    })();""",
    """    /* просто стены (лифты и дверь соседа убраны по отметкам) */""")

# --- петли дверей: полотна больше не заходят в стены ---
rep("    kit:  mkDoor(3.70, K.z1+P.LOAD/2-0.04, 0.79, [1,0], [0,-1]),",
    "    kit:  mkDoor(3.70, K.z1+P.LOAD/2-0.06, 0.79, [1,0], [0,-1]),")
rep("    room: mkDoor(K.x0-P.LOAD/2, DH.room.z1, 0.80, [0,-1], [-1,0]),",
    "    room: mkDoor(K.x0-P.LOAD/2, DH.room.z1-0.02, 0.80, [0,-1], [-1,0]),")
rep("    ent:  mkDoor(DH.ent.x1-0.02, HA.z1+P.LOAD/2, 0.88, [-1,0], [0,1], true)",
    "    ent:  mkDoor(DH.ent.x1-0.02, HA.z1+P.LOAD, 0.88, [-1,0], [0,1], true)")

# --- ящик-половинку убрать: второй верхний фасад снова целый ---
rep("""    if (i3 === 1){
      /* второй фасад — разрезной в половину: снизу мини-ящик, сверху дверца */
      var d2b = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH/2-0.03, UZD-0.02), M.front);
      d2b.position.set(mx(KX-0.35), (UY0+UYM)/2+0.005, uz); d2b.castShadow = d2b.receiveShadow = true;
      var hb = mkHinge(d2b, mx(KX-0.35), uz-(UZD-0.02)/2+0.01, 'ящик', -1.8, upGrp);
      var uhb = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
      uhb.position.set(-0.025, 0.02, UZD-0.02-0.055);
      uhb.castShadow = true; handles.push(uhb); hb.grp.add(uhb);
      var d2c = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH/2-0.03, UZD-0.02), M.front);
      d2c.position.set(mx(KX-0.35), (UYM+UY1)/2-0.005, uz); d2c.castShadow = d2c.receiveShadow = true;
      var hc = mkHinge(d2c, mx(KX-0.35), uz-(UZD-0.02)/2+0.01, 'шкафчик', -1.8, upGrp);
      var uhc = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
      uhc.position.set(-0.025, (UPH/2-0.03)-0.075, UZD-0.02-0.055);
      uhc.castShadow = true; handles.push(uhc); hc.grp.add(uhc);
    } else {
      var d2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH-0.02, UZD-0.02), M.front);
      d2.position.set(mx(KX-0.35), UYM, uz); d2.castShadow = d2.receiveShadow = true;
      var hu = mkHinge(d2, mx(KX-0.35), uz - (UZD-0.02)/2 + 0.01, 'шкафчик', -1.8, upGrp);
      var uh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
      uh.position.set(-0.025, UY0-UYM+0.09, UZD-0.02-0.055);
      uh.castShadow = true; handles.push(uh); hu.grp.add(uh);
    }
  }""",
    """    var d2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH-0.02, UZD-0.02), M.front);
    d2.position.set(mx(KX-0.35), UYM, uz); d2.castShadow = d2.receiveShadow = true;
    var hu = mkHinge(d2, mx(KX-0.35), uz - (UZD-0.02)/2 + 0.01, 'шкафчик', -1.8, upGrp);
    var uh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
    uh.position.set(-0.025, UY0-UYM+0.09, UZD-0.02-0.055);
    uh.castShadow = true; handles.push(uh); hu.grp.add(uh);
  }""")

# --- площадка: плиты пола чуть выше базовой — без щелей и мерцания у стен ---
rep("      m.position.set((x0+x1)/2, -0.046, (z0+z1)/2); m.receiveShadow = true; g.add(m); return m;",
    "      m.position.set((x0+x1)/2, -0.038, (z0+z1)/2); m.receiveShadow = true; g.add(m); return m;")

p.write_text(s, encoding='utf-8')
print('K1 ok')
