"""J1: окно эркера — наклон убрать, первое окно вертикально на скос (диагональ),
передние створки обратно 100+70; дверь комнаты без захода в стену; маленький диван —
как большой, 1:1, в разобранном виде; белая полка — в 2 столбца и 4 полки."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    s = s.replace(old, new, count)


# --- 1) наклон окон убрать (как было)
rep("""      var fr = new THREE.Group(); grp.add(fr);
      fr.position.y = y0; fr.rotation.x = 0.10;    /* окно скошено под углом внутрь */
      function bar(bw,bh,bx,by){ var m = new THREE.Mesh(new THREE.BoxGeometry(bw,bh,0.10), M.frame);
        m.position.set(bx, by - y0, 0); fr.add(m); return m; }""",
    """      var fr = new THREE.Group(); grp.add(fr);
      function bar(bw,bh,bx,by){ var m = new THREE.Mesh(new THREE.BoxGeometry(bw,bh,0.10), M.frame);
        m.position.set(bx, by, 0); fr.add(m); return m; }""")

# --- 2) передние створки — снова 100 + 70
rep("    var parts = [ [0.50, 0.00], [0.50, 0.50], [0.70, 1.00] ];",
    "    var parts = [ [1.00, 0.00], [0.70, 1.00] ];")

# --- 3) на левом скосе (диагонали) — вертикальное окно-створка
rep("""  [ [ [BAY.p0,BAY.p1], true ], [ [BAY.p1,BAY.p2], false ], [ [BAY.p2,BAY.p3], true ] ].forEach(function(pr){""",
    """  [ [ [BAY.p0,BAY.p1], true ], [ [BAY.p1,BAY.p2], false ], [ [BAY.p2,BAY.p3], true ] ].forEach(function(pr, pi){""")
rep("""    if (pr[1]){
      var mMid = solidBeam(a, b, P.LOAD, P.bay.sillY, BWP, null, M.facade2, 1.35, gRoom);
      stagedFaces.push({ mesh:mMid, idx:mMid.userData.innerIdx });
    }""",
    """    if (pr[1] && pi > 0){                 /* правый скос глухой; на левом — окно */
      var mMid = solidBeam(a, b, P.LOAD, P.bay.sillY, BWP, null, M.facade2, 1.35, gRoom);
      stagedFaces.push({ mesh:mMid, idx:mMid.userData.innerIdx });
    }""")
rep("""  /* две створки переднего окна — открываются кликом */""",
    """  /* первое окно — вертикально на левом скосе (диагонали), открывается кликом */
  (function(){
    var a = BAY.p0, b = BAY.p1;
    var A2 = mp(a), B2 = mp(b);
    var len = Math.hypot(B2[0]-A2[0], B2[1]-A2[1]);
    var ux = (B2[0]-A2[0])/len, uz = (B2[1]-A2[1])/len;
    var w = len - 0.10, off = 0.05;
    var hx = A2[0] + ux*off, hz = A2[1] + uz*off;
    var grp = new THREE.Group(); grp.position.set(hx, 0, hz);
    var rot0 = Math.atan2(-uz, ux);
    grp.rotation.y = rot0;
    var y0 = P.bay.sillY, y1 = BWP, hgt = y1-y0;
    var fr = new THREE.Group(); grp.add(fr);
    function bar(bw,bh,bx,by){ var m = new THREE.Mesh(new THREE.BoxGeometry(bw,bh,0.10), M.frame);
      m.position.set(bx, by, 0); fr.add(m); return m; }
    bar(w-0.04, 0.06, w/2, y0+0.03);
    bar(w-0.04, 0.06, w/2, y1-0.03);
    bar(0.06, hgt, 0.03, (y0+y1)/2);
    bar(0.06, hgt, w-0.03, (y0+y1)/2);
    var gls = new THREE.Mesh(new THREE.PlaneGeometry(w-0.08, hgt-0.10), M.glass);
    gls.position.set(w/2, (y0+y1)/2, 0.005); fr.add(gls);
    fr.traverse(function(o){ if (o.isMesh){ o.castShadow = (o.material !== M.glass); o.receiveShadow = true; } });
    gRoom.add(grp);
    var d = { grp: grp, w: w, a0: rot0, a1: rot0 - 1.25, cur: rot0, open:false, anim:null, noSeg:true };
    fr.children.forEach(function(o){ doorLeaves.push(o); o.userData.door = d; });
    WIN_SASHES.push(d);
  })();
  /* две створки переднего окна — открываются кликом */""")

# --- 4) дверь комнаты: ровно по проёму, без захода в стену
rep("    room: mkDoor(K.x0-P.LOAD/2, DH.room.z1-0.04, 0.82, [0,-1], [-1,0]),",
    "    room: mkDoor(K.x0-P.LOAD/2, DH.room.z1, 0.80, [0,-1], [-1,0]),")

# --- 5) маленький диван — как большой, 1:1, сразу разобранный
rep("""  /* кровать убрана по отметке; у южной стены — маленький диван */
  var IT = item('Диван (маленький)', '🛋', 0.72, 0.40);
  ibox(IT, 1.70, 5.97, 1.30, 0.68, 0.14, 0.26, M.woodDark);            /* каркас */
  [[1.10,5.68],[2.30,5.68],[1.10,6.26],[2.30,6.26]].forEach(function(lg){
    ibox(IT, lg[0], lg[1], 0.05, 0.05, 0, 0.14, M.woodDark);           /* ножки */
  });
  ibox(IT, 1.70, 6.245, 1.30, 0.15, 0.26, 0.86, M.fabric2);            /* спинка у стены */
  ibox(IT, 1.70, 5.88, 1.30, 0.52, 0.26, 0.44, M.fabric);              /* сиденье */
  ibox(IT, 1.085, 5.97, 0.13, 0.62, 0, 0.56, M.fabric2);               /* подлокотники */
  ibox(IT, 2.315, 5.97, 0.13, 0.62, 0, 0.56, M.fabric2);""",
    """  /* кровать убрана по отметке; у южной стены — маленький диван: как большой, но разобранный */
  var IT = item('Диван (маленький)', '🛋', 0.74, 0.52);
  ibox(IT, 1.60, 5.99, 1.44, 0.66, 0.15, 0.27, M.woodDark);            /* каркас */
  [[0.98,5.72],[2.22,5.72],[0.98,6.26],[2.22,6.26]].forEach(function(lg){
    ibox(IT, lg[0], lg[1], 0.05, 0.05, 0, 0.15, M.woodDark);           /* ножки */
  });
  ibox(IT, 0.94, 5.99, 0.12, 0.70, 0, 0.60, M.fabric2);                /* подлокотники */
  ibox(IT, 2.26, 5.99, 0.12, 0.70, 0, 0.60, M.fabric2);
  ibox(IT, 1.60, 5.58, 1.24, 0.46, 0.27, 0.50, M.fabric);              /* сиденье выдвинуто */
  ibox(IT, 1.60, 6.08, 1.24, 0.44, 0.27, 0.50, M.fabric);              /* лежак */
  ibox(IT, 1.60, 6.27, 1.24, 0.10, 0.30, 0.58, M.fabric2);             /* спинка лежит у стены */""")

# --- 6) белая полка — 2 столбца, 4 полки, в 2 раза шире
rep("""  IT = item('Полка', '🗄', 0.18, 0.36);
  ibox(IT, 3.77, 6.85, 0.34, 0.70, 0.76, 0.80, M.white);
  ibox(IT, 3.77, 6.85, 0.34, 0.70, 0.36, 0.40, M.white);
  ibox(IT, 3.77, 6.85, 0.34, 0.70, 0, 0.04, M.white);
  ibox(IT, 3.77, 6.51, 0.34, 0.02, 0.04, 0.80, M.white);
  ibox(IT, 3.77, 7.19, 0.34, 0.02, 0.04, 0.80, M.white);""",
    """  IT = item('Полка', '🗄', 0.18, 0.62);
  [0.02, 0.44, 0.86, 1.28].forEach(function(yy){                       /* 4 полки */
    ibox(IT, 3.77, 6.80, 0.34, 1.20, yy, yy+0.03, M.white);
  });
  ibox(IT, 3.77, 6.225, 0.34, 0.02, 0.02, 1.31, M.white);              /* боковины */
  ibox(IT, 3.77, 7.375, 0.34, 0.02, 0.02, 1.31, M.white);
  ibox(IT, 3.77, 6.80, 0.34, 0.02, 0.02, 1.31, M.white);               /* столбик по центру */""")

p.write_text(s, encoding='utf-8')
print('J1 ok')
