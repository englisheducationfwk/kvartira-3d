"""H3: вода — рабочие краны на кухне и в санузле, кран+душ в ванне с реальным
наполнением (уровень воды), зеркала становятся рабочими (настоящее отражение,
куб-игрок виден в зеркале), в коридоре — люстра с тремя плафонами, выключатель
и красная пожарная кнопка."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    s = s.replace(old, new, count)


# ---------- материалы ----------
rep("  mirror:    new THREE.MeshStandardMaterial({ color:0xc9dde6, metalness:.6, roughness:.12 }),",
    """  mirror:    new THREE.MeshStandardMaterial({ color:0xc9dde6, metalness:.6, roughness:.12 }),
  water:     new THREE.MeshStandardMaterial({ color:0x9fc8e8, transparent:true, opacity:.55, roughness:.15 }),
  lampGlass: new THREE.MeshStandardMaterial({ color:0xfff2d8, transparent:true, opacity:.45, side:THREE.DoubleSide, roughness:.2 }),
  bulb:      new THREE.MeshStandardMaterial({ color:0xfff6e0, emissive:0xffdf9e, emissiveIntensity:0, roughness:.3 }),
  redBtn:    new THREE.MeshStandardMaterial({ color:0xcc2a1e, roughness:.45 }),""")

# ---------- реестры кранов ----------
rep("var HINGES = [], hingeParts = [];",
    "var HINGES = [], hingeParts = [];\nvar TAPS = [], tapParts = [];")
rep("  HINGES = []; hingeParts = [];",
    "  HINGES = []; hingeParts = []; TAPS = []; tapParts = [];")

# ---------- рабочее зеркало ----------
rep("""function toggleHinge(h){
  h.open = !h.open;
  h.anim = { t:0, dur:0.4, from:h.cur, to: h.open ? h.a1 : h.a0 };
  toast((h.open ? 'Открыл: ' : 'Закрыл: ') + (h.name || 'ящик'));
}""",
    """function toggleHinge(h){
  h.open = !h.open;
  h.anim = { t:0, dur:0.4, from:h.cur, to: h.open ? h.a1 : h.a0 };
  toast((h.open ? 'Открыл: ' : 'Закрыл: ') + (h.name || 'ящик'));
}
/* рабочее зеркало: настоящее отражение через второй рендер */
var mirrorRT = null, mirrorCam = null, mirrorBusy = false;
function makeMirror(w, h){
  var mat = new THREE.ShaderMaterial({
    uniforms: { tDiffuse: { value: null }, textureMatrix: { value: new THREE.Matrix4() } },
    vertexShader: 'uniform mat4 textureMatrix; varying vec4 vUv;\\n' +
      'void main(){ vUv = textureMatrix * vec4(position, 1.0);' +
      ' gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: 'uniform sampler2D tDiffuse; varying vec4 vUv;\\n' +
      'void main(){ gl_FragColor = texture2DProj(tDiffuse, vUv); }'
  });
  var mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
  var rp = new THREE.Vector3(), cp = new THREE.Vector3(), nrm = new THREE.Vector3(),
      view = new THREE.Vector3(), look = new THREE.Vector3(), tgt = new THREE.Vector3(),
      rotM = new THREE.Matrix4(), tm = mat.uniforms.textureMatrix.value;
  mesh.onBeforeRender = function(rend, scn, cam){
    if (mirrorBusy) return;
    mirrorBusy = true;
    if (!mirrorRT) mirrorRT = new THREE.WebGLRenderTarget(640, 640);
    if (!mirrorCam){ mirrorCam = new THREE.PerspectiveCamera(); mirrorCam.layers.enable(1); }
    rp.setFromMatrixPosition(mesh.matrixWorld);
    cp.setFromMatrixPosition(cam.matrixWorld);
    rotM.extractRotation(mesh.matrixWorld);
    nrm.set(0, 0, 1).applyMatrix4(rotM);
    view.subVectors(rp, cp);
    if (view.dot(nrm) > 0){ mirrorBusy = false; return; }
    view.reflect(nrm).negate().add(rp);
    rotM.extractRotation(cam.matrixWorld);
    look.set(0, 0, -1).applyMatrix4(rotM).add(cp);
    tgt.subVectors(rp, look).reflect(nrm).negate().add(rp);
    mirrorCam.position.copy(view);
    mirrorCam.up.set(0, 1, 0).applyMatrix4(rotM).reflect(nrm);
    mirrorCam.lookAt(tgt);
    mirrorCam.far = cam.far;
    mirrorCam.updateMatrixWorld();
    mirrorCam.projectionMatrix.copy(cam.projectionMatrix);
    tm.set(0.5,0,0,0.5, 0,0.5,0,0.5, 0,0,0.5,0.5, 0,0,0,1);
    tm.multiply(mirrorCam.projectionMatrix).multiply(mirrorCam.matrixWorldInverse);
    var was = mesh.visible; mesh.visible = false;
    var oldRT = rend.getRenderTarget();
    rend.setRenderTarget(mirrorRT);
    rend.clear();
    rend.render(scn, mirrorCam);
    rend.setRenderTarget(oldRT);
    mesh.visible = was;
    mat.uniforms.tDiffuse.value = mirrorRT.texture;
    mirrorBusy = false;
  };
  return mesh;
}
/* рабочие краны и душ */
function toggleTap(t){
  if (t.sub === 'tub'){ t.fill = !t.fill; toast(t.fill ? 'Наливаю ванну 💧' : 'Сливаю воду…'); }
  else if (t.sub === 'shower'){ t.on = !t.on; t.mesh.visible = t.on; toast(t.on ? 'Душ включён 🚿' : 'Душ выключен'); }
  else if (t.sub === 'stream'){ t.on = !t.on; t.mesh.visible = t.on; toast((t.name || 'Кран') + (t.on ? ': вода пошла 💦' : ': вода закрыта')); }
  else if (t.sub === 'switch'){
    t.on = !t.on;
    if (t.rocker) t.rocker.rotation.x = t.on ? 0.16 : -0.16;
    if (t.light) t.light.intensity = t.on ? 0.85 : 0;
    M.bulb.emissiveIntensity = (t.on && t.bulbs) ? 1.2 : M.bulb.emissiveIntensity;
    if (t.bulbs) t.bulbs.forEach(function(b2){ b2.visible = true; });
    toast(t.on ? 'Свет включён 💡' : 'Свет выключен');
  }
}
function useThing(d){
  if (!d) return;
  if (d.kind === 'sofa') toggleSofa(d);
  else if (d.kind === 'hinge') toggleHinge(d);
  else if (d.kind === 'tap') toggleTap(d);
  else toggleDoor(d);
}""")

# ---------- тик воды ----------
rep("""  HINGES.forEach(function(h){
    if (!h.anim) return;
    h.anim.t = Math.min(1, h.anim.t + dt/h.anim.dur);
    var e3 = h.anim.t<0.5 ? 2*h.anim.t*h.anim.t : -1+(4-2*h.anim.t)*h.anim.t;
    h.cur = h.anim.from + (h.anim.to - h.anim.from)*e3;
    h.grp.rotation.y = h.cur;
    if (h.anim.t >= 1) h.anim = null;
  });
}""",
    """  HINGES.forEach(function(h){
    if (!h.anim) return;
    h.anim.t = Math.min(1, h.anim.t + dt/h.anim.dur);
    var e3 = h.anim.t<0.5 ? 2*h.anim.t*h.anim.t : -1+(4-2*h.anim.t)*h.anim.t;
    h.cur = h.anim.from + (h.anim.to - h.anim.from)*e3;
    h.grp.rotation.y = h.cur;
    if (h.anim.t >= 1) h.anim = null;
  });
  /* вода: наполнение ванны и струя из смесителя */
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
  });
}""")

# ---------- клики: универсальная кнопка ----------
rep("  if (d && held < 0){ if (d.kind === 'sofa') toggleSofa(d); else if (d.kind === 'hinge') toggleHinge(d); else toggleDoor(d); return; }",
    "  if (d && held < 0){ useThing(d); return; }")
rep("""    var d = doorUnder(0, 0);
    if (d && held < 0){ if (d.kind === 'sofa') toggleSofa(d); else if (d.kind === 'hinge') toggleHinge(d); else toggleDoor(d); return; }""",
    """    var d = doorUnder(0, 0);
    if (d && held < 0){ useThing(d); return; }""")
rep("""    var d2 = doorUnder(0, 0);
    if (d2){ if (d2.kind === 'sofa') toggleSofa(d2); else if (d2.kind === 'hinge') toggleHinge(d2); else toggleDoor(d2); return; }""",
    """    var d2 = doorUnder(0, 0);
    if (d2){ useThing(d2); return; }""")
rep("  var hits = raycaster.intersectObjects(doorLeaves.concat(sofaParts, hingeParts), false);\n  if (!hits.length) return null;\n  var u = hits[0].object.userData;\n  return u.door || u.sofa || u.hinge || null;",
    "  var hits = raycaster.intersectObjects(doorLeaves.concat(sofaParts, hingeParts, tapParts), false);\n  if (!hits.length) return null;\n  var u = hits[0].object.userData;\n  return u.door || u.sofa || u.hinge || u.tap || null;")

# ---------- кухонная мойка: струя + клик по крану ----------
rep("""    cyl(0.022,0.026,0.05, M.chrome, KX-0.07, WT+0.025, 2.44);
    cyl(0.015,0.015,0.26, M.chrome, KX-0.07, WT+0.16, 2.44);
    cyl(0.013,0.013,0.20, M.chrome, KX-0.17, WT+0.29, 2.44, null, Math.PI/2);""",
    """    var ck1 = cyl(0.022,0.026,0.05, M.chrome, KX-0.07, WT+0.025, 2.44);
    var ck2 = cyl(0.015,0.015,0.26, M.chrome, KX-0.07, WT+0.16, 2.44);
    var ck3 = cyl(0.013,0.013,0.20, M.chrome, KX-0.17, WT+0.29, 2.44, null, Math.PI/2);
    var kStream = new THREE.Mesh(new THREE.CylinderGeometry(0.007, 0.007, 0.26, 10), M.water);
    kStream.position.set(mx(KX-0.17), WT+0.16, 2.44); kStream.visible = false; IT.add(kStream);
    var kTap = { kind:'tap', sub:'stream', on:false, mesh:kStream, name:'Кухня' };
    [ck1, ck2, ck3].forEach(function(cm){ cm.userData.tap = kTap; tapParts.push(cm); });
    TAPS.push(kTap);""")

# ---------- раковина в санузле: струя + клик ----------
rep("""  IT = item('Раковина', '🚰', 0.28, 0.21);
  ibox(IT, 6.18, 4.20, 0.54, 0.42, 0.70, 0.82, M.white);
  (function(){
    var bw = new THREE.Mesh(new THREE.PlaneGeometry(0.46, 0.34), M.dark);
    bw.geometry.rotateX(-Math.PI/2); bw.position.set(mx(6.18), 0.826, 4.20); IT.add(bw);
    var sf = new THREE.Mesh(new THREE.CylinderGeometry(0.014,0.014,0.17,12), M.chrome);
    sf.position.set(mx(6.36), 0.90, 4.20); IT.add(sf);
    var sn = new THREE.Mesh(new THREE.CylinderGeometry(0.011,0.011,0.14,12), M.chrome);
    sn.rotation.z = Math.PI/2; sn.position.set(mx(6.30), 0.985, 4.20); IT.add(sn);
  })();""",
    """  IT = item('Раковина', '🚰', 0.28, 0.21);
  ibox(IT, 6.18, 4.20, 0.54, 0.42, 0.70, 0.82, M.white);
  (function(){
    var bw = new THREE.Mesh(new THREE.PlaneGeometry(0.46, 0.34), M.dark);
    bw.geometry.rotateX(-Math.PI/2); bw.position.set(mx(6.18), 0.826, 4.20); IT.add(bw);
    var sf = new THREE.Mesh(new THREE.CylinderGeometry(0.014,0.014,0.17,12), M.chrome);
    sf.position.set(mx(6.36), 0.90, 4.20); IT.add(sf);
    var sn = new THREE.Mesh(new THREE.CylinderGeometry(0.011,0.011,0.14,12), M.chrome);
    sn.rotation.z = Math.PI/2; sn.position.set(mx(6.30), 0.985, 4.20); IT.add(sn);
    var sStream = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.13, 10), M.water);
    sStream.position.set(mx(6.30), 0.965, 4.20); sStream.visible = false; IT.add(sStream);
    var sTap = { kind:'tap', sub:'stream', on:false, mesh:sStream, name:'Санузел' };
    [sf, sn].forEach(function(cm){ cm.userData.tap = sTap; tapParts.push(cm); });
    TAPS.push(sTap);
  })();""")

# ---------- ванна: кран + душ + уровень воды ----------
rep("""  IT = item('Зеркало в санузле', '🪞', 0, 0);
  (function(){
    var mirr2 = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 0.7), M.mirror);
    mirr2.rotation.y = faceRY(-Math.PI/2);
    mirr2.position.set(mx(6.44), 1.60, 4.20); IT.add(mirr2);
  })();""",
    """  IT = item('Зеркало в санузле', '🪞', 0, 0);
  (function(){
    var mirr2 = makeMirror(0.5, 0.7);
    mirr2.rotation.y = faceRY(-Math.PI/2);
    mirr2.position.set(mx(6.44), 1.60, 4.20); IT.add(mirr2);
  })();
  /* кран и душ у ванны: клик — ванна наполняется */
  (function(){
    function wm(mesh, t){ mesh.userData.tap = t; tapParts.push(mesh); }
    var riser = new THREE.Mesh(new THREE.CylinderGeometry(0.012,0.012,1.30,12), M.chrome);
    riser.position.set(mx(6.43), 1.37, 5.17); gRoom.add(riser);
    var arm = new THREE.Mesh(new THREE.CylinderGeometry(0.011,0.011,0.30,12), M.chrome);
    arm.rotation.z = Math.PI/2; arm.position.set(mx(6.28), 2.02, 5.17); gRoom.add(arm);
    var head = new THREE.Mesh(new THREE.CylinderGeometry(0.055,0.022,0.05,16), M.steel);
    head.position.set(mx(6.14), 1.99, 5.17); head.castShadow = true; gRoom.add(head);
    var spray = new THREE.Mesh(new THREE.CylinderGeometry(0.02,0.15,1.40,12,1,true), M.water);
    spray.position.set(mx(6.14), 1.28, 5.17); spray.visible = false; gRoom.add(spray);
    var tSh = { kind:'tap', sub:'shower', on:false, mesh:spray, name:'Душ' };
    wm(head, tSh); wm(arm, tSh); wm(riser, tSh);
    var tap = new THREE.Mesh(new THREE.CylinderGeometry(0.024,0.028,0.07,14), M.chrome);
    tap.rotation.z = Math.PI/2; tap.position.set(mx(6.42), 0.72, 5.17); gRoom.add(tap);
    var spout = new THREE.Mesh(new THREE.CylinderGeometry(0.013,0.013,0.22,12), M.chrome);
    spout.rotation.z = Math.PI/2; spout.position.set(mx(6.30), 0.72, 5.17); gRoom.add(spout);
    var stream = new THREE.Mesh(new THREE.CylinderGeometry(0.008,0.008,0.42,10), M.water);
    stream.position.set(mx(6.20), 0.48, 5.17); stream.visible = false; gRoom.add(stream);
    var wl = new THREE.Mesh(new THREE.PlaneGeometry(1.44, 0.48), M.water);
    wl.geometry.rotateX(-Math.PI/2); wl.position.set(mx(5.48), 0.15, 5.17); wl.visible = false; gRoom.add(wl);
    var tTub = { kind:'tap', sub:'tub', fill:false, level:0, mesh:wl, stream:stream,
                 y0:0.15, y1:0.50, name:'Ванна' };
    wm(tap, tTub); wm(spout, tTub);
    TAPS.push(tSh); TAPS.push(tTub);
  })();""")

# ---------- зеркало в коридоре — рабочее ----------
rep("""  IT = item('Зеркало', '🪞', 0, 0);
  (function(){
    var mirr = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 1.2), M.mirror);
    mirr.rotation.y = faceRY(Math.PI/2); mirr.position.set(mx(3.581), 1.45, 5.90); IT.add(mirr);
    var fr = new THREE.Mesh(new THREE.BoxGeometry(0.02, 1.24, 0.54), M.woodDark);
    fr.position.set(mx(3.565), 1.45, 5.90); IT.add(fr);
  })();""",
    """  IT = item('Зеркало', '🪞', 0, 0);
  (function(){
    var mirr = makeMirror(0.5, 1.2);
    mirr.rotation.y = faceRY(Math.PI/2); mirr.position.set(mx(3.581), 1.45, 5.90); IT.add(mirr);
    var fr = new THREE.Mesh(new THREE.BoxGeometry(0.02, 1.24, 0.54), M.woodDark);
    fr.position.set(mx(3.565), 1.45, 5.90); IT.add(fr);
  })();""")

# ---------- коридор: люстра три плафона, выключатель, пожарная кнопка ----------
rep("""  /* мини-коридор у входа: зеркало на западной стене + комод */""",
    """  /* коридор: люстра с тремя плафонами (завитками в ряд) + выключатель + пожарная кнопка */
  var corLight = new THREE.PointLight(0xffe8c0, 0.0, 7, 2);
  corLight.position.set(mx(4.45), 2.30, 5.73); gRoom.add(corLight);
  (function(){
    var bx = mx(4.45);
    var base = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.075, 0.035, 16), M.frame);
    base.position.set(bx, P.HC-0.018, 5.73); gRoom.add(base);
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
  })();
  (function(){
    var bx = mx(4.72);
    var pl = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.09, 0.014), M.frame);
    pl.position.set(bx, 1.55, HA.z1-0.012); gRoom.add(pl);
    var rock = new THREE.Mesh(new THREE.BoxGeometry(0.032, 0.05, 0.014), M.white);
    rock.position.set(bx, 1.55, HA.z1-0.022); gRoom.add(rock);
    var sw = { kind:'tap', sub:'switch', on:false, light:corLight, rocker:rock, bulbs:[M.bulb] };
    rock.userData.tap = sw; tapParts.push(rock);
    pl.userData.tap = sw; tapParts.push(pl);
    TAPS.push(sw);
  })();
  (function(){
    var bx = mx(5.07);
    var pl = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.11, 0.016), M.frame);
    pl.position.set(bx, 1.54, HA.z1-0.012); gRoom.add(pl);
    var btn = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.032, 0.02, 16), M.redBtn);
    btn.rotation.x = Math.PI/2; btn.position.set(bx, 1.54, HA.z1-0.027); gRoom.add(btn);
  })();
  /* мини-коридор у входа: зеркало на западной стене + комод */""")

# ---------- куб-игрок видно в зеркале ----------
rep("  scene.add(gRoom, gKitchen, gFurn, gDecals, gTape, gDims, gProps);",
    """  scene.add(gRoom, gKitchen, gFurn, gDecals, gTape, gDims, gProps);
  if (playerCube){ scene.remove(playerCube); playerCube = null; }
  playerCube = new THREE.Mesh(new THREE.BoxGeometry(0.42, 1.72, 0.42), M.fabric2);
  playerCube.layers.set(1); playerCube.position.set(0, -10, 0);
  scene.add(playerCube);""")
rep("var TAPS = [], tapParts = [];",
    "var TAPS = [], tapParts = [];\nvar playerCube = null;")
rep("""  if (state.mode === 'walk'){
    if (walk.locked || Object.keys(walk.keys).some(function(k2){ return walk.keys[k2]; })) walkUpdate(dt);
    updateMap();""",
    """  if (state.mode === 'walk'){
    if (walk.locked || Object.keys(walk.keys).some(function(k2){ return walk.keys[k2]; })) walkUpdate(dt);
    if (playerCube){
      playerCube.visible = true;
      playerCube.position.set(walk.pos.x, 0.86 + walk.pos.y, walk.pos.z);
      playerCube.rotation.y = walk.yaw;
    }
    updateMap();""")

p.write_text(s, encoding='utf-8')
print('H3 ok')
