# app.py
import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES =====
PAD_X_PX = 8
PAD_TOP_PX = 8
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"
# ===================

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

html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <style>
    :root{{
      --padx:{PAD_X_PX}px;
      --padtop:{PAD_TOP_PX}px;
      --b:{BORDER_PX}px;
      --bc:{BORDER_COLOR};
      --bg:{BG_COLOR};

      --cyan:#00e5ff;
      --cyan-dark:#003b46;
      --yellow:#ffee32;
      --panel:#061923;
      --panel2:#082632;
      --text:#e9fbff;
      --muted:#9fb5c3;
      --danger:#ff5f73;
      --ok:#36ff9f;
    }}

    *{{
      box-sizing:border-box;
    }}

    html, body{{
      margin:0;
      padding:0;
      width:100%;
      height:100%;
      overflow:hidden;
      background:var(--bg);
      font-family:Arial, Helvetica, sans-serif;
    }}

    #stage{{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      overflow-y:auto;
      overflow-x:hidden;
      -webkit-overflow-scrolling:touch;
      background:
        radial-gradient(circle at 50% 12%, rgba(0,229,255,.20), transparent 28%),
        linear-gradient(180deg, #06111b 0%, #071926 45%, #051018 100%);
      color:var(--text);
    }}

    .app{{
      width:100%;
      min-height:100vh;
      padding:10px 10px 92px 10px;
    }}

    .topbar{{
      border:1px solid rgba(0,229,255,.65);
      border-radius:18px;
      padding:10px;
      background:rgba(0,0,0,.42);
      box-shadow:0 0 18px rgba(0,229,255,.25);
      margin-bottom:10px;
    }}

    .logo{{
      width:100%;
      text-align:center;
      font-size:30px;
      font-weight:900;
      letter-spacing:3px;
      color:#9dffbd;
      text-shadow:0 0 14px rgba(0,229,255,.65);
      line-height:1;
      margin-bottom:10px;
    }}

    .top-grid{{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:8px;
    }}

    .top-pill{{
      border:1px solid rgba(0,229,255,.65);
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
    }}

    .socials{{
      display:flex;
      justify-content:center;
      gap:10px;
      font-size:15px;
    }}

    .stats{{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:8px;
      margin-bottom:12px;
    }}

    .stat-card{{
      border:1px solid rgba(0,229,255,.75);
      border-radius:14px;
      padding:10px;
      background:rgba(0,10,18,.72);
      min-height:80px;
      box-shadow:0 0 12px rgba(0,229,255,.18);
    }}

    .stat-title{{
      color:var(--yellow);
      font-size:10px;
      font-weight:900;
      text-transform:uppercase;
      margin-bottom:8px;
    }}

    .stat-value{{
      font-size:21px;
      font-weight:900;
      color:var(--text);
    }}

    .stat-small{{
      font-size:10px;
      color:#bcefff;
      margin-top:5px;
      line-height:1.3;
    }}

    .btn-recargar{{
      display:inline-flex;
      margin-top:8px;
      padding:4px 9px;
      border-radius:999px;
      background:var(--cyan);
      color:#001018;
      font-weight:900;
      font-size:10px;
    }}

    .title-main{{
      font-size:21px;
      line-height:1;
      color:var(--yellow);
      font-weight:1000;
      text-transform:uppercase;
      text-shadow:0 0 12px rgba(255,238,50,.75);
      margin:16px 0 10px 0;
    }}

    .tabs{{
      display:grid;
      grid-template-columns:1fr 1fr;
      border:1px solid var(--yellow);
      border-radius:14px 14px 0 0;
      overflow:hidden;
      background:rgba(0,0,0,.5);
    }}

    .tab-btn{{
      border:0;
      padding:13px 8px;
      font-size:13px;
      font-weight:900;
      color:var(--text);
      background:transparent;
      cursor:pointer;
      text-transform:uppercase;
    }}

    .tab-btn.active{{
      color:var(--yellow);
      background:rgba(255,238,50,.13);
      box-shadow:inset 0 -3px 0 var(--yellow);
    }}

    .panel{{
      border:1px solid rgba(255,238,50,.85);
      border-top:0;
      border-radius:0 0 14px 14px;
      background:rgba(0,12,18,.72);
      padding:12px;
      box-shadow:0 0 15px rgba(255,238,50,.18);
      margin-bottom:14px;
    }}

    .section-title{{
      color:var(--yellow);
      font-size:16px;
      font-weight:900;
      margin-bottom:10px;
      line-height:1.1;
    }}

    .field-label{{
      font-size:11px;
      font-weight:900;
      color:var(--yellow);
      margin-bottom:5px;
      text-transform:uppercase;
    }}

    select, input{{
      width:100%;
      border:1px solid rgba(0,229,255,.85);
      background:rgba(0,20,30,.88);
      color:var(--text);
      border-radius:999px;
      min-height:39px;
      padding:0 12px;
      outline:none;
      font-size:13px;
      font-weight:700;
    }}

    .ficha{{
      margin-top:12px;
      border:1px solid rgba(0,229,255,.65);
      border-radius:14px;
      background:rgba(0,23,34,.72);
      overflow:hidden;
    }}

    .ficha-row{{
      display:grid;
      grid-template-columns:42% 58%;
      border-bottom:1px solid rgba(255,255,255,.14);
      min-height:38px;
    }}

    .ficha-row:last-child{{
      border-bottom:0;
    }}

    .ficha-k{{
      padding:10px;
      font-size:11px;
      font-weight:900;
      color:var(--yellow);
      background:rgba(255,238,50,.08);
      display:flex;
      align-items:center;
    }}

    .ficha-v{{
      padding:10px;
      font-size:12px;
      font-weight:800;
      color:var(--text);
      display:flex;
      align-items:center;
      overflow-wrap:anywhere;
    }}

    .actions{{
      display:flex;
      gap:8px;
      align-items:center;
      flex-wrap:wrap;
    }}

    .action-btn{{
      width:34px;
      height:34px;
      border-radius:999px;
      border:1px solid rgba(0,229,255,.8);
      background:rgba(0,229,255,.12);
      color:var(--cyan);
      display:inline-flex;
      align-items:center;
      justify-content:center;
      font-size:16px;
      cursor:pointer;
    }}

    .action-btn.disabled{{
      opacity:.28;
      cursor:not-allowed;
      filter:grayscale(1);
    }}

    .empty{{
      border:1px dashed rgba(255,255,255,.28);
      border-radius:14px;
      padding:14px;
      font-size:13px;
      color:var(--muted);
      text-align:center;
      background:rgba(255,255,255,.04);
    }}

    .participants-head{{
      display:grid;
      grid-template-columns:1fr;
      gap:8px;
      margin-bottom:10px;
    }}

    .participant-card{{
      border:1px solid rgba(0,229,255,.65);
      border-radius:14px;
      background:rgba(0,17,27,.76);
      overflow:hidden;
      margin-bottom:10px;
      box-shadow:0 0 10px rgba(0,229,255,.12);
    }}

    .participant-title{{
      padding:10px 12px;
      font-size:14px;
      font-weight:900;
      color:var(--text);
      border-bottom:1px solid rgba(255,255,255,.12);
      background:rgba(0,229,255,.08);
    }}

    .mini-grid{{
      display:grid;
      grid-template-columns:1fr 1fr;
    }}

    .mini-item{{
      min-height:42px;
      padding:8px 10px;
      border-right:1px solid rgba(255,255,255,.10);
      border-bottom:1px solid rgba(255,255,255,.10);
    }}

    .mini-item:nth-child(2n){{
      border-right:0;
    }}

    .mini-k{{
      color:var(--yellow);
      font-size:10px;
      font-weight:900;
      margin-bottom:4px;
      text-transform:uppercase;
    }}

    .mini-v{{
      color:var(--text);
      font-size:12px;
      font-weight:800;
      line-height:1.25;
      overflow-wrap:anywhere;
    }}

    .users-panel{{
      border:1px solid rgba(0,229,255,.75);
      border-radius:14px;
      background:rgba(0,12,18,.72);
      padding:12px;
      box-shadow:0 0 15px rgba(0,229,255,.18);
      margin-bottom:14px;
    }}

    .users-grid{{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:8px;
      margin-top:10px;
      max-height:170px;
      overflow-y:auto;
      padding-right:4px;
    }}

    .alias{{
      border:1px solid rgba(0,229,255,.35);
      background:rgba(0,229,255,.12);
      color:#dffcff;
      border-radius:999px;
      padding:7px 9px;
      font-size:12px;
      font-weight:800;
      overflow:hidden;
      text-overflow:ellipsis;
      white-space:nowrap;
    }}

    .bottom-menu{{
      position:fixed;
      left:0;
      right:0;
      bottom:0;
      z-index:9999;
      background:rgba(0,12,18,.96);
      border-top:1px solid rgba(0,229,255,.75);
      box-shadow:0 -8px 22px rgba(0,229,255,.18);
      padding:8px 8px 10px 8px;
      display:grid;
      grid-template-columns:repeat(5, 1fr);
      gap:8px;
    }}

    .bottom-item{{
      height:46px;
      border:1px solid rgba(0,229,255,.65);
      border-radius:14px;
      background:rgba(0,229,255,.10);
      color:var(--cyan);
      display:flex;
      align-items:center;
      justify-content:center;
      font-size:20px;
      font-weight:900;
    }}

    .toast{{
      position:fixed;
      left:12px;
      right:12px;
      bottom:76px;
      z-index:10000;
      display:none;
      border:1px solid rgba(0,229,255,.75);
      border-radius:14px;
      background:rgba(0,18,28,.96);
      color:var(--text);
      padding:12px;
      font-size:13px;
      font-weight:800;
      box-shadow:0 0 18px rgba(0,229,255,.32);
    }}

    .toast.show{{
      display:block;
    }}

    @media (min-width:520px){{
      .app{{
        max-width:430px;
        margin:0 auto;
      }}
    }}
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

      <section class="panel">
        <div class="participants-head">
          <div class="section-title">Participantes del reto</div>
          <input id="buscarUsuario" type="search" placeholder="Buscar usuario..." />
        </div>

        <div id="participantesContainer">
          <div class="empty">Sin mesa seleccionada.</div>
        </div>
      </section>

      <section class="users-panel">
        <div class="section-title">Usuarios</div>
        <input id="buscarAlias" type="search" placeholder="Buscar alias..." />

        <div class="users-grid" id="usuariosGrid"></div>
      </section>

    </main>

    <nav class="bottom-menu">
      <div class="bottom-item">💬</div>
      <div class="bottom-item">👤</div>
      <div class="bottom-item">▦</div>
      <div class="bottom-item">🔔</div>
      <div class="bottom-item">⚙</div>
    </nav>

    <div class="toast" id="toast"></div>
  </div>

  <script>
    (function(){{
      var fe = window.frameElement;
      if (fe){{
        fe.style.position = "fixed";
        fe.style.inset = "0";
        fe.style.width = "100vw";
        fe.style.height = "100vh";
        fe.style.border = "0";
        fe.style.margin = "0";
        fe.style.padding = "0";
        fe.style.zIndex = "999999";
        fe.style.background = "transparent";
      }}

      const DATA = {{
        abiertos: [
          {{
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
              {{
                usuario: "test1234",
                partido: "Club Atlético de Madrid vs Athletic Club",
                ganador: "NO_APLICA",
                golAmbos: "X",
                penales: "No",
                marcador: "X",
                participantes: "3",
                bolsa: "$9.00"
              }},
              {{
                usuario: "pablico",
                partido: "Club Atlético de Madrid vs Athletic Club",
                ganador: "NO_APLICA",
                golAmbos: "X",
                penales: "No",
                marcador: "X",
                participantes: "3",
                bolsa: "$9.00"
              }},
              {{
                usuario: "Diana",
                partido: "Club Atlético de Madrid vs Athletic Club",
                ganador: "NO_APLICA",
                golAmbos: "X",
                penales: "No",
                marcador: "X",
                participantes: "3",
                bolsa: "$9.00"
              }}
            ]
          }},
          {{
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
              {{
                usuario: "pablico",
                partido: "Real Madrid vs Barcelona",
                ganador: "Real Madrid",
                golAmbos: "Sí",
                penales: "No",
                marcador: "2-1",
                participantes: "2",
                bolsa: "$10.00"
              }},
              {{
                usuario: "Blanco",
                partido: "Real Madrid vs Barcelona",
                ganador: "Barcelona",
                golAmbos: "Sí",
                penales: "No",
                marcador: "1-2",
                participantes: "2",
                bolsa: "$10.00"
              }}
            ]
          }}
        ],

        cerrados: [
          {{
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
              {{
                usuario: "Enano",
                partido: "Manchester City vs Liverpool",
                ganador: "Manchester City",
                golAmbos: "Sí",
                penales: "No",
                marcador: "3-2",
                participantes: "4",
                bolsa: "$16.00"
              }},
              {{
                usuario: "Gym",
                partido: "Manchester City vs Liverpool",
                ganador: "Liverpool",
                golAmbos: "Sí",
                penales: "No",
                marcador: "2-3",
                participantes: "4",
                bolsa: "$16.00"
              }},
              {{
                usuario: "Hulk",
                partido: "Manchester City vs Liverpool",
                ganador: "Manchester City",
                golAmbos: "Sí",
                penales: "No",
                marcador: "3-2",
                participantes: "4",
                bolsa: "$16.00"
              }},
              {{
                usuario: "Fantasma",
                partido: "Manchester City vs Liverpool",
                ganador: "Empate",
                golAmbos: "Sí",
                penales: "No",
                marcador: "2-2",
                participantes: "4",
                bolsa: "$16.00"
              }}
            ]
          }}
        ]
      }};

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

      let modoActual = "abiertos";
      let mesaActual = "";
      let filtroUsuario = "";
      let filtroAlias = "";

      const btnAbiertos = document.getElementById("btnAbiertos");
      const btnCerrados = document.getElementById("btnCerrados");
      const mesaSelect = document.getElementById("mesaSelect");
      const fichaContainer = document.getElementById("fichaContainer");
      const participantesContainer = document.getElementById("participantesContainer");
      const buscarUsuario = document.getElementById("buscarUsuario");
      const buscarAlias = document.getElementById("buscarAlias");
      const usuariosGrid = document.getElementById("usuariosGrid");
      const mainTitle = document.getElementById("mainTitle");
      const statActivos = document.getElementById("statActivos");
      const statCerrados = document.getElementById("statCerrados");
      const toast = document.getElementById("toast");

      function esc(value){{
        return String(value ?? "")
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;")
          .replaceAll('"', "&quot;")
          .replaceAll("'", "&#039;");
      }}

      function showToast(text){{
        toast.textContent = text;
        toast.classList.add("show");
        setTimeout(function(){{
          toast.classList.remove("show");
        }}, 1700);
      }}

      function getMesas(){{
        return DATA[modoActual] || [];
      }}

      function getMesaSeleccionada(){{
        return getMesas().find(function(m){{ return m.id === mesaActual; }});
      }}

      function renderStats(){{
        statActivos.textContent = DATA.abiertos.length;
        statCerrados.textContent = DATA.cerrados.length;
      }}

      function renderTabs(){{
        btnAbiertos.classList.toggle("active", modoActual === "abiertos");
        btnCerrados.classList.toggle("active", modoActual === "cerrados");

        mainTitle.textContent = modoActual === "abiertos"
          ? "Selecciona un reto abierto"
          : "Selecciona un reto cerrado";
      }}

      function renderMesaSelect(){{
        const mesas = getMesas();

        let html = '<option value="">Selecciona nombre de mesa</option>';

        mesas.forEach(function(mesa){{
          html += '<option value="' + esc(mesa.id) + '">' + esc(mesa.nombreMesa) + '</option>';
        }});

        mesaSelect.innerHTML = html;
        mesaSelect.value = mesaActual;
      }}

      function renderFicha(){{
        const mesa = getMesaSeleccionada();

        if (!mesa){{
          fichaContainer.innerHTML = '<div class="empty">Primero selecciona el nombre de la mesa.</div>';
          return;
        }}

        const puedeEditar = modoActual === "abiertos";

        fichaContainer.innerHTML = `
          <div class="ficha">
            <div class="ficha-row">
              <div class="ficha-k">Nombre Mesa</div>
              <div class="ficha-v">${{esc(mesa.nombreMesa)}}</div>
            </div>

            <div class="ficha-row">
              <div class="ficha-k">Partido</div>
              <div class="ficha-v">${{esc(mesa.partido)}}</div>
            </div>

            <div class="ficha-row">
              <div class="ficha-k">Estado</div>
              <div class="ficha-v">${{esc(mesa.estado)}}</div>
            </div>

            <div class="ficha-row">
              <div class="ficha-k">Ganador</div>
              <div class="ficha-v">${{esc(mesa.ganador)}}</div>
            </div>

            <div class="ficha-row">
              <div class="ficha-k">Gol Ambos</div>
              <div class="ficha-v">${{esc(mesa.golAmbos)}}</div>
            </div>

            <div class="ficha-row">
              <div class="ficha-k">Penales</div>
              <div class="ficha-v">${{esc(mesa.penales)}}</div>
            </div>

            <div class="ficha-row">
              <div class="ficha-k">Marcador</div>
              <div class="ficha-v">${{esc(mesa.marcador)}}</div>
            </div>

            <div class="ficha-row">
              <div class="ficha-k">Apuestas</div>
              <div class="ficha-v">${{esc(mesa.apuestas)}}</div>
            </div>

            <div class="ficha-row">
              <div class="ficha-k">Apuesta</div>
              <div class="ficha-v">${{esc(mesa.apuesta)}}</div>
            </div>

            <div class="ficha-row">
              <div class="ficha-k">Acciones</div>
              <div class="ficha-v">
                <div class="actions">
                  <button class="action-btn" data-action="ver" type="button" title="Ver">👁</button>
                  <button class="action-btn" data-action="estadistica" type="button" title="Estadística">📊</button>
                  <button class="action-btn ${{puedeEditar ? "" : "disabled"}}" data-action="editar" type="button" title="Editar">✎</button>
                </div>
              </div>
            </div>
          </div>
        `;

        fichaContainer.querySelectorAll(".action-btn").forEach(function(btn){{
          btn.addEventListener("click", function(){{
            const action = btn.getAttribute("data-action");

            if (action === "editar" && modoActual === "cerrados"){{
              showToast("Reto cerrado: el lápiz está deshabilitado.");
              return;
            }}

            if (action === "ver"){{
              showToast("Ver reto: " + mesa.nombreMesa);
            }}

            if (action === "estadistica"){{
              showToast("Estadísticas: " + mesa.nombreMesa);
            }}

            if (action === "editar"){{
              showToast("Editar indicadores: " + mesa.nombreMesa);
            }}
          }});
        }});
      }}

      function renderParticipantes(){{
        const mesa = getMesaSeleccionada();

        if (!mesa){{
          participantesContainer.innerHTML = '<div class="empty">Sin mesa seleccionada.</div>';
          return;
        }}

        const filtro = filtroUsuario.trim().toLowerCase();

        const participantes = mesa.participantes.filter(function(p){{
          if (!filtro) return true;

          return (
            p.usuario.toLowerCase().includes(filtro) ||
            p.partido.toLowerCase().includes(filtro) ||
            p.ganador.toLowerCase().includes(filtro)
          );
        }});

        if (!participantes.length){{
          participantesContainer.innerHTML = '<div class="empty">No hay participantes con ese filtro.</div>';
          return;
        }}

        participantesContainer.innerHTML = participantes.map(function(p){{
          return `
            <article class="participant-card">
              <div class="participant-title">${{esc(p.usuario)}}</div>

              <div class="mini-grid">
                <div class="mini-item">
                  <div class="mini-k">Partido</div>
                  <div class="mini-v">${{esc(p.partido)}}</div>
                </div>

                <div class="mini-item">
                  <div class="mini-k">Ganador</div>
                  <div class="mini-v">${{esc(p.ganador)}}</div>
                </div>

                <div class="mini-item">
                  <div class="mini-k">Gol Ambos</div>
                  <div class="mini-v">${{esc(p.golAmbos)}}</div>
                </div>

                <div class="mini-item">
                  <div class="mini-k">Penales</div>
                  <div class="mini-v">${{esc(p.penales)}}</div>
                </div>

                <div class="mini-item">
                  <div class="mini-k">Marcador</div>
                  <div class="mini-v">${{esc(p.marcador)}}</div>
                </div>

                <div class="mini-item">
                  <div class="mini-k">Bolsa</div>
                  <div class="mini-v">${{esc(p.bolsa)}}</div>
                </div>
              </div>
            </article>
          `;
        }}).join("");
      }}

      function renderUsuarios(){{
        const filtro = filtroAlias.trim().toLowerCase();

        const usuarios = USUARIOS.filter(function(alias){{
          return !filtro || alias.toLowerCase().includes(filtro);
        }});

        usuariosGrid.innerHTML = usuarios.map(function(alias){{
          return '<div class="alias">' + esc(alias) + '</div>';
        }}).join("");
      }}

      function renderAll(){{
        renderStats();
        renderTabs();
        renderMesaSelect();
        renderFicha();
        renderParticipantes();
        renderUsuarios();
      }}

      btnAbiertos.addEventListener("click", function(){{
        modoActual = "abiertos";
        mesaActual = "";
        filtroUsuario = "";
        buscarUsuario.value = "";
        renderAll();
      }});

      btnCerrados.addEventListener("click", function(){{
        modoActual = "cerrados";
        mesaActual = "";
        filtroUsuario = "";
        buscarUsuario.value = "";
        renderAll();
      }});

      mesaSelect.addEventListener("change", function(){{
        mesaActual = mesaSelect.value;
        filtroUsuario = "";
        buscarUsuario.value = "";
        renderFicha();
        renderParticipantes();
      }});

      buscarUsuario.addEventListener("input", function(){{
        filtroUsuario = buscarUsuario.value;
        renderParticipantes();
      }});

      buscarAlias.addEventListener("input", function(){{
        filtroAlias = buscarAlias.value;
        renderUsuarios();
      }});

      renderAll();
    }})();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
