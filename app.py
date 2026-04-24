# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

html = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <style>
    :root{
      --accent:#00e5ff;
      --accent-soft:rgba(0,229,255,.14);
      --yellow:#ffee32;
      --bg:#06111b;
      --panel:#061923;
      --panel2:#082632;
      --text:#e9fbff;
      --muted:#9fb5c3;
    }

    *{box-sizing:border-box;}

    html, body{
      margin:0;
      padding:0;
      width:100%;
      height:100%;
      overflow:hidden;
      font-family:Arial, Helvetica, sans-serif;
      background:#06111b;
    }

    #stage{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      overflow-y:auto;
      overflow-x:hidden;
      -webkit-overflow-scrolling:touch;
      color:var(--text);
      background:
        radial-gradient(circle at 50% 12%, color-mix(in srgb, var(--accent) 20%, transparent), transparent 28%),
        linear-gradient(180deg, #06111b 0%, #071926 45%, #051018 100%);
    }

    .app{
      width:100%;
      min-height:100vh;
      padding:10px 10px 92px 10px;
    }

    .hidden{
      display:none !important;
    }

    .topbar{
      border:1px solid var(--accent);
      border-radius:18px;
      padding:10px;
      background:rgba(0,0,0,.42);
      box-shadow:0 0 18px color-mix(in srgb, var(--accent) 35%, transparent);
      margin-bottom:10px;
    }

    .logo{
      width:100%;
      text-align:center;
      font-size:30px;
      font-weight:900;
      letter-spacing:3px;
      color:#9dffbd;
      text-shadow:0 0 14px color-mix(in srgb, var(--accent) 70%, transparent);
      line-height:1;
      margin-bottom:10px;
    }

    .top-grid{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:8px;
    }

    .top-pill{
      border:1px solid var(--accent);
      background:rgba(0,50,65,.55);
      border-radius:999px;
      min-height:36px;
      display:flex;
      align-items:center;
      justify-content:center;
      gap:6px;
      font-size:13px;
      font-weight:700;
      color:var(--text);
      overflow:hidden;
      white-space:nowrap;
    }

    .socials{
      display:flex;
      justify-content:center;
      gap:10px;
      font-size:15px;
    }

    .stats{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:8px;
      margin-bottom:12px;
    }

    .stat-card{
      border:1px solid var(--accent);
      border-radius:14px;
      padding:10px;
      background:rgba(0,10,18,.72);
      min-height:80px;
      box-shadow:0 0 12px color-mix(in srgb, var(--accent) 25%, transparent);
    }

    .stat-title{
      color:var(--yellow);
      font-size:10px;
      font-weight:900;
      text-transform:uppercase;
      margin-bottom:8px;
    }

    .stat-value{
      font-size:21px;
      font-weight:900;
      color:var(--text);
    }

    .stat-small{
      font-size:10px;
      color:#bcefff;
      margin-top:5px;
      line-height:1.3;
    }

    .btn-recargar{
      display:inline-flex;
      margin-top:8px;
      padding:4px 9px;
      border-radius:999px;
      background:var(--accent);
      color:#001018;
      font-weight:900;
      font-size:10px;
    }

    .title-main{
      font-size:21px;
      line-height:1;
      color:var(--yellow);
      font-weight:1000;
      text-transform:uppercase;
      text-shadow:0 0 12px rgba(255,238,50,.75);
      margin:16px 0 10px 0;
    }

    .tabs{
      display:grid;
      grid-template-columns:1fr 1fr;
      border:1px solid var(--yellow);
      border-radius:14px 14px 0 0;
      overflow:hidden;
      background:rgba(0,0,0,.5);
    }

    .tab-btn{
      border:0;
      padding:13px 8px;
      font-size:13px;
      font-weight:900;
      color:var(--text);
      background:transparent;
      cursor:pointer;
      text-transform:uppercase;
    }

    .tab-btn.active{
      color:var(--yellow);
      background:rgba(255,238,50,.13);
      box-shadow:inset 0 -3px 0 var(--yellow);
    }

    .panel{
      border:1px solid rgba(255,238,50,.85);
      border-top:0;
      border-radius:0 0 14px 14px;
      background:rgba(0,12,18,.72);
      padding:12px;
      box-shadow:0 0 15px rgba(255,238,50,.18);
      margin-bottom:14px;
    }

    #participantesPanel{
      border-top:1px solid rgba(255,238,50,.85);
      border-radius:14px;
    }

    .section-title{
      color:var(--yellow);
      font-size:16px;
      font-weight:900;
      margin-bottom:10px;
      line-height:1.1;
    }

    .field-label{
      font-size:11px;
      font-weight:900;
      color:var(--yellow);
      margin-bottom:5px;
      text-transform:uppercase;
    }

    select, input{
      width:100%;
      border:1px solid var(--accent);
      background:rgba(0,20,30,.88);
      color:var(--text);
      border-radius:999px;
      min-height:39px;
      padding:0 12px;
      outline:none;
      font-size:13px;
      font-weight:700;
    }

    input::placeholder{color:#7e8d96;}

    .ficha{
      margin-top:12px;
      border:1px solid var(--accent);
      border-radius:14px;
      background:rgba(0,23,34,.72);
      overflow:hidden;
    }

    .ficha-row{
      display:grid;
      grid-template-columns:42% 58%;
      border-bottom:1px solid rgba(255,255,255,.14);
      min-height:38px;
    }

    .ficha-row:last-child{border-bottom:0;}

    .ficha-k{
      padding:10px;
      font-size:11px;
      font-weight:900;
      color:var(--yellow);
      background:rgba(255,238,50,.08);
      display:flex;
      align-items:center;
    }

    .ficha-v{
      padding:10px;
      font-size:12px;
      font-weight:800;
      color:var(--text);
      display:flex;
      align-items:center;
      overflow-wrap:anywhere;
    }

    .actions{
      display:flex;
      gap:8px;
      align-items:center;
      flex-wrap:wrap;
    }

    .action-btn{
      width:34px;
      height:34px;
      border-radius:999px;
      border:1px solid var(--accent);
      background:var(--accent-soft);
      color:var(--accent);
      display:inline-flex;
      align-items:center;
      justify-content:center;
      font-size:16px;
      cursor:pointer;
    }

    .action-btn.disabled{
      opacity:.28;
      cursor:not-allowed;
      filter:grayscale(1);
    }

    .empty{
      border:1px dashed rgba(255,255,255,.28);
      border-radius:14px;
      padding:14px;
      font-size:13px;
      color:var(--muted);
      text-align:center;
      background:rgba(255,255,255,.04);
    }

    .participants-head{
      display:grid;
      grid-template-columns:1fr;
      gap:8px;
      margin-bottom:10px;
    }

    .participant-card{
      border:1px solid var(--accent);
      border-radius:14px;
      background:rgba(0,17,27,.76);
      overflow:hidden;
      margin-bottom:10px;
      box-shadow:0 0 10px color-mix(in srgb, var(--accent) 20%, transparent);
    }

    .participant-title{
      padding:10px 12px;
      font-size:14px;
      font-weight:900;
      color:var(--text);
      border-bottom:1px solid rgba(255,255,255,.12);
      background:var(--accent-soft);
    }

    .mini-grid{
      display:grid;
      grid-template-columns:1fr 1fr;
    }

    .mini-item{
      min-height:42px;
      padding:8px 10px;
      border-right:1px solid rgba(255,255,255,.10);
      border-bottom:1px solid rgba(255,255,255,.10);
    }

    .mini-item:nth-child(2n){border-right:0;}

    .mini-k{
      color:var(--yellow);
      font-size:10px;
      font-weight:900;
      margin-bottom:4px;
      text-transform:uppercase;
    }

    .mini-v{
      color:var(--text);
      font-size:12px;
      font-weight:800;
      line-height:1.25;
      overflow-wrap:anywhere;
    }

    .bottom-menu{
      position:fixed;
      left:0;
      right:0;
      bottom:0;
      z-index:9999;
      background:rgba(0,12,18,.96);
      border-top:1px solid var(--accent);
      box-shadow:0 -8px 22px color-mix(in srgb, var(--accent) 25%, transparent);
      padding:8px 8px 10px 8px;
      display:grid;
      grid-template-columns:repeat(5, 1fr);
      gap:8px;
    }

    .bottom-item{
      height:46px;
      border:1px solid var(--accent);
      border-radius:14px;
      background:var(--accent-soft);
      color:var(--accent);
      display:flex;
      align-items:center;
      justify-content:center;
      font-size:20px;
      font-weight:900;
      cursor:pointer;
    }

    .bottom-item.active{
      border-color:var(--yellow);
      color:var(--yellow);
      box-shadow:0 0 18px rgba(255,238,50,.75);
    }

    .overlay{
      position:fixed;
      inset:0;
      z-index:12000;
      display:none;
      align-items:center;
      justify-content:center;
      background:rgba(0,0,0,.32);
      padding:12px;
    }

    .overlay.show{display:flex;}

    .menu-window{
      width:min(96vw, 560px);
      height:min(82vh, 410px);
      border:1px solid var(--accent);
      border-radius:16px;
      background:rgba(0,12,18,.97);
      box-shadow:0 0 25px color-mix(in srgb, var(--accent) 30%, transparent);
      display:grid;
      grid-template-columns:88px 1fr;
      overflow:hidden;
    }

    .side-menu{
      border-right:1px solid var(--accent);
      background:rgba(0,30,38,.62);
      display:flex;
      flex-direction:column;
      align-items:center;
    }

    .side-title{
      width:100%;
      height:50px;
      display:flex;
      align-items:center;
      justify-content:center;
      font-size:19px;
      font-weight:1000;
      color:var(--accent);
      text-shadow:0 0 10px var(--accent);
      border-bottom:1px solid rgba(255,255,255,.12);
    }

    .side-icons{
      flex:1;
      width:100%;
      display:flex;
      flex-direction:column;
      align-items:center;
      justify-content:center;
      gap:14px;
      padding:12px 0;
    }

    .side-btn{
      width:56px;
      height:56px;
      border-radius:999px;
      border:1px solid rgba(0,229,255,.25);
      background:rgba(0,229,255,.08);
      color:var(--accent);
      display:flex;
      align-items:center;
      justify-content:center;
      font-size:24px;
      box-shadow:0 0 14px color-mix(in srgb, var(--accent) 22%, transparent);
      cursor:pointer;
    }

    .side-btn.active{
      color:var(--yellow);
      border-color:var(--yellow);
      box-shadow:0 0 20px rgba(255,238,50,.9);
    }

    .menu-content{
      min-width:0;
      display:flex;
      flex-direction:column;
    }

    .content-head{
      min-height:52px;
      border-bottom:1px solid rgba(255,255,255,.14);
      display:flex;
      align-items:center;
      justify-content:space-between;
      padding:0 16px;
    }

    .content-title{
      color:var(--accent);
      font-size:17px;
      font-weight:1000;
      letter-spacing:1px;
      text-shadow:0 0 10px var(--accent);
      text-transform:uppercase;
    }

    .close-btn{
      width:34px;
      height:26px;
      border-radius:999px;
      border:1px solid var(--accent);
      background:transparent;
      color:var(--text);
      font-weight:900;
      cursor:pointer;
    }

    .content-body{
      flex:1;
      min-height:0;
      overflow:auto;
      padding:16px;
    }

    .message-box{
      height:100%;
      display:flex;
      flex-direction:column;
      justify-content:flex-end;
      gap:10px;
    }

    .message-line{
      border-top:1px solid rgba(0,229,255,.35);
      padding-top:8px;
      display:grid;
      grid-template-columns:1fr 82px;
      gap:10px;
    }

    .send-btn{
      border:0;
      border-radius:999px;
      background:var(--accent);
      color:#001018;
      font-weight:1000;
      min-height:38px;
      cursor:pointer;
      box-shadow:0 0 15px color-mix(in srgb, var(--accent) 70%, transparent);
    }

    .alias-grid{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:8px 22px;
      margin-top:12px;
      max-height:200px;
      overflow-y:auto;
      background:rgba(0,229,255,.13);
      border-radius:8px;
      padding:10px;
      border-right:4px solid var(--accent);
    }

    .alias{
      width:max-content;
      max-width:100%;
      border:1px solid rgba(0,229,255,.35);
      background:var(--accent-soft);
      color:#dffcff;
      border-radius:999px;
      padding:7px 10px;
      font-size:12px;
      font-weight:800;
      overflow:hidden;
      text-overflow:ellipsis;
      white-space:nowrap;
    }

    .mesa-list{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:10px;
      margin-top:12px;
      background:rgba(0,229,255,.13);
      border-radius:8px;
      padding:12px;
    }

    .mesa-item{
      min-height:56px;
      border:1px solid rgba(0,229,255,.35);
      background:var(--accent-soft);
      border-radius:17px;
      padding:10px;
      font-size:12px;
      color:var(--text);
      font-weight:900;
      line-height:1.25;
    }

    .mesa-item strong{color:var(--yellow);}

    .mesa-item span{
      display:block;
      margin-top:5px;
      color:#bcefff;
      font-size:10px;
      font-weight:800;
    }

    .notif-list{
      display:grid;
      gap:10px;
      margin-top:10px;
    }

    .notif-item{
      border:1px solid var(--accent);
      border-radius:14px;
      background:var(--accent-soft);
      padding:12px;
      font-size:13px;
      font-weight:800;
      color:var(--text);
    }

    .center-empty{
      height:100%;
      display:flex;
      align-items:center;
      justify-content:center;
      font-size:16px;
      font-weight:800;
      color:#dffcff;
      text-align:center;
    }

    .color-panel{
      height:100%;
      display:flex;
      flex-direction:column;
      align-items:center;
      justify-content:flex-start;
      padding-top:20px;
      gap:18px;
    }

    .color-title{
      font-size:16px;
      font-weight:900;
      color:var(--yellow);
    }

    .color-input{
      width:86%;
      height:44px;
      border-radius:8px;
      padding:0;
      border:0;
      background:transparent;
      cursor:pointer;
    }

    .color-help{
      text-align:center;
      font-size:12px;
      font-weight:800;
      color:#dffcff;
      max-width:360px;
      line-height:1.4;
    }

    .toast{
      position:fixed;
      left:12px;
      right:12px;
      bottom:76px;
      z-index:14000;
      display:none;
      border:1px solid var(--accent);
      border-radius:14px;
      background:rgba(0,18,28,.96);
      color:var(--text);
      padding:12px;
      font-size:13px;
      font-weight:800;
      box-shadow:0 0 18px color-mix(in srgb, var(--accent) 35%, transparent);
    }

    .toast.show{display:block;}

    @media (max-width:420px){
      .menu-window{
        width:100vw;
        height:78vh;
        grid-template-columns:78px 1fr;
      }

      .side-title{
        font-size:16px;
      }

      .side-btn{
        width:52px;
        height:52px;
        font-size:22px;
      }

      .mesa-list{
        grid-template-columns:1fr;
      }

      .alias-grid{
        grid-template-columns:1fr 1fr;
        gap:8px;
      }
    }

    @media (min-width:520px){
      .app{
        max-width:430px;
        margin:0 auto;
      }
    }
  </style>
</head>

<body>
  <div id="stage">
    <main class="app">

      <section class="topbar">
        <div class="logo">✣GAMBT</div>

        <div class="top-grid">
          <div class="top-pill socials">f 𝕏 ◎ ▶ ♪</div>
          <div class="top-pill">🇪🇸 Español</div>
          <div class="top-pill">⚙ Ajustes</div>
          <div class="top-pill">👤 @pablico</div>
        </div>
      </section>

      <section class="stats">
        <div class="stat-card">
          <div class="stat-title">Saldo</div>
          <div class="stat-value">$30.00</div>
          <div class="btn-recargar">RECARGAR +</div>
        </div>

        <div class="stat-card">
          <div class="stat-title">Puntos</div>
          <div class="stat-value">0 pts</div>
          <div class="stat-small">Nivel 0<br>Ranking: #0 de 0</div>
        </div>

        <div class="stat-card">
          <div class="stat-title">Retos activos</div>
          <div class="stat-value" id="statActivos">1</div>
          <div class="stat-small">Buena suerte!</div>
        </div>

        <div class="stat-card">
          <div class="stat-title">Retos cerrados</div>
          <div class="stat-value" id="statCerrados">0</div>
        </div>
      </section>

      <h1 class="title-main">OPEN / CLOSED CHALLENGES</h1>

      <section class="tabs">
        <button class="tab-btn active" id="btnAbiertos" type="button">Retos Abiertos</button>
        <button class="tab-btn" id="btnCerrados" type="button">Retos Cerrados</button>
      </section>

      <section class="panel">
        <div class="section-title" id="mainTitle">Selecciona un reto abierto</div>

        <div class="field-label">Ficha de reto</div>
        <select id="mesaSelect">
          <option value="">Selecciona nombre de mesa</option>
        </select>

        <div id="fichaContainer" style="margin-top:12px;">
          <div class="empty">Primero selecciona el nombre de la mesa.</div>
        </div>
      </section>

      <section class="panel hidden" id="participantesPanel">
        <div class="participants-head">
          <div class="section-title">Participantes del reto</div>
          <input id="buscarUsuario" type="search" placeholder="Buscar usuario..." />
        </div>

        <div id="participantesContainer"></div>
      </section>

    </main>

    <nav class="bottom-menu">
      <button class="bottom-item" data-open="mensajes" type="button">💬</button>
      <button class="bottom-item" data-open="usuarios" type="button">👤</button>
      <button class="bottom-item" data-open="mesas" type="button">▦</button>
      <button class="bottom-item" data-open="notificaciones" type="button">🔔</button>
      <button class="bottom-item" data-open="configuracion" type="button">⚙</button>
    </nav>

    <div class="overlay" id="menuOverlay">
      <section class="menu-window">
        <aside class="side-menu">
          <div class="side-title">MENU</div>

          <div class="side-icons">
            <button class="side-btn" data-open="mensajes" type="button">💬</button>
            <button class="side-btn" data-open="usuarios" type="button">👤</button>
            <button class="side-btn" data-open="mesas" type="button">▦</button>
            <button class="side-btn" data-open="notificaciones" type="button">🔔</button>
            <button class="side-btn" data-open="configuracion" type="button">⚙</button>
          </div>
        </aside>

        <section class="menu-content">
          <header class="content-head">
            <div class="content-title" id="menuTitle">MENSAJES</div>
            <button class="close-btn" id="closeOverlay" type="button">↻</button>
          </header>

          <div class="content-body" id="menuBody"></div>
        </section>
      </section>
    </div>

    <div class="toast" id="toast"></div>
  </div>

  <script>
    (function(){
      var fe = window.frameElement;
      if (fe){
        fe.style.position = "fixed";
        fe.style.inset = "0";
        fe.style.width = "100vw";
        fe.style.height = "100vh";
        fe.style.border = "0";
        fe.style.margin = "0";
        fe.style.padding = "0";
        fe.style.zIndex = "999999";
        fe.style.background = "transparent";
      }

      const DATA = {
        abiertos: [
          {
            id: "mesa_diana_open",
            nombreMesa: "Creo mesa privada - Diana",
            partido: "Club Atlético de Madrid vs Athletic Club",
            estado: "Retos Abiertos",
            ganador: "NO_APLICA",
            golAmbos: "X",
            penales: "No",
            marcador: "X",
            apuestas: "1",
            apuesta: "$3.00",
            participantes: [
              {usuario:"test1234", partido:"Club Atlético de Madrid vs Athletic Club", ganador:"NO_APLICA", golAmbos:"X", penales:"No", marcador:"X", participantes:"3", bolsa:"$9.00"},
              {usuario:"pablico", partido:"Club Atlético de Madrid vs Athletic Club", ganador:"NO_APLICA", golAmbos:"X", penales:"No", marcador:"X", participantes:"3", bolsa:"$9.00"},
              {usuario:"Diana", partido:"Club Atlético de Madrid vs Athletic Club", ganador:"NO_APLICA", golAmbos:"X", penales:"No", marcador:"X", participantes:"3", bolsa:"$9.00"}
            ]
          },
          {
            id: "mesa_pablico_open",
            nombreMesa: "Mesa pública - pablico",
            partido: "Real Madrid vs Barcelona",
            estado: "Retos Abiertos",
            ganador: "NO_APLICA",
            golAmbos: "Sí",
            penales: "No",
            marcador: "2-1",
            apuestas: "2",
            apuesta: "$5.00",
            participantes: [
              {usuario:"pablico", partido:"Real Madrid vs Barcelona", ganador:"Real Madrid", golAmbos:"Sí", penales:"No", marcador:"2-1", participantes:"2", bolsa:"$10.00"},
              {usuario:"Blanco", partido:"Real Madrid vs Barcelona", ganador:"Barcelona", golAmbos:"Sí", penales:"No", marcador:"1-2", participantes:"2", bolsa:"$10.00"}
            ]
          }
        ],
        cerrados: [
          {
            id: "mesa_cerrada_1",
            nombreMesa: "Mesa cerrada - Enano",
            partido: "Manchester City vs Liverpool",
            estado: "Retos Cerrados",
            ganador: "Manchester City",
            golAmbos: "Sí",
            penales: "No",
            marcador: "3-2",
            apuestas: "4",
            apuesta: "$4.00",
            participantes: [
              {usuario:"Enano", partido:"Manchester City vs Liverpool", ganador:"Manchester City", golAmbos:"Sí", penales:"No", marcador:"3-2", participantes:"4", bolsa:"$16.00"},
              {usuario:"Gym", partido:"Manchester City vs Liverpool", ganador:"Liverpool", golAmbos:"Sí", penales:"No", marcador:"2-3", participantes:"4", bolsa:"$16.00"},
              {usuario:"Hulk", partido:"Manchester City vs Liverpool", ganador:"Manchester City", golAmbos:"Sí", penales:"No", marcador:"3-2", participantes:"4", bolsa:"$16.00"},
              {usuario:"Fantasma", partido:"Manchester City vs Liverpool", ganador:"Empate", golAmbos:"Sí", penales:"No", marcador:"2-2", participantes:"4", bolsa:"$16.00"}
            ]
          }
        ]
      };

      const USUARIOS = [
        "@Blanco",
        "@cristihan_gc",
        "@David",
        "@Diana",
        "@EliasMuki",
        "@Enano",
        "@Fantasma",
        "@Gym",
        "@Hulk",
        "@pablico"
      ];

      const MESAS_USUARIO = [
        {nombre:"Celular - test1234", participantes:"1 participantes"},
        {nombre:"Creo mesa privada - Diana", participantes:"3 participantes"},
        {nombre:"Prueba celular - cristhian_gc", participantes:"1 participantes"}
      ];

      const NOTIFICACIONES = [
        {titulo:"@Diana", texto:"Envió mensaje en Creo mesa privada - Diana"},
        {titulo:"Mesa pública - pablico", texto:"Nuevo mensaje recibido"}
      ];

      let modoActual = "abiertos";
      let mesaActual = "";
      let filtroUsuario = "";

      const btnAbiertos = document.getElementById("btnAbiertos");
      const btnCerrados = document.getElementById("btnCerrados");
      const mesaSelect = document.getElementById("mesaSelect");
      const fichaContainer = document.getElementById("fichaContainer");
      const participantesPanel = document.getElementById("participantesPanel");
      const participantesContainer = document.getElementById("participantesContainer");
      const buscarUsuario = document.getElementById("buscarUsuario");
      const mainTitle = document.getElementById("mainTitle");
      const statActivos = document.getElementById("statActivos");
      const statCerrados = document.getElementById("statCerrados");
      const toast = document.getElementById("toast");

      const overlay = document.getElementById("menuOverlay");
      const menuTitle = document.getElementById("menuTitle");
      const menuBody = document.getElementById("menuBody");
      const closeOverlay = document.getElementById("closeOverlay");

      function esc(value){
        return String(value ?? "")
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;")
          .replaceAll('"', "&quot;")
          .replaceAll("'", "&#039;");
      }

      function showToast(text){
        toast.textContent = text;
        toast.classList.add("show");
        setTimeout(function(){
          toast.classList.remove("show");
        }, 1700);
      }

      function getMesas(){
        return DATA[modoActual] || [];
      }

      function getMesaSeleccionada(){
        return getMesas().find(function(m){ return m.id === mesaActual; });
      }

      function renderStats(){
        statActivos.textContent = DATA.abiertos.length;
        statCerrados.textContent = DATA.cerrados.length;
      }

      function renderTabs(){
        btnAbiertos.classList.toggle("active", modoActual === "abiertos");
        btnCerrados.classList.toggle("active", modoActual === "cerrados");

        mainTitle.textContent = modoActual === "abiertos"
          ? "Selecciona un reto abierto"
          : "Selecciona un reto cerrado";
      }

      function renderMesaSelect(){
        const mesas = getMesas();
        let html = '<option value="">Selecciona nombre de mesa</option>';

        mesas.forEach(function(mesa){
          html += '<option value="' + esc(mesa.id) + '">' + esc(mesa.nombreMesa) + '</option>';
        });

        mesaSelect.innerHTML = html;
        mesaSelect.value = mesaActual;
      }

      function renderFicha(){
        const mesa = getMesaSeleccionada();

        if (!mesa){
          fichaContainer.innerHTML = '<div class="empty">Primero selecciona el nombre de la mesa.</div>';
          return;
        }

        const puedeEditar = modoActual === "abiertos";

        fichaContainer.innerHTML = `
          <div class="ficha">
            <div class="ficha-row"><div class="ficha-k">Nombre Mesa</div><div class="ficha-v">${esc(mesa.nombreMesa)}</div></div>
            <div class="ficha-row"><div class="ficha-k">Partido</div><div class="ficha-v">${esc(mesa.partido)}</div></div>
            <div class="ficha-row"><div class="ficha-k">Estado</div><div class="ficha-v">${esc(mesa.estado)}</div></div>
            <div class="ficha-row"><div class="ficha-k">Ganador</div><div class="ficha-v">${esc(mesa.ganador)}</div></div>
            <div class="ficha-row"><div class="ficha-k">Gol Ambos</div><div class="ficha-v">${esc(mesa.golAmbos)}</div></div>
            <div class="ficha-row"><div class="ficha-k">Penales</div><div class="ficha-v">${esc(mesa.penales)}</div></div>
            <div class="ficha-row"><div class="ficha-k">Marcador</div><div class="ficha-v">${esc(mesa.marcador)}</div></div>
            <div class="ficha-row"><div class="ficha-k">Apuestas</div><div class="ficha-v">${esc(mesa.apuestas)}</div></div>
            <div class="ficha-row"><div class="ficha-k">Apuesta</div><div class="ficha-v">${esc(mesa.apuesta)}</div></div>
            <div class="ficha-row">
              <div class="ficha-k">Acciones</div>
              <div class="ficha-v">
                <div class="actions">
                  <button class="action-btn" data-action="ver" type="button" title="Ver">👁</button>
                  <button class="action-btn" data-action="estadistica" type="button" title="Estadística">📊</button>
                  <button class="action-btn ${puedeEditar ? "" : "disabled"}" data-action="editar" type="button" title="Editar">✎</button>
                </div>
              </div>
            </div>
          </div>
        `;

        fichaContainer.querySelectorAll(".action-btn").forEach(function(btn){
          btn.addEventListener("click", function(){
            const action = btn.getAttribute("data-action");

            if (action === "editar" && modoActual === "cerrados"){
              showToast("Reto cerrado: el lápiz está deshabilitado.");
              return;
            }

            if (action === "ver") showToast("Ver reto: " + mesa.nombreMesa);
            if (action === "estadistica") showToast("Estadísticas: " + mesa.nombreMesa);
            if (action === "editar") showToast("Editar indicadores: " + mesa.nombreMesa);
          });
        });
      }

      function renderParticipantes(){
        const mesa = getMesaSeleccionada();

        if (!mesa){
          participantesPanel.classList.add("hidden");
          participantesContainer.innerHTML = "";
          return;
        }

        participantesPanel.classList.remove("hidden");

        const filtro = filtroUsuario.trim().toLowerCase();

        const participantes = mesa.participantes.filter(function(p){
          if (!filtro) return true;

          return (
            p.usuario.toLowerCase().includes(filtro) ||
            p.partido.toLowerCase().includes(filtro) ||
            p.ganador.toLowerCase().includes(filtro)
          );
        });

        if (!participantes.length){
          participantesContainer.innerHTML = '<div class="empty">No hay participantes con ese filtro.</div>';
          return;
        }

        participantesContainer.innerHTML = participantes.map(function(p){
          return `
            <article class="participant-card">
              <div class="participant-title">${esc(p.usuario)}</div>
              <div class="mini-grid">
                <div class="mini-item"><div class="mini-k">Partido</div><div class="mini-v">${esc(p.partido)}</div></div>
                <div class="mini-item"><div class="mini-k">Ganador</div><div class="mini-v">${esc(p.ganador)}</div></div>
                <div class="mini-item"><div class="mini-k">Gol Ambos</div><div class="mini-v">${esc(p.golAmbos)}</div></div>
                <div class="mini-item"><div class="mini-k">Penales</div><div class="mini-v">${esc(p.penales)}</div></div>
                <div class="mini-item"><div class="mini-k">Marcador</div><div class="mini-v">${esc(p.marcador)}</div></div>
                <div class="mini-item"><div class="mini-k">Bolsa</div><div class="mini-v">${esc(p.bolsa)}</div></div>
              </div>
            </article>
          `;
        }).join("");
      }

      function renderAll(){
        renderStats();
        renderTabs();
        renderMesaSelect();
        renderFicha();
        renderParticipantes();
      }

      function setActiveMenu(type){
        document.querySelectorAll(".side-btn, .bottom-item").forEach(function(btn){
          btn.classList.toggle("active", btn.getAttribute("data-open") === type);
        });
      }

      function openPanel(type){
        overlay.classList.add("show");
        setActiveMenu(type);

        if (type === "mensajes") renderMensajes();
        if (type === "usuarios") renderUsuariosPanel();
        if (type === "mesas") renderMesasPanel();
        if (type === "notificaciones") renderNotificacionesPanel();
        if (type === "configuracion") renderConfiguracionPanel();
      }

      function renderMensajes(){
        menuTitle.textContent = "MENSAJES";
        menuBody.innerHTML = `
          <div class="message-box">
            <div></div>
            <div class="message-line">
              <input id="mensajeInput" type="text" placeholder="Escribe un mensaje..." />
              <button class="send-btn" id="sendMsg" type="button">SEND</button>
            </div>
          </div>
        `;

        document.getElementById("sendMsg").addEventListener("click", function(){
          const msg = document.getElementById("mensajeInput").value.trim();
          if (!msg) return;
          document.getElementById("mensajeInput").value = "";
          showToast("Mensaje enviado.");
        });
      }

      function renderUsuariosPanel(){
        menuTitle.textContent = "USUARIOS";

        menuBody.innerHTML = `
          <input id="buscarAliasPanel" type="search" placeholder="Buscar alias..." />
          <div class="alias-grid" id="aliasGridPanel"></div>
        `;

        const input = document.getElementById("buscarAliasPanel");
        const grid = document.getElementById("aliasGridPanel");

        function draw(){
          const filtro = input.value.trim().toLowerCase();
          const usuarios = USUARIOS.filter(function(alias){
            return !filtro || alias.toLowerCase().includes(filtro);
          });

          grid.innerHTML = usuarios.map(function(alias){
            return '<div class="alias">' + esc(alias) + '</div>';
          }).join("");
        }

        input.addEventListener("input", draw);
        draw();
      }

      function renderMesasPanel(){
        menuTitle.textContent = "MESAS ABIERTAS";

        menuBody.innerHTML = `
          <input id="buscarMesaPanel" type="search" placeholder="Buscar mesa..." />
          <div class="mesa-list" id="mesaListPanel"></div>
        `;

        const input = document.getElementById("buscarMesaPanel");
        const list = document.getElementById("mesaListPanel");

        function draw(){
          const filtro = input.value.trim().toLowerCase();
          const mesas = MESAS_USUARIO.filter(function(mesa){
            return !filtro || mesa.nombre.toLowerCase().includes(filtro);
          });

          list.innerHTML = mesas.map(function(mesa){
            return `
              <div class="mesa-item">
                <strong>${esc(mesa.nombre)}</strong>
                <span>${esc(mesa.participantes)}</span>
              </div>
            `;
          }).join("");
        }

        input.addEventListener("input", draw);
        draw();
      }

      function renderNotificacionesPanel(){
        menuTitle.textContent = "NOTIFICACIONES";

        if (!NOTIFICACIONES.length){
          menuBody.innerHTML = '<div class="center-empty">No hay notificaciones</div>';
          return;
        }

        menuBody.innerHTML = `
          <div class="notif-list">
            ${NOTIFICACIONES.map(function(n){
              return `
                <div class="notif-item">
                  <strong>${esc(n.titulo)}</strong><br>
                  ${esc(n.texto)}
                </div>
              `;
            }).join("")}
          </div>
        `;
      }

      function renderConfiguracionPanel(){
        menuTitle.textContent = "CONFIGURACIÓN";

        menuBody.innerHTML = `
          <div class="color-panel">
            <div class="color-title">Color primario</div>
            <input class="color-input" id="colorPicker" type="color" value="#00e5ff" />
            <div class="color-help">Cambia el color de acento (bordes, sombras, iconos, títulos)</div>
          </div>
        `;

        document.getElementById("colorPicker").addEventListener("input", function(e){
          document.documentElement.style.setProperty("--accent", e.target.value);
          document.documentElement.style.setProperty("--accent-soft", e.target.value + "22");
        });
      }

      btnAbiertos.addEventListener("click", function(){
        modoActual = "abiertos";
        mesaActual = "";
        filtroUsuario = "";
        buscarUsuario.value = "";
        renderAll();
      });

      btnCerrados.addEventListener("click", function(){
        modoActual = "cerrados";
        mesaActual = "";
        filtroUsuario = "";
        buscarUsuario.value = "";
        renderAll();
      });

      mesaSelect.addEventListener("change", function(){
        mesaActual = mesaSelect.value;
        filtroUsuario = "";
        buscarUsuario.value = "";
        renderFicha();
        renderParticipantes();
      });

      buscarUsuario.addEventListener("input", function(){
        filtroUsuario = buscarUsuario.value;
        renderParticipantes();
      });

      document.querySelectorAll("[data-open]").forEach(function(btn){
        btn.addEventListener("click", function(){
          openPanel(btn.getAttribute("data-open"));
        });
      });

      closeOverlay.addEventListener("click", function(){
        overlay.classList.remove("show");
        setActiveMenu("");
      });

      overlay.addEventListener("click", function(e){
        if (e.target === overlay){
          overlay.classList.remove("show");
          setActiveMenu("");
        }
      });

      renderAll();
    })();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
