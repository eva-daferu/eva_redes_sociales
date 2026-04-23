# app.py
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
      .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
      section.main > div{padding:0 !important;margin:0 !important;}
      header, footer{display:none !important;}
      iframe{display:block !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

SECTION_TABS = {
    "UNIRSE MESA": ["Mesas activas", "Histórico de encuentros", "Histórico de apuestas"],
    "CREAR MESA": ["Elegir Deporte", "Configurar Encuentro", "Elegir Partidos", "Histórico de encuentros", "Histórico de apuestas"],
    "MESA JUGADOR": ["Mesas activas", "Histórico de encuentros", "Histórico de apuestas"],
    "MESA PRIVADA": ["Histórico de encuentros", "Histórico de apuestas", "Mesas privadas"],
}

html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"/>
  <title>GAMBT - Parley</title>
  <!-- Font Awesome para iconos (usado en el diseño original de parley_actual) -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    /* ===== ESTILOS BASE DE PLANO1 (ARQUITECTURA MÓVIL OBLIGATORIA) ===== */
    :root{
      --bg:#f3f3f3;
      --panel:#ffffff;
      --panel2:#f7f7f7;
      --line:#202020;
      --line2:#6d6d6d;
      --text:#111111;
      --muted:#555555;
      --soft:#e7e7e7;
      --neon-cyan: #00eaff;
      --neon-yellow: #ffe855;
      --neon-pink: #ff66cc;
    }

    *{box-sizing:border-box;}

    html,body{
      margin:0;
      padding:0;
      width:100%;
      height:100%;
      overflow:hidden;
      background:var(--bg);
      font-family:'Orbitron', Arial, sans-serif;
      color:var(--text);
    }

    #stage{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      margin:0;
      padding:0;
      background:var(--bg);
    }

    #phone{
      width:100vw;
      height:100vh;
      margin:0;
      padding:0;
      overflow:auto;
      background:var(--bg);
      border:none;
      border-radius:0;
      box-shadow:none;
    }

    #screen{
      min-height:100vh;
      padding:0;
      margin:0;
      display:flex;
      flex-direction:column;
      gap:10px;
    }

    /* ===== TOPBAR (adaptado de parley_actual con estilo neón pero estructura plano1) ===== */
    .topbar{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:8px;
      padding:8px 10px;
      background: linear-gradient(90deg, rgba(0,10,20,0.95) 0%, rgba(10,20,30,0.92) 100%);
      border-bottom:2px solid transparent;
      box-shadow:0 5px 25px rgba(0,234,255,0.3);
      backdrop-filter:blur(10px);
      border-image: linear-gradient(45deg, #00eaff, #ffe855, #ff66cc, #00eaff) 1;
      animation: borderNeon 3s linear infinite;
      color:white;
    }

    @keyframes borderNeon {
      0% { border-image-source: linear-gradient(45deg, #00eaff, #ffe855, #ff66cc, #00eaff); }
      25% { border-image-source: linear-gradient(45deg, #ffe855, #ff66cc, #00eaff, #ffe855); }
      50% { border-image-source: linear-gradient(45deg, #ff66cc, #00eaff, #ffe855, #ff66cc); }
      75% { border-image-source: linear-gradient(45deg, #00eaff, #ffe855, #ff66cc, #00eaff); }
      100% { border-image-source: linear-gradient(45deg, #ffe855, #ff66cc, #00eaff, #ffe855); }
    }

    .logo{
      min-width:100px;
      height:42px;
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:900;
      font-size:24px;
      background:transparent;
      border:none;
      text-decoration:none;
      color:white;
    }

    .logo span {
      background: linear-gradient(45deg, #00eaff, #ffe855, #ff66cc, #00eaff);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      text-shadow: 0 2px 15px rgba(0,234,255,0.3);
      font-size:24px;
    }

    .lang{
      min-width:100px;
      height:36px;
      border:1px solid #0ce3ff55;
      background: linear-gradient(180deg, #041a27, #041321);
      display:flex;
      align-items:center;
      justify-content:center;
      font-size:14px;
      font-weight:700;
      color:#c8f6ff;
      border-radius:999px;
      padding:0 12px;
      cursor:pointer;
      box-shadow:0 6px 20px #00e7ff22;
    }

    .user-menu-btn {
      display:flex;
      align-items:center;
      gap:6px;
      padding:6px 12px;
      border-radius:999px;
      border:1px solid #0ce3ff55;
      background: linear-gradient(180deg, #041a27, #041321);
      color:#c8f6ff;
      font-weight:700;
      font-size:13px;
      cursor:pointer;
    }

    /* ===== CONTENIDO PRINCIPAL ===== */
    .content-wrap{
      padding:10px;
      display:flex;
      flex-direction:column;
      gap:10px;
    }

    .cards{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:10px;
    }

    .card{
      background:var(--panel);
      border:1px solid var(--line);
      padding:12px;
      min-height:92px;
      border-radius:12px;
    }

    .card.full{
      grid-column:1 / -1;
      min-height:84px;
    }

    .card-title{
      font-size:12px;
      font-weight:700;
      text-transform:uppercase;
      margin-bottom:8px;
    }

    .card-value{
      font-size:24px;
      font-weight:900;
      line-height:1;
      margin-bottom:8px;
    }

    .mini{
      font-size:12px;
      line-height:1.25;
      color:var(--muted);
    }

    .action-btn{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      min-height:34px;
      padding:0 16px;
      border:1px solid var(--line);
      background:var(--soft);
      font-weight:900;
      font-size:14px;
      border-radius:8px;
      cursor:pointer;
    }

    .select-wrap{
      background:var(--panel);
      border:1px solid var(--line);
      padding:10px;
      border-radius:12px;
    }

    .select-label{
      font-size:12px;
      font-weight:700;
      text-transform:uppercase;
      margin-bottom:6px;
    }

    select{
      width:100%;
      height:40px;
      border:1px solid var(--line);
      background:#fff;
      color:var(--text);
      padding:0 10px;
      font-size:14px;
      font-weight:700;
      outline:none;
      border-radius:8px;
    }

    .tabs{
      display:grid;
      grid-template-columns:repeat(auto-fit, minmax(100px, 1fr));
      gap:8px;
    }

    .tab{
      min-height:40px;
      border:1px solid var(--line);
      background:var(--panel);
      color:var(--text);
      font-weight:700;
      font-size:12px;
      padding:8px 6px;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      cursor:pointer;
      border-radius:8px;
      transition: all 0.2s;
    }

    .tab.active{
      background:var(--soft);
      border-width:2px;
      border-color: var(--neon-cyan);
    }

    .panel{
      background:var(--panel);
      border:1px solid var(--line);
      padding:10px;
      border-radius:12px;
    }

    .panel-inner{
      border:1px solid var(--line2);
      padding:10px;
      background:#fff;
      border-radius:8px;
    }

    .title-row{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:8px;
      margin-bottom:12px;
    }

    .title-lg{
      font-size:18px;
      font-weight:900;
      text-transform:uppercase;
    }

    .search{
      height:38px;
      border:1px solid var(--line);
      padding:0 12px;
      background:#fff;
      color:var(--muted);
      display:flex;
      align-items:center;
      font-size:13px;
      min-width:140px;
      border-radius:20px;
    }

    .mesa-list{
      display:grid;
      grid-template-columns:1fr;
      gap:10px;
      max-height: 450px;
      overflow-y: auto;
    }

    .mesa-card{
      border:1px solid var(--line);
      background:var(--panel2);
      padding:12px;
      border-radius:12px;
      cursor:pointer;
    }

    .mesa-name{
      font-size:14px;
      font-weight:900;
      margin-bottom:8px;
    }

    .mesa-meta{
      font-size:13px;
      line-height:1.35;
      color:#222;
      margin-bottom:10px;
    }

    .mesa-btn{
      min-height:34px;
      border:1px solid var(--line);
      background:var(--soft);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:900;
      border-radius:8px;
    }

    .empty{
      min-height:200px;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      color:var(--muted);
      font-size:14px;
      font-weight:700;
      line-height:1.35;
    }

    /* Formularios */
    .form-stack{
      display:grid;
      grid-template-columns:1fr;
      gap:10px;
    }

    .field{
      border:1px solid var(--line);
      padding:12px;
      background:#fff;
      border-radius:8px;
    }

    .field-title{
      font-size:13px;
      font-weight:900;
      margin-bottom:10px;
    }

    .input{
      min-height:42px;
      border:1px solid var(--line2);
      background:#fff;
      color:#444;
      display:flex;
      align-items:center;
      padding:0 12px;
      font-weight:700;
      border-radius:8px;
    }

    .option-col{
      display:grid;
      grid-template-columns:1fr;
      gap:8px;
    }

    .option{
      min-height:44px;
      border:1px solid var(--line2);
      display:flex;
      align-items:center;
      justify-content:space-between;
      padding:10px 12px;
      font-weight:700;
      background:#fff;
      gap:10px;
      border-radius:8px;
    }

    .toggle{
      width:42px;
      height:24px;
      border:1px solid var(--line);
      background:#fff;
      position:relative;
      flex:0 0 auto;
      border-radius:12px;
    }

    .toggle::after{
      content:"";
      position:absolute;
      top:2px;
      left:20px;
      width:18px;
      height:18px;
      background:#bbb;
      border:1px solid var(--line);
      border-radius:50%;
    }

    .radio-line{
      display:flex;
      flex-wrap:wrap;
      gap:12px;
      color:#111;
      font-weight:700;
      font-size:13px;
    }

    .pick-cards{
      display:grid;
      grid-template-columns:1fr;
      gap:10px;
    }

    .pick-card{
      border:1px solid var(--line);
      background:var(--panel2);
      padding:12px;
      display:grid;
      grid-template-columns:36px 1fr;
      gap:10px;
      align-items:flex-start;
      cursor:pointer;
      border-radius:8px;
    }

    .pick-card.selected{
      border-width:2px;
      background:#ececec;
    }

    .pick-check{
      width:24px;
      height:24px;
      border:2px solid var(--line);
      background:#fff;
      margin-top:2px;
      position:relative;
      border-radius:4px;
    }

    .pick-card.selected .pick-check::after{
      content:"";
      position:absolute;
      inset:4px;
      background:#888;
    }

    .pick-title{
      font-size:15px;
      font-weight:900;
      margin-bottom:8px;
    }

    .pick-meta{
      font-size:13px;
      line-height:1.35;
      color:#222;
    }

    .pick-tag{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      min-height:28px;
      padding:0 10px;
      border:1px solid var(--line2);
      background:#fff;
      font-size:12px;
      font-weight:700;
      margin-top:8px;
      border-radius:20px;
    }

    .next-wrap{
      margin-top:12px;
      display:flex;
      justify-content:center;
    }

    .next-btn{
      min-height:42px;
      min-width:160px;
      padding:0 24px;
      border:1px solid var(--line);
      background:var(--soft);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:900;
      font-size:16px;
      border-radius:8px;
      cursor:pointer;
    }

    .history-table{
      border:1px solid var(--line2);
      overflow-x: auto;
    }

    .history-head,
    .history-row{
      display:grid;
      grid-template-columns:1.1fr 1.1fr 1.2fr .9fr .8fr;
    }

    .history-head div{
      background:var(--soft);
      padding:10px;
      border-right:1px solid var(--line2);
      font-weight:900;
    }

    .history-head div:last-child{
      border-right:none;
    }

    .history-row div{
      padding:10px;
      border-top:1px solid var(--line2);
      border-right:1px solid var(--line2);
      background:#fff;
      display:flex;
      align-items:center;
    }

    .history-row div:last-child{
      border-right:none;
    }

    /* ===== MODAL OVERLAY (adaptado de parley_actual) ===== */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.85);
      z-index: 9999;
      display: none;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(5px);
    }

    .modal-container {
      position: relative;
      background: linear-gradient(135deg, rgba(0,15,25,0.95) 0%, rgba(0,30,45,0.98) 100%);
      border: 2px solid #ffe855;
      border-radius: 16px;
      padding: 20px;
      width: 95%;
      max-width: 600px;
      max-height: 85vh;
      overflow-y: auto;
      box-shadow: 0 0 60px rgba(255,232,133,0.4);
      color: #d6f7ff;
    }

    .modal-close {
      position: absolute;
      right: 15px;
      top: 10px;
      font-size: 28px;
      cursor: pointer;
      color: #ffe855;
      background: none;
      border: none;
      z-index: 10;
    }

    .modal-title {
      font-size: 20px;
      font-weight: 800;
      color: #ffe855;
      margin-bottom: 15px;
      text-align: center;
    }

    .modal-subtitle {
      font-size: 14px;
      color: #00eaff;
      margin-bottom: 15px;
      text-align: center;
    }

    .prediction-item {
      background: rgba(0,30,45,0.6);
      border: 1px solid #00eaff33;
      border-radius: 12px;
      padding: 12px;
      margin-bottom: 15px;
    }

    .prediction-header {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      margin-bottom: 10px;
    }

    .prediction-team {
      font-weight: 700;
      color: #ffe855;
    }

    .prediction-options {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 8px;
    }

    .prediction-option {
      background: rgba(0,234,255,0.1);
      padding: 8px 12px;
      border-radius: 8px;
      cursor: pointer;
      border: 1px solid #00eaff;
      color: #d6f7ff;
      font-size: 13px;
      font-weight: 600;
      flex: 1 0 auto;
      text-align: center;
    }

    .prediction-option.selected {
      background: linear-gradient(135deg, #00eaff 0%, #00c8ff 100%);
      color: #00151f;
      border-color: #ffe855;
    }

    .modal-actions {
      display: flex;
      gap: 15px;
      justify-content: center;
      margin-top: 20px;
    }

    .btn-primary {
      background: linear-gradient(135deg, #00eaff 0%, #00c8ff 100%);
      color: #00151f;
      border: none;
      padding: 12px 25px;
      border-radius: 10px;
      font-weight: 800;
      cursor: pointer;
      text-transform: uppercase;
    }

    .btn-secondary {
      background: rgba(255,232,133,0.15);
      color: #ffe855;
      border: 2px solid #ffe855;
      padding: 12px 25px;
      border-radius: 10px;
      font-weight: 800;
      cursor: pointer;
    }

    /* Ajustes para móvil */
    @media (max-width:360px){
      .cards{ grid-template-columns:1fr; }
      .card.full{ grid-column:auto; }
      .tabs{ grid-template-columns:1fr; }
      .title-row{ flex-direction:column; align-items:stretch; }
    }

    /* Ocultar elementos según corresponda */
    .hidden { display: none !important; }
  </style>
</head>
<body>
  <div id="stage">
    <div id="phone">
      <div id="screen">
        <!-- TOPBAR con elementos de parley_actual -->
        <div class="topbar">
          <a href="#" class="logo" id="logo-link">
            <span>GAMBT</span>
          </a>
          <div class="lang" id="lang-toggle">
            <span>🇪🇸 Español</span>
          </div>
          <div class="user-menu-btn" id="user-menu">
            <i class="fas fa-user-circle"></i>
            <span id="user-name-top">@Invitado</span>
          </div>
        </div>

        <div class="content-wrap">
          <!-- Tarjetas de Saldo, Puntos, Modo Classic -->
          <div class="cards">
            <div class="card">
              <div class="card-title">Saldo virtual</div>
              <div class="card-value" id="saldo-usuario">$0.00</div>
              <div class="action-btn" id="btn-recargar">RECARGAR +</div>
            </div>

            <div class="card">
              <div class="card-title">Puntos ganados</div>
              <div class="card-value" id="user-puntos">0 pts</div>
              <div class="mini" id="user-nivel">Nivel 0</div>
              <div class="mini" id="user-posicion">Ranking: #0</div>
            </div>

            <div class="card full">
              <div class="card-title">Modo classic</div>
              <div class="mini">Cuotas en vivo, tickets tradicionales.</div>
              <div style="margin-top:10px;" class="action-btn" id="btn-entrar-classic">Entrar</div>
            </div>
          </div>

          <!-- Selector de sección (UNIRSE MESA, CREAR MESA, etc) -->
          <div class="select-wrap">
            <div class="select-label">Sección</div>
            <select id="sectionSelect"></select>
          </div>

          <!-- Tabs dinámicos -->
          <div id="tabs" class="tabs"></div>
          
          <!-- Contenido dinámico -->
          <div id="content"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL PARA PREDICCIONES (unirse a mesa / crear reto / privado) -->
  <div class="modal-overlay" id="modal-overlay">
    <div class="modal-container" id="modal-predicciones">
      <button class="modal-close" id="modal-close">&times;</button>
      <div class="modal-title" id="modal-titulo">Predicciones</div>
      <div class="modal-subtitle" id="modal-subtitulo">Selecciona tus predicciones para cada partido</div>
      <div id="modal-contenido"></div>
      <div class="modal-actions">
        <button class="btn-primary" id="modal-enviar">Enviar</button>
        <button class="btn-secondary" id="modal-cancelar">Cancelar</button>
      </div>
    </div>
  </div>

  <!-- MODAL PARA CONTRASEÑA DE MESA PRIVADA (se reutiliza el mismo overlay con contenido dinámico) -->

  <script>
    (function() {
      // ========== CONFIGURACIÓN Y ESTADO GLOBAL ==========
      const API = "https://gambt.pythonanywhere.com/ppm";  // Para endpoints de saldo/puntos
      
      // Secciones y tabs (exactamente igual a plano1)
      const SECTION_TABS = __SECTION_TABS__;
      const sectionOrder = ["UNIRSE MESA", "CREAR MESA", "MESA JUGADOR", "MESA PRIVADA"];
      
      let currentSection = "UNIRSE MESA";
      let currentTab = SECTION_TABS[currentSection][0];
      
      // Estado para creación de reto
      let deportesSeleccionados = new Set();
      let configuracionData = {};
      let partidosSeleccionados = new Set();        // IDs de partidos seleccionados
      let partidosData = [], partidosMap = new Map();
      let respuestasPartidos = {};                  // Para el modal de predicciones
      
      // Estado para unirse a mesas
      let mesaActual = null;                        // llave o grupo_rango
      let tipoMesaActual = null;                    // 'publica', 'local', 'privada'
      let activeQuestionsMap = null;
      let publicRetoConfig = null;
      
      // Referencias DOM
      const sectionSelect = document.getElementById("sectionSelect");
      const tabsEl = document.getElementById("tabs");
      const contentEl = document.getElementById("content");
      
      // Modal
      const modalOverlay = document.getElementById("modal-overlay");
      const modalTitulo = document.getElementById("modal-titulo");
      const modalSubtitulo = document.getElementById("modal-subtitulo");
      const modalContenido = document.getElementById("modal-contenido");
      const modalEnviar = document.getElementById("modal-enviar");
      const modalCancelar = document.getElementById("modal-cancelar");
      const modalClose = document.getElementById("modal-close");
      
      // ========== INICIALIZACIÓN DE USUARIO ==========
      function cargarDatosUsuario() {
        try {
          const raw = localStorage.getItem("user_data");
          if (!raw) return;
          const u = JSON.parse(raw) || {};
          const alias = u.alias || u.nombre || "Invitado";
          const elTop = document.getElementById("user-name-top");
          if (elTop) elTop.textContent = alias.startsWith("@") ? alias : `@${alias}`;
        } catch (_) {}
      }
      
      async function cargarSaldo() {
        const uid = localStorage.getItem("user_id");
        if (!uid) return;
        try {
          const r = await fetch(`${API}/saldo/${uid}`);
          const d = await r.json();
          if (d && typeof d.saldo !== "undefined") {
            document.getElementById("saldo-usuario").textContent = `$${parseFloat(d.saldo).toFixed(2)}`;
          }
        } catch (_) {}
      }
      
      async function cargarPuntosUsuario() {
        const uid = localStorage.getItem("user_id");
        if (!uid) return;
        try {
          const r = await fetch(`${API}/puntos/${uid}`);
          const d = await r.json();
          if (d && typeof d.puntos_actuales !== "undefined") {
            document.getElementById("user-puntos").textContent = `${Number(d.puntos_actuales).toLocaleString()} pts`;
            document.getElementById("user-nivel").textContent = `${d.nivel} - ${d.descripcion_nivel || ""}`;
            document.getElementById("user-posicion").textContent = `Ranking: #${d.posicion_actual} de ${d.cantidad_jugadores} jugadores`;
          }
        } catch (_) {}
      }
      
      async function recargarDatos() {
        await Promise.all([cargarSaldo(), cargarPuntosUsuario()]);
      }
      
      // ========== NAVEGACIÓN Y RENDERIZADO ==========
      function fillSelect() {
        sectionSelect.innerHTML = "";
        sectionOrder.forEach(name => {
          const op = document.createElement("option");
          op.value = name;
          op.textContent = name;
          sectionSelect.appendChild(op);
        });
        sectionSelect.value = currentSection;
        sectionSelect.addEventListener("change", (e) => {
          currentSection = e.target.value;
          currentTab = SECTION_TABS[currentSection][0];
          // Resetear estados si cambiamos a CREAR MESA
          if (currentSection === "CREAR MESA") {
            deportesSeleccionados.clear();
            configuracionData = {};
            partidosSeleccionados.clear();
          }
          render();
        });
      }
      
      function renderTabs() {
        const tabs = SECTION_TABS[currentSection];
        tabsEl.innerHTML = tabs.map(tab => `
          <button class="tab ${tab === currentTab ? 'active' : ''}" data-tab="${tab}">
            ${tab}
          </button>
        `).join("");
        tabsEl.querySelectorAll(".tab").forEach(btn => {
          btn.addEventListener("click", () => {
            currentTab = btn.dataset.tab;
            render();
          });
        });
      }
      
      // ========== RENDERIZADO DE VISTAS (adaptado de parley_actual) ==========
      
      // ---- Mesas Activas (UNIRSE MESA / MESA JUGADOR) ----
      async function renderMesasActivas() {
        contentEl.innerHTML = `<div class="panel"><div class="panel-inner"><div class="title-row"><div class="title-lg">Mesas activas disponibles</div><div class="search"><i class="fas fa-search" style="margin-right:8px;"></i><input type="text" id="buscador-mesas" placeholder="Buscar mesas..." style="border:none;background:transparent;outline:none;width:100%;"></div></div><div id="mesas-grid" class="mesa-list">Cargando mesas...</div></div></div>`;
        
        const grid = document.getElementById("mesas-grid");
        const buscador = document.getElementById("buscador-mesas");
        
        try {
          const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_cargar_mesas_activas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: 'cargar_mesas=true'
          });
          const data = await resp.json();
          if (data.success && data.data.html) {
            grid.innerHTML = data.data.html;
            // Agregar eventos a botones Unirse
            grid.querySelectorAll('.btn-unirse').forEach(btn => {
              btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const grupoRango = btn.dataset.grupoRango;
                const nombreMesa = btn.dataset.nombreMesa;
                const card = btn.closest('.mesa-card');
                if (card && card.classList.contains('mesa-card-publica')) {
                  mostrarPartidosPublicos(grupoRango, nombreMesa);
                } else {
                  mostrarPartidosMesa(grupoRango, nombreMesa);
                }
              });
            });
          } else {
            grid.innerHTML = '<div class="empty">No hay mesas disponibles</div>';
          }
        } catch (e) {
          grid.innerHTML = '<div class="empty">Error al cargar mesas</div>';
        }
        
        if (buscador) {
          buscador.addEventListener('input', () => {
            const term = buscador.value.toLowerCase();
            grid.querySelectorAll('.mesa-card').forEach(card => {
              const title = card.querySelector('.mesa-name')?.textContent.toLowerCase() || '';
              card.style.display = title.includes(term) ? '' : 'none';
            });
          });
        }
      }
      
      // ---- Mesas Privadas ----
      async function renderMesasPrivadas() {
        contentEl.innerHTML = `<div class="panel"><div class="panel-inner"><div class="title-row"><div class="title-lg">Mesas privadas</div><div class="search"><i class="fas fa-search" style="margin-right:8px;"></i><input type="text" id="buscador-privadas" placeholder="Buscar mesas..." style="border:none;background:transparent;outline:none;width:100%;"></div></div><div id="mesas-privadas-grid" class="mesa-list">Cargando...</div></div></div>`;
        
        const grid = document.getElementById("mesas-privadas-grid");
        const userId = localStorage.getItem('user_id') || '';
        
        try {
          const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_cargar_mesas_privadas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `cargar=true&user_id=${userId}`
          });
          const data = await resp.json();
          if (data.success && data.data.html) {
            grid.innerHTML = data.data.html;
            // Adjuntar eventos para validación y copia
            grid.querySelectorAll('.btn-copy-code').forEach(btn => {
              btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const codigo = btn.dataset.codigo;
                navigator.clipboard?.writeText(codigo);
                alert('Código copiado');
              });
            });
            grid.querySelectorAll('.btn-validar-privado').forEach(btn => {
              btn.addEventListener('click', async (e) => {
                e.stopPropagation();
                const card = btn.closest('.mesa-card');
                const retoLlave = btn.dataset.llave;
                const pwdInput = card.querySelector('.privado-password-input');
                const password = pwdInput.value.trim();
                if (!password) { alert('Ingresa contraseña'); return; }
                try {
                  const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_validar_llave_privada', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: `reto_llave=${encodeURIComponent(retoLlave)}&password=${encodeURIComponent(password)}`
                  });
                  const d = await resp.json();
                  if (d.success) {
                    card.querySelector('.privado-password-container').style.display = 'none';
                    const acceptBtn = card.querySelector('.btn-aceptar-privado');
                    if (acceptBtn) acceptBtn.style.display = 'block';
                  } else {
                    alert('Contraseña incorrecta');
                  }
                } catch (err) { alert('Error de conexión'); }
              });
            });
            grid.querySelectorAll('.btn-aceptar-privado').forEach(btn => {
              btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const retoLlave = btn.dataset.llave;
                const nombreMesa = btn.dataset.nombreMesa;
                mostrarPartidosPrivados(retoLlave, nombreMesa);
              });
            });
          } else {
            grid.innerHTML = '<div class="empty">No hay mesas privadas</div>';
          }
        } catch (e) {
          grid.innerHTML = '<div class="empty">Error de conexión</div>';
        }
        
        const buscador = document.getElementById("buscador-privadas");
        if (buscador) {
          buscador.addEventListener('input', () => {
            const term = buscador.value.toLowerCase();
            grid.querySelectorAll('.mesa-card').forEach(card => {
              const title = card.querySelector('.mesa-name')?.textContent.toLowerCase() || '';
              card.style.display = title.includes(term) ? '' : 'none';
            });
          });
        }
      }
      
      // ---- Elegir Deporte (CREAR MESA) ----
      function renderElegirDeporte() {
        contentEl.innerHTML = `
          <div class="panel"><div class="panel-inner">
            <div class="title-lg">SPORTS</div>
            <div class="field">
              <div class="field-title">Nombre mesa (máximo 30 caracteres)</div>
              <input type="text" id="input-nombre-mesa" class="input" placeholder="Ej: Torneo de expertos" maxlength="30" value="${configuracionData.nombreMesa || ''}">
            </div>
            <div class="option-col" style="margin-top:10px;">
              ${['Fútbol','Baloncesto','Tenis'].map(dep => `
                <div class="option">
                  <span>${dep}</span>
                  <label class="switch"><input type="checkbox" name="deporte" value="${dep}" ${deportesSeleccionados.has(dep) ? 'checked' : ''}><span class="slider"></span></label>
                </div>
              `).join('')}
            </div>
            <div class="next-wrap"><button class="next-btn" id="btn-next-deportes" ${deportesSeleccionados.size > 0 ? '' : 'disabled'}>SIGUIENTE</button></div>
          </div></div>
        `;
        
        const nombreInput = document.getElementById('input-nombre-mesa');
        const btnNext = document.getElementById('btn-next-deportes');
        const checkboxes = document.querySelectorAll('input[name="deporte"]');
        
        const actualizarEstado = () => {
          const nombreValido = nombreInput.value.trim().length > 0 && nombreInput.value.trim().length <= 30;
          btnNext.disabled = !(deportesSeleccionados.size > 0 && nombreValido);
        };
        
        nombreInput.addEventListener('input', actualizarEstado);
        checkboxes.forEach(cb => {
          cb.addEventListener('change', (e) => {
            if (cb.checked) deportesSeleccionados.add(cb.value);
            else deportesSeleccionados.delete(cb.value);
            actualizarEstado();
          });
        });
        
        btnNext.addEventListener('click', () => {
          const nombre = nombreInput.value.trim();
          if (!nombre || nombre.length > 30) { alert('Nombre inválido'); return; }
          configuracionData.deportes = Array.from(deportesSeleccionados);
          configuracionData.nombreMesa = nombre;
          currentTab = "Configurar Encuentro";
          render();
        });
        
        actualizarEstado();
      }
      
      // ---- Configurar Encuentro (CREAR MESA) ----
      function renderConfigurarEncuentro() {
        const preguntasGuardadas = configuracionData.preguntasSeleccionadas || ['ganador'];
        contentEl.innerHTML = `
          <div class="panel"><div class="panel-inner">
            <div class="form-stack">
              <div class="field">
                <div class="field-title">Apuesta mínima (USD)</div>
                <input type="number" class="input" id="input-monto-minimo" placeholder="Ej: 17" min="1" value="${configuracionData.montoMinimo || ''}">
              </div>
              <div class="field">
                <div class="field-title">¿Tipo de reto?</div>
                <div class="radio-line">
                  <label><input type="radio" name="tipo-reto" value="Público" ${configuracionData.tipoReto !== 'Privado' ? 'checked' : ''}> Público</label>
                  <label><input type="radio" name="tipo-reto" value="Privado" ${configuracionData.tipoReto === 'Privado' ? 'checked' : ''}> Privado</label>
                </div>
              </div>
              <div class="field">
                <div class="field-title">¿Cuántos ganadores?</div>
                <div class="radio-line">
                  <label><input type="radio" name="ganadores" value="Único Ganador" ${configuracionData.ganadores !== 'Varios Ganadores' ? 'checked' : ''}> Único ganador</label>
                  <label><input type="radio" name="ganadores" value="Varios Ganadores" ${configuracionData.ganadores === 'Varios Ganadores' ? 'checked' : ''}> Varios ganadores</label>
                </div>
              </div>
              <div class="field">
                <div class="field-title">¿Preguntas por encuentro? (Selecciona 1-4)</div>
                <div class="option-col">
                  <div class="option"><label><input type="checkbox" name="preguntas" value="ganador" ${preguntasGuardadas.includes('ganador') ? 'checked' : ''}> Definir ganador</label></div>
                  <div class="option"><label><input type="checkbox" name="preguntas" value="ambos_goles" ${preguntasGuardadas.includes('ambos_goles') ? 'checked' : ''}> ¿Gol de ambos equipos?</label></div>
                  <div class="option"><label><input type="checkbox" name="preguntas" value="penales" ${preguntasGuardadas.includes('penales') ? 'checked' : ''}> ¿Penales?</label></div>
                  <div class="option"><label><input type="checkbox" name="preguntas" value="marcador" ${preguntasGuardadas.includes('marcador') ? 'checked' : ''}> Predice el marcador</label></div>
                </div>
                <div class="mini" style="margin-top:5px;">Selecciona entre 1 y 4 preguntas.</div>
              </div>
              <div class="field">
                <div class="field-title">¿Tipo de Mesa?</div>
                <div class="radio-line">
                  <label><input type="radio" name="tipo-mesa" value="Selección" ${configuracionData.tipoMesa !== 'Torneo corto' && configuracionData.tipoMesa !== 'Torneo Largo' ? 'checked' : ''}> Selección</label>
                  <label><input type="radio" name="tipo-mesa" value="Torneo corto" ${configuracionData.tipoMesa === 'Torneo corto' ? 'checked' : ''}> Torneo corto</label>
                  <label><input type="radio" name="tipo-mesa" value="Torneo Largo" ${configuracionData.tipoMesa === 'Torneo Largo' ? 'checked' : ''}> Torneo largo</label>
                </div>
              </div>
            </div>
            <div class="next-wrap"><button class="next-btn" id="btn-next-config" disabled>SIGUIENTE</button></div>
          </div></div>
        `;
        
        const montoInput = document.getElementById('input-monto-minimo');
        const btnNext = document.getElementById('btn-next-config');
        const checkPreguntas = document.querySelectorAll('input[name="preguntas"]');
        
        const validar = () => {
          const montoValido = parseFloat(montoInput.value) > 0;
          const seleccionadas = Array.from(checkPreguntas).filter(cb => cb.checked).length;
          btnNext.disabled = !(montoValido && seleccionadas >= 1 && seleccionadas <= 4);
        };
        
        montoInput.addEventListener('input', validar);
        checkPreguntas.forEach(cb => cb.addEventListener('change', validar));
        validar();
        
        btnNext.addEventListener('click', () => {
          const monto = montoInput.value;
          const tipoReto = document.querySelector('input[name="tipo-reto"]:checked').value;
          const ganadores = document.querySelector('input[name="ganadores"]:checked').value;
          const preguntas = Array.from(document.querySelectorAll('input[name="preguntas"]:checked')).map(cb => cb.value);
          const tipoMesa = document.querySelector('input[name="tipo-mesa"]:checked').value;
          
          configuracionData.montoMinimo = monto;
          configuracionData.tipoReto = tipoReto;
          configuracionData.ganadores = ganadores;
          configuracionData.preguntasSeleccionadas = preguntas;
          configuracionData.tipoMesa = tipoMesa;
          
          currentTab = "Elegir Partidos";
          render();
        });
      }
      
      // ---- Elegir Partidos (CREAR MESA) ----
      async function renderElegirPartidos() {
        contentEl.innerHTML = `<div class="panel"><div class="panel-inner"><div class="title-lg">Partidos disponibles</div><div id="partidos-lista" class="pick-cards">Cargando partidos...</div><div class="next-wrap"><button class="next-btn" id="btn-enviar-partidos" disabled>ENVIAR</button></div></div></div>`;
        
        // Cargar partidos desde el endpoint
        try {
          const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_retos_grupales_ajax');
          const html = await resp.text();
          const tempDiv = document.createElement('div');
          tempDiv.innerHTML = html;
          const filas = tempDiv.querySelectorAll('tbody tr[data-mid]');
          partidosData = [];
          partidosMap.clear();
          filas.forEach(fila => {
            const partidoId = fila.getAttribute('data-mid');
            const celdas = fila.querySelectorAll('td');
            if (celdas.length) {
              const equipoDiv = celdas[0].querySelector('.g-row');
              const textos = equipoDiv?.querySelectorAll('span');
              const escudos = equipoDiv?.querySelectorAll('img');
              const partido = {
                id: partidoId,
                local: { nombre: textos[0]?.textContent || 'Local', escudo: escudos[0]?.src || '' },
                visita: { nombre: textos[2]?.textContent || 'Visitante', escudo: escudos[1]?.src || '' },
                horario: celdas[1]?.textContent || '',
                estado: 'SCHEDULED'
              };
              partidosData.push(partido);
              partidosMap.set(partidoId, partido);
            }
          });
        } catch (e) {
          // Datos de ejemplo
          partidosData = [
            { id: 'p1', local:{nombre:'Casa Pia'}, visita:{nombre:'Gil Vicente'}, horario:'26 abr 2026, 00:00' },
            { id: 'p2', local:{nombre:'Tondela'}, visita:{nombre:'CD Nacional'}, horario:'26 abr 2026, 00:00' },
          ];
          partidosData.forEach(p => partidosMap.set(p.id, p));
        }
        
        const container = document.getElementById('partidos-lista');
        container.innerHTML = partidosData.map(p => `
          <div class="pick-card ${partidosSeleccionados.has(p.id) ? 'selected' : ''}" data-id="${p.id}">
            <div class="pick-check"></div>
            <div>
              <div class="pick-title">${p.local.nombre} vs ${p.visita.nombre}</div>
              <div class="pick-meta">Horario: ${p.horario}<br>Estado: Disponible</div>
              <div class="pick-tag">Agregar al reto</div>
            </div>
          </div>
        `).join('');
        
        const btnEnviar = document.getElementById('btn-enviar-partidos');
        const actualizarBoton = () => {
          btnEnviar.disabled = partidosSeleccionados.size === 0;
          btnEnviar.textContent = partidosSeleccionados.size ? `ENVIAR (${partidosSeleccionados.size})` : 'ENVIAR';
        };
        actualizarBoton();
        
        container.querySelectorAll('.pick-card').forEach(card => {
          card.addEventListener('click', () => {
            const id = card.dataset.id;
            if (partidosSeleccionados.has(id)) {
              partidosSeleccionados.delete(id);
              card.classList.remove('selected');
            } else {
              partidosSeleccionados.add(id);
              card.classList.add('selected');
            }
            actualizarBoton();
          });
        });
        
        btnEnviar.addEventListener('click', mostrarModalCrearReto);
      }
      
      // ---- Históricos ----
      function renderHistEncuentros() {
        contentEl.innerHTML = `<div class="panel"><div class="panel-inner"><div class="title-lg">Histórico de encuentros</div><div class="empty">No hay encuentros históricos disponibles</div></div></div>`;
      }
      
      async function renderHistApuestas() {
        contentEl.innerHTML = `<div class="panel"><div class="panel-inner"><div class="title-lg">Histórico de apuestas</div><div class="history-table"><div class="history-head"><div>Partido</div><div>Predicción</div><div>Resultado</div><div>Estado</div><div>Fecha</div></div><div id="historial-body"></div></div></div></div>`;
        const userId = localStorage.getItem('user_id');
        if (!userId) return;
        try {
          const resp = await fetch(`/wp-admin/admin-ajax.php?action=gambt_obtener_historial&user_id=${userId}`);
          const data = await resp.json();
          const apuestas = data.data?.apuestas || [];
          const body = document.getElementById('historial-body');
          if (apuestas.length === 0) {
            body.innerHTML = `<div class="history-row"><div></div><div></div><div>No hay apuestas</div><div></div><div></div></div>`;
            return;
          }
          body.innerHTML = apuestas.map(a => `
            <div class="history-row">
              <div>${a.partido || 'N/A'}</div>
              <div>${a.ganador || ''} (${a.marcador_local||0}-${a.marcador_visita||0})</div>
              <div>${a.ganador_real || ''} (${a.marcador_local_real||0}-${a.marcador_visita_real||0})</div>
              <div>${a.resultado_ia || 'Pendiente'}</div>
              <div>${new Date(a.fecha_apuesta).toLocaleDateString()}</div>
            </div>
          `).join('');
        } catch (e) {
          document.getElementById('historial-body').innerHTML = `<div class="history-row"><div></div><div></div><div>Error al cargar</div><div></div><div></div></div>`;
        }
      }
      
      // ========== MODALES DE PREDICCIÓN ==========
      function cerrarModal() {
        modalOverlay.style.display = 'none';
        respuestasPartidos = {};
        mesaActual = null;
        tipoMesaActual = null;
      }
      
      async function mostrarPartidosPublicos(llave, nombreMesa) {
        tipoMesaActual = 'publica';
        mesaActual = llave;
        modalTitulo.textContent = `Partidos - ${nombreMesa}`;
        modalSubtitulo.textContent = 'Selecciona tus predicciones';
        modalContenido.innerHTML = 'Cargando...';
        modalOverlay.style.display = 'flex';
        
        try {
          const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_cargar_partidos_publicos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `llave=${encodeURIComponent(llave)}`
          });
          const data = await resp.json();
          if (!data.success) throw new Error(data.data);
          
          const partidos = data.data.partidos;
          const config = data.data.config;
          publicRetoConfig = config;
          
          // Determinar preguntas activas
          const first = partidos[0];
          const activeQuestions = [];
          if (first.ganador !== 'NO_APLICA') activeQuestions.push('ganador');
          if (first.ambos_anotan != 99) activeQuestions.push('ambos_goles');
          if (first.penales != 99) activeQuestions.push('penales');
          if (first.marcador_local != 99 || first.marcador_visita != 99) activeQuestions.push('marcador');
          activeQuestionsMap = {};
          
          let html = '';
          partidos.forEach(p => {
            const pid = p.partido_id;
            activeQuestionsMap[pid] = activeQuestions;
            respuestasPartidos[pid] = { id_partido: pid, estado_partido: 'SCHEDULED' };
            
            let pregHTML = '';
            if (activeQuestions.includes('ganador')) {
              pregHTML += `<div class="prediction-options"><div class="prediction-option" data-pid="${pid}" data-preg="ganador" data-val="Empate">Empate</div><div class="prediction-option" data-pid="${pid}" data-preg="ganador" data-val="${p.local_nombre}">${p.local_nombre}</div><div class="prediction-option" data-pid="${pid}" data-preg="ganador" data-val="${p.visita_nombre}">${p.visita_nombre}</div></div>`;
            }
            if (activeQuestions.includes('ambos_goles')) {
              pregHTML += `<div class="prediction-options"><div class="prediction-option" data-pid="${pid}" data-preg="ambos_goles" data-val="Sí">Sí</div><div class="prediction-option" data-pid="${pid}" data-preg="ambos_goles" data-val="No">No</div><div class="prediction-option" data-pid="${pid}" data-preg="ambos_goles" data-val="Ninguno anota">Ninguno anota</div></div>`;
            }
            if (activeQuestions.includes('penales')) {
              pregHTML += `<div class="prediction-options"><div class="prediction-option" data-pid="${pid}" data-preg="penales" data-val="Sí">Sí</div><div class="prediction-option" data-pid="${pid}" data-preg="penales" data-val="No">No</div></div>`;
            }
            if (activeQuestions.includes('marcador')) {
              pregHTML += `<div style="display:flex;gap:10px;justify-content:center;margin-top:10px;"><input type="number" min="0" max="9" value="0" data-pid="${pid}" data-tipo="local" class="marcador-input" style="width:60px;"> <span>-</span> <input type="number" min="0" max="9" value="0" data-pid="${pid}" data-tipo="visitante" class="marcador-input" style="width:60px;"></div>`;
            }
            
            html += `<div class="prediction-item"><div class="prediction-header"><span class="prediction-team">${p.local_nombre}</span> VS <span class="prediction-team">${p.visita_nombre}</span></div>${pregHTML}</div>`;
          });
          modalContenido.innerHTML = html;
          
          // Eventos
          modalContenido.querySelectorAll('.prediction-option').forEach(opt => {
            opt.addEventListener('click', () => {
              const pid = opt.dataset.pid;
              const preg = opt.dataset.preg;
              const val = opt.dataset.val;
              if (!respuestasPartidos[pid]) respuestasPartidos[pid] = {};
              respuestasPartidos[pid][preg] = val;
              opt.parentNode.querySelectorAll('.prediction-option').forEach(o => o.classList.remove('selected'));
              opt.classList.add('selected');
            });
          });
          
        } catch (e) {
          alert('Error al cargar partidos');
          cerrarModal();
        }
      }
      
      async function mostrarPartidosMesa(grupoRango, nombreMesa) {
        tipoMesaActual = 'local';
        mesaActual = grupoRango;
        modalTitulo.textContent = `Partidos - ${nombreMesa}`;
        modalSubtitulo.textContent = 'Selecciona tus predicciones';
        modalContenido.innerHTML = 'Cargando...';
        modalOverlay.style.display = 'flex';
        
        try {
          const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_cargar_partidos_mesa', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `grupo_rango=${encodeURIComponent(grupoRango)}`
          });
          const data = await resp.json();
          if (!data.success) throw new Error(data.data);
          modalContenido.innerHTML = data.data.html;
          
          // Inicializar respuestas
          modalContenido.querySelectorAll('.partido-item-mejorado').forEach(item => {
            const pid = item.dataset.partidoId;
            respuestasPartidos[pid] = { id_partido: pid, estado_partido: 'SCHEDULED' };
          });
          
          // Eventos (similares a parley_actual)
          modalContenido.querySelectorAll('.opcion-mejorada').forEach(opt => {
            opt.addEventListener('click', () => {
              const pid = opt.dataset.partidoId;
              const preg = opt.dataset.pregunta;
              const val = opt.dataset.valor;
              if (!respuestasPartidos[pid]) respuestasPartidos[pid] = {};
              respuestasPartidos[pid][preg] = val;
              const grupo = opt.closest('.opciones-grid-mejorado');
              if (grupo) grupo.querySelectorAll('.opcion-mejorada').forEach(o => o.classList.remove('selected'));
              opt.classList.add('selected');
            });
          });
          
        } catch (e) {
          alert('Error al cargar partidos');
          cerrarModal();
        }
      }
      
      async function mostrarPartidosPrivados(retoLlave, nombreMesa) {
        tipoMesaActual = 'privada';
        mesaActual = retoLlave;
        modalTitulo.textContent = `Reto Privado - ${nombreMesa}`;
        modalSubtitulo.textContent = 'Selecciona tus predicciones';
        modalContenido.innerHTML = 'Cargando...';
        modalOverlay.style.display = 'flex';
        
        try {
          const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_cargar_preguntas_privadas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `reto_llave=${encodeURIComponent(retoLlave)}`
          });
          const data = await resp.json();
          if (!data.success) throw new Error(data.data);
          
          const partidos = data.data.partidos;
          const config = data.data.config;
          const activeQuestions = config.activeQuestions || [];
          
          let html = '';
          partidos.forEach(p => {
            const pid = p.partido_id;
            respuestasPartidos[pid] = { id_partido: pid };
            let pregHTML = '';
            if (activeQuestions.includes('ganador')) {
              pregHTML += `<div class="prediction-options"><div class="prediction-option" data-pid="${pid}" data-preg="ganador" data-val="Empate">Empate</div><div class="prediction-option" data-pid="${pid}" data-preg="ganador" data-val="${p.local_nombre}">${p.local_nombre}</div><div class="prediction-option" data-pid="${pid}" data-preg="ganador" data-val="${p.visita_nombre}">${p.visita_nombre}</div></div>`;
            }
            if (activeQuestions.includes('ambos_goles')) {
              pregHTML += `<div class="prediction-options"><div class="prediction-option" data-pid="${pid}" data-preg="ambos_goles" data-val="Sí">Sí</div><div class="prediction-option" data-pid="${pid}" data-preg="ambos_goles" data-val="No">No</div><div class="prediction-option" data-pid="${pid}" data-preg="ambos_goles" data-val="Ninguno anota">Ninguno anota</div></div>`;
            }
            if (activeQuestions.includes('penales')) {
              pregHTML += `<div class="prediction-options"><div class="prediction-option" data-pid="${pid}" data-preg="penales" data-val="Sí">Sí</div><div class="prediction-option" data-pid="${pid}" data-preg="penales" data-val="No">No</div></div>`;
            }
            if (activeQuestions.includes('marcador')) {
              pregHTML += `<div style="display:flex;gap:10px;justify-content:center;"><input type="number" value="0" data-pid="${pid}" data-tipo="local"> - <input type="number" value="0" data-pid="${pid}" data-tipo="visitante"></div>`;
            }
            html += `<div class="prediction-item"><div class="prediction-header">${p.local_nombre} vs ${p.visita_nombre}</div>${pregHTML}</div>`;
          });
          modalContenido.innerHTML = html;
          
          modalContenido.querySelectorAll('.prediction-option').forEach(opt => {
            opt.addEventListener('click', () => {
              const pid = opt.dataset.pid;
              const preg = opt.dataset.preg;
              const val = opt.dataset.val;
              if (!respuestasPartidos[pid]) respuestasPartidos[pid] = {};
              respuestasPartidos[pid][preg] = val;
              opt.parentNode.querySelectorAll('.prediction-option').forEach(o => o.classList.remove('selected'));
              opt.classList.add('selected');
            });
          });
          
        } catch (e) {
          alert('Error al cargar reto privado');
          cerrarModal();
        }
      }
      
      // Enviar apuesta (unirse)
      async function enviarApuesta() {
        const userId = localStorage.getItem('user_id');
        if (!userId) { alert('Usuario no identificado'); return; }
        
        // Validar que todas las preguntas tengan respuesta
        const partidos = modalContenido.querySelectorAll('[data-pid], .partido-item-mejorado');
        for (let p of partidos) {
          const pid = p.dataset.pid || p.dataset.partidoId;
          const resp = respuestasPartidos[pid];
          if (!resp) { alert('Faltan respuestas'); return; }
          // Validación básica: al menos ganador debe estar presente si existe
          if (activeQuestionsMap && activeQuestionsMap[pid]?.includes('ganador') && !resp.ganador) {
            alert('Selecciona un ganador para todos los partidos'); return;
          }
        }
        
        const apuestaData = {
          user_id: userId,
          grupo_rango: mesaActual,
          fecha_apuesta: new Date().toISOString().slice(0,19).replace('T',' '),
          respuestas: respuestasPartidos
        };
        
        if (tipoMesaActual === 'publica') apuestaData.modo_forzado = 'Acepta_reto';
        else if (tipoMesaActual === 'local') apuestaData.modo_forzado = 'Acepta_reto_local';
        else if (tipoMesaActual === 'privada') apuestaData.modo_forzado = 'Acepta reto privado';
        
        if (publicRetoConfig) {
          apuestaData.apuesta_minima_usd = publicRetoConfig.apuesta_minima_usd;
          apuestaData.nombre_mesa = publicRetoConfig.nombre_mesa;
        }
        
        try {
          const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_guardar_apuesta_ppm', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `apuesta_data=${encodeURIComponent(JSON.stringify(apuestaData))}`
          });
          const data = await resp.json();
          if (data.success) {
            alert('Apuesta registrada');
            cerrarModal();
            recargarDatos();
            if (currentTab === 'Mesas activas') renderMesasActivas();
          } else {
            alert('Error: ' + (data.data || ''));
          }
        } catch (e) {
          alert('Error de conexión');
        }
      }
      
      // Modal para CREAR RETO
      function mostrarModalCrearReto() {
        if (partidosSeleccionados.size === 0) { alert('Selecciona al menos un partido'); return; }
        if (!configuracionData.preguntasSeleccionadas?.length) { alert('Configura las preguntas primero'); return; }
        if (!configuracionData.nombreMesa) { alert('Ingresa nombre de mesa'); return; }
        
        respuestasPartidos = {};
        modalTitulo.textContent = 'Crear Reto';
        modalSubtitulo.textContent = 'Selecciona tus predicciones para cada partido';
        modalOverlay.style.display = 'flex';
        
        const partidosArray = Array.from(partidosSeleccionados);
        let html = '';
        partidosArray.forEach(id => {
          const p = partidosMap.get(id);
          if (!p) return;
          respuestasPartidos[id] = { id_partido: id, estado_partido: 'SCHEDULED' };
          
          let pregHTML = '';
          const preguntas = configuracionData.preguntasSeleccionadas;
          if (preguntas.includes('ganador')) {
            pregHTML += `<div class="prediction-options"><div class="prediction-option" data-pid="${id}" data-preg="ganador" data-val="Local">${p.local.nombre}</div><div class="prediction-option" data-pid="${id}" data-preg="ganador" data-val="Empate">Empate</div><div class="prediction-option" data-pid="${id}" data-preg="ganador" data-val="Visitante">${p.visita.nombre}</div></div>`;
          }
          if (preguntas.includes('ambos_goles')) {
            pregHTML += `<div class="prediction-options"><div class="prediction-option" data-pid="${id}" data-preg="ambos_goles" data-val="Sí">Sí</div><div class="prediction-option" data-pid="${id}" data-preg="ambos_goles" data-val="No">No</div><div class="prediction-option" data-pid="${id}" data-preg="ambos_goles" data-val="Ninguno anota">Ninguno anota</div></div>`;
          }
          if (preguntas.includes('penales')) {
            pregHTML += `<div class="prediction-options"><div class="prediction-option" data-pid="${id}" data-preg="penales" data-val="Sí">Sí</div><div class="prediction-option" data-pid="${id}" data-preg="penales" data-val="No">No</div></div>`;
          }
          if (preguntas.includes('marcador')) {
            pregHTML += `<div style="display:flex;gap:10px;"><input type="number" value="0" data-pid="${id}" data-tipo="local"> - <input type="number" value="0" data-pid="${id}" data-tipo="visitante"></div>`;
          }
          
          html += `<div class="prediction-item"><div class="prediction-header">${p.local.nombre} vs ${p.visita.nombre}</div>${pregHTML}</div>`;
        });
        modalContenido.innerHTML = html;
        
        modalContenido.querySelectorAll('.prediction-option').forEach(opt => {
          opt.addEventListener('click', () => {
            const pid = opt.dataset.pid;
            const preg = opt.dataset.preg;
            const val = opt.dataset.val;
            if (!respuestasPartidos[pid]) respuestasPartidos[pid] = {};
            respuestasPartidos[pid][preg] = val;
            opt.parentNode.querySelectorAll('.prediction-option').forEach(o => o.classList.remove('selected'));
            opt.classList.add('selected');
          });
        });
        
        // Cambiar comportamiento del botón enviar
        modalEnviar.onclick = async () => {
          const userId = localStorage.getItem('user_id');
          if (!userId) { alert('Usuario no identificado'); return; }
          
          // Validar
          for (let id of partidosArray) {
            const resp = respuestasPartidos[id];
            if (!resp) { alert('Completa todas las predicciones'); return; }
            if (configuracionData.preguntasSeleccionadas.includes('ganador') && !resp.ganador) { alert('Selecciona ganador'); return; }
          }
          
          const grupoRango = 'user_created_challenge_' + Date.now();
          const llave = [userId, ...partidosArray].join('-');
          
          const apuestaData = {
            user_id: userId,
            grupo_rango: grupoRango,
            fecha_apuesta: new Date().toISOString().slice(0,19).replace('T',' '),
            respuestas: respuestasPartidos,
            configuracion: configuracionData,
            apuesta_minima_usd: configuracionData.montoMinimo || 0,
            preguntas_por_encuentro: configuracionData.preguntasSeleccionadas.length,
            tipo_reto: configuracionData.tipoReto,
            tipo_mesa: configuracionData.tipoMesa,
            pregunta_cuantos_ganadores: configuracionData.ganadores,
            llave: llave,
            nombre_mesa: configuracionData.nombreMesa,
            modo_forzado: 'Crear_reto'
          };
          
          try {
            const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_guardar_apuesta_ppm', {
              method: 'POST',
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
              body: `apuesta_data=${encodeURIComponent(JSON.stringify(apuestaData))}`
            });
            const data = await resp.json();
            if (data.success) {
              alert('Reto creado correctamente');
              cerrarModal();
              partidosSeleccionados.clear();
              recargarDatos();
            } else {
              alert('Error: ' + (data.data || ''));
            }
          } catch (e) {
            alert('Error de conexión');
          }
        };
      }
      
      // ========== RENDER PRINCIPAL ==========
      function renderContent() {
        if (currentTab === "Mesas activas") {
          renderMesasActivas(); return;
        }
        if (currentTab === "Mesas privadas") {
          renderMesasPrivadas(); return;
        }
        if (currentTab === "Histórico de encuentros") {
          renderHistEncuentros(); return;
        }
        if (currentTab === "Histórico de apuestas") {
          renderHistApuestas(); return;
        }
        if (currentTab === "Elegir Deporte") {
          renderElegirDeporte(); return;
        }
        if (currentTab === "Configurar Encuentro") {
          renderConfigurarEncuentro(); return;
        }
        if (currentTab === "Elegir Partidos") {
          renderElegirPartidos(); return;
        }
        // Fallback
        contentEl.innerHTML = `<div class="panel"><div class="panel-inner"><div class="empty">Vista no implementada</div></div></div>`;
      }
      
      function render() {
        renderTabs();
        renderContent();
        sectionSelect.value = currentSection;
      }
      
      // ========== EVENTOS GLOBALES ==========
      function setupEventListeners() {
        document.getElementById('btn-entrar-classic').addEventListener('click', () => {
          const lang = localStorage.getItem('gambt_lang') || 'es';
          window.location.href = lang === 'en' ? 'https://www.gambt.online/elementor-1641-en/' : 'https://www.gambt.online/elementor-1641/';
        });
        
        document.getElementById('logo-link').addEventListener('click', (e) => {
          e.preventDefault();
          const lang = localStorage.getItem('gambt_lang') || 'es';
          window.location.href = lang === 'en' ? 'https://www.gambt.online/Inicio GAMBT-en/' : 'https://www.gambt.online/Inicio GAMBT/';
        });
        
        document.getElementById('user-menu').addEventListener('click', () => {
          window.location.href = 'https://www.gambt.online/entorno-usuario/';
        });
        
        // Modal
        modalClose.addEventListener('click', cerrarModal);
        modalCancelar.addEventListener('click', cerrarModal);
        modalOverlay.addEventListener('click', (e) => { if (e.target === modalOverlay) cerrarModal(); });
        modalEnviar.addEventListener('click', enviarApuesta);
      }
      
      // ========== INICIALIZACIÓN ==========
      async function init() {
        cargarDatosUsuario();
        await recargarDatos();
        fillSelect();
        render();
        setupEventListeners();
        setInterval(recargarDatos, 30000);
      }
      
      init();
    })();
  </script>
</body>
</html>
"""

html = html.replace("__SECTION_TABS__", json.dumps(SECTION_TABS, ensure_ascii=False))
components.html(html, height=930, scrolling=True)
