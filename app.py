<div id="gambt-mobile-wordpress">
  <style>
    #gambt-mobile-wordpress{
      --gm-bg:#f3f3f3;
      --gm-panel:#ffffff;
      --gm-panel2:#f7f7f7;
      --gm-line:#202020;
      --gm-line2:#6d6d6d;
      --gm-text:#111111;
      --gm-muted:#555555;
      --gm-soft:#e7e7e7;
      --gm-accent:#111111;
      --gm-danger:#8b0000;
      width:100%;
      max-width:100%;
      margin:0;
      padding:0;
      background:var(--gm-bg);
      color:var(--gm-text);
      font-family:Arial,sans-serif;
      box-sizing:border-box;
    }

    #gambt-mobile-wordpress *, 
    #gambt-mobile-wordpress *::before, 
    #gambt-mobile-wordpress *::after{
      box-sizing:border-box;
      font-family:inherit;
    }

    #gambt-mobile-wordpress .gm-screen{
      width:100%;
      min-height:100vh;
      background:var(--gm-bg);
      display:flex;
      flex-direction:column;
      gap:10px;
    }

    #gambt-mobile-wordpress .gm-topbar{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:8px;
      padding:10px;
      background:var(--gm-panel);
      border:1px solid var(--gm-line);
    }

    #gambt-mobile-wordpress .gm-topbar-right{
      display:flex;
      align-items:center;
      gap:8px;
      min-width:0;
      flex:1;
      justify-content:flex-end;
    }

    #gambt-mobile-wordpress .gm-logo,
    #gambt-mobile-wordpress .gm-lang,
    #gambt-mobile-wordpress .gm-user-chip{
      min-height:42px;
      border:1px solid var(--gm-line);
      background:var(--gm-panel2);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:900;
      color:var(--gm-text);
      text-align:center;
    }

    #gambt-mobile-wordpress .gm-logo{
      flex:1;
      font-size:24px;
      min-width:120px;
    }

    #gambt-mobile-wordpress .gm-lang{
      width:110px;
      font-size:14px;
    }

    #gambt-mobile-wordpress .gm-wrap{
      padding:10px;
      display:flex;
      flex-direction:column;
      gap:10px;
    }

    #gambt-mobile-wordpress .gm-cards{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:10px;
    }

    #gambt-mobile-wordpress .gm-card{
      background:var(--gm-panel);
      border:1px solid var(--gm-line);
      padding:12px;
      min-height:92px;
    }

    #gambt-mobile-wordpress .gm-card.gm-full{
      grid-column:1 / -1;
      min-height:84px;
    }

    #gambt-mobile-wordpress .gm-card-title{
      font-size:12px;
      font-weight:700;
      text-transform:uppercase;
      margin-bottom:8px;
    }

    #gambt-mobile-wordpress .gm-card-value{
      font-size:26px;
      font-weight:900;
      line-height:1;
      margin-bottom:8px;
    }

    #gambt-mobile-wordpress .gm-mini{
      font-size:12px;
      line-height:1.25;
      color:var(--gm-muted);
    }

    #gambt-mobile-wordpress .gm-btn,
    #gambt-mobile-wordpress button,
    #gambt-mobile-wordpress .btn-unirse,
    #gambt-mobile-wordpress .btn-copy-code,
    #gambt-mobile-wordpress .btn-validar-privado,
    #gambt-mobile-wordpress .btn-aceptar-privado{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      min-height:36px;
      padding:0 14px;
      border:1px solid var(--gm-line);
      background:var(--gm-soft);
      color:var(--gm-text);
      font-size:14px;
      font-weight:900;
      cursor:pointer;
      text-decoration:none;
      border-radius:0;
      box-shadow:none;
    }

    #gambt-mobile-wordpress .gm-btn:disabled,
    #gambt-mobile-wordpress button:disabled{
      opacity:.45;
      cursor:not-allowed;
    }

    #gambt-mobile-wordpress .gm-select-wrap{
      background:var(--gm-panel);
      border:1px solid var(--gm-line);
      padding:10px;
    }

    #gambt-mobile-wordpress .gm-label{
      font-size:12px;
      font-weight:700;
      text-transform:uppercase;
      margin-bottom:6px;
    }

    #gambt-mobile-wordpress select,
    #gambt-mobile-wordpress input[type="text"],
    #gambt-mobile-wordpress input[type="number"],
    #gambt-mobile-wordpress input[type="password"]{
      width:100%;
      min-height:40px;
      border:1px solid var(--gm-line);
      background:#fff;
      color:var(--gm-text);
      padding:8px 10px;
      font-size:14px;
      outline:none;
      border-radius:0;
    }

    #gambt-mobile-wordpress .gm-tabs{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:8px;
    }

    #gambt-mobile-wordpress .gm-tab{
      min-height:40px;
      border:1px solid var(--gm-line);
      background:var(--gm-panel);
      color:var(--gm-text);
      font-weight:700;
      font-size:13px;
      padding:8px 10px;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      cursor:pointer;
    }

    #gambt-mobile-wordpress .gm-tab.active{
      background:var(--gm-soft);
      border-width:2px;
    }

    #gambt-mobile-wordpress .gm-panel{
      background:var(--gm-panel);
      border:1px solid var(--gm-line);
      padding:10px;
    }

    #gambt-mobile-wordpress .gm-panel-inner{
      border:1px solid var(--gm-line2);
      padding:10px;
      background:#fff;
    }

    #gambt-mobile-wordpress .gm-title-row{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:8px;
      margin-bottom:12px;
    }

    #gambt-mobile-wordpress .gm-title-lg{
      font-size:18px;
      font-weight:900;
      text-transform:uppercase;
      line-height:1.15;
    }

    #gambt-mobile-wordpress .gm-search{
      width:160px;
      min-height:38px;
    }

    #gambt-mobile-wordpress .gm-empty,
    #gambt-mobile-wordpress .historial-vacio{
      min-height:120px;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      color:var(--gm-muted);
      font-size:14px;
      font-weight:700;
      padding:10px;
    }

    #gambt-mobile-wordpress .gm-field{
      border:1px solid var(--gm-line);
      padding:12px;
      background:#fff;
      margin-bottom:10px;
    }

    #gambt-mobile-wordpress .gm-field-title{
      font-size:13px;
      font-weight:900;
      margin-bottom:10px;
    }

    #gambt-mobile-wordpress .gm-option-col{
      display:grid;
      grid-template-columns:1fr;
      gap:8px;
    }

    #gambt-mobile-wordpress .gm-sport,
    #gambt-mobile-wordpress .gm-question,
    #gambt-mobile-wordpress .gm-radio{
      min-height:44px;
      border:1px solid var(--gm-line2);
      background:#fff;
      padding:10px 12px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      cursor:pointer;
      user-select:none;
    }

    #gambt-mobile-wordpress .gm-sport.active,
    #gambt-mobile-wordpress .gm-question.active,
    #gambt-mobile-wordpress .gm-radio.active{
      background:var(--gm-soft);
      border-width:2px;
      border-color:var(--gm-line);
    }

    #gambt-mobile-wordpress .gm-radio-list{
      display:grid;
      grid-template-columns:1fr;
      gap:8px;
    }

    #gambt-mobile-wordpress .gm-next-wrap{
      margin-top:12px;
      display:flex;
      justify-content:center;
      gap:8px;
      flex-wrap:wrap;
    }

    #gambt-mobile-wordpress .gm-pick-cards{
      display:grid;
      grid-template-columns:1fr;
      gap:10px;
    }

    #gambt-mobile-wordpress .gm-pick-card{
      border:1px solid var(--gm-line);
      background:var(--gm-panel2);
      padding:12px;
      display:grid;
      grid-template-columns:36px 1fr;
      gap:10px;
      align-items:flex-start;
      cursor:pointer;
    }

    #gambt-mobile-wordpress .gm-pick-card.selected{
      border-width:2px;
      background:#ececec;
    }

    #gambt-mobile-wordpress .gm-pick-check{
      width:24px;
      height:24px;
      border:2px solid var(--gm-line);
      background:#fff;
      margin-top:2px;
      position:relative;
    }

    #gambt-mobile-wordpress .gm-pick-card.selected .gm-pick-check::after{
      content:"";
      position:absolute;
      inset:4px;
      background:#888;
    }

    #gambt-mobile-wordpress .gm-pick-title{
      font-size:15px;
      font-weight:900;
      margin-bottom:8px;
      line-height:1.2;
    }

    #gambt-mobile-wordpress .gm-pick-meta{
      font-size:13px;
      line-height:1.35;
      color:#222;
    }

    #gambt-mobile-wordpress .gm-pick-tag{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      min-height:28px;
      padding:0 10px;
      border:1px solid var(--gm-line2);
      background:#fff;
      font-size:12px;
      font-weight:700;
      margin-top:8px;
    }

    #gambt-mobile-wordpress .gm-history-table{
      border:1px solid var(--gm-line2);
      overflow:hidden;
      background:#fff;
    }

    #gambt-mobile-wordpress .gm-history-head,
    #gambt-mobile-wordpress .gm-history-row{
      display:grid;
      grid-template-columns:1.15fr 1.1fr 1.15fr .9fr .9fr;
    }

    #gambt-mobile-wordpress .gm-history-head div{
      background:var(--gm-soft);
      padding:10px;
      border-right:1px solid var(--gm-line2);
      font-weight:900;
      font-size:12px;
    }

    #gambt-mobile-wordpress .gm-history-head div:last-child{
      border-right:none;
    }

    #gambt-mobile-wordpress .gm-history-row div{
      padding:10px;
      border-top:1px solid var(--gm-line2);
      border-right:1px solid var(--gm-line2);
      font-size:12px;
      line-height:1.3;
      display:flex;
      align-items:center;
      background:#fff;
      word-break:break-word;
    }

    #gambt-mobile-wordpress .gm-history-row div:last-child{
      border-right:none;
    }

    #gambt-mobile-wordpress .gm-chip-ok{
      font-weight:900;
    }

    #gambt-mobile-wordpress .gm-chip-bad{
      font-weight:900;
    }

    #gambt-mobile-wordpress .mesa-list,
    #gambt-mobile-wordpress .mesas-grid{
      display:grid;
      grid-template-columns:1fr;
      gap:10px;
    }

    #gambt-mobile-wordpress .mesa-card{
      border:1px solid var(--gm-line);
      background:var(--gm-panel2);
      padding:12px;
    }

    #gambt-mobile-wordpress .mesa-titulo,
    #gambt-mobile-wordpress .mesa-name{
      font-size:14px;
      font-weight:900;
      margin-bottom:8px;
      line-height:1.2;
    }

    #gambt-mobile-wordpress .mesa-info,
    #gambt-mobile-wordpress .mesa-meta{
      font-size:13px;
      line-height:1.35;
      color:#222;
      margin-bottom:3px;
    }

    #gambt-mobile-wordpress .mesa-card .btn-unirse,
    #gambt-mobile-wordpress .mesa-card .btn-copy-code,
    #gambt-mobile-wordpress .mesa-card .btn-validar-privado,
    #gambt-mobile-wordpress .mesa-card .btn-aceptar-privado{
      margin-top:10px;
      width:100%;
    }

    #gambt-mobile-wordpress .privado-password-container{
      display:grid;
      grid-template-columns:1fr;
      gap:8px;
      margin-top:10px;
    }

    #gambt-mobile-wordpress .gm-modal-overlay{
      position:fixed;
      inset:0;
      background:rgba(0,0,0,.55);
      display:none;
      align-items:flex-start;
      justify-content:center;
      padding:14px;
      z-index:99999;
      overflow:auto;
    }

    #gambt-mobile-wordpress .gm-modal{
      width:min(100%, 460px);
      background:#fff;
      border:1px solid var(--gm-line);
      padding:10px;
      margin:10px auto;
    }

    #gambt-mobile-wordpress .gm-modal-head{
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap:8px;
      margin-bottom:10px;
    }

    #gambt-mobile-wordpress .gm-modal-title{
      font-size:16px;
      font-weight:900;
      line-height:1.2;
    }

    #gambt-mobile-wordpress .gm-close{
      width:36px;
      height:36px;
      min-height:36px;
      padding:0;
      flex:0 0 auto;
    }

    #gambt-mobile-wordpress .gm-modal-sub{
      font-size:13px;
      color:var(--gm-muted);
      margin-bottom:10px;
      line-height:1.3;
    }

    #gambt-mobile-wordpress .gm-modal-body{
      display:grid;
      gap:10px;
    }

    #gambt-mobile-wordpress .partido-item-mejorado{
      border:1px solid var(--gm-line);
      background:var(--gm-panel2);
      padding:10px;
    }

    #gambt-mobile-wordpress .partido-header-mejorado{
      display:grid;
      grid-template-columns:24px 1fr auto 24px 1fr;
      gap:6px;
      align-items:center;
      margin-bottom:8px;
    }

    #gambt-mobile-wordpress .escudo-mejorado{
      width:24px;
      height:24px;
      object-fit:contain;
      display:block;
    }

    #gambt-mobile-wordpress .equipo-nombre-mejorado{
      font-size:12px;
      font-weight:900;
      line-height:1.2;
      word-break:break-word;
    }

    #gambt-mobile-wordpress .vs-separator-mejorado{
      font-size:11px;
      font-weight:900;
    }

    #gambt-mobile-wordpress .estado-partido{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      min-height:28px;
      padding:0 10px;
      border:1px solid var(--gm-line2);
      background:#fff;
      font-size:12px;
      font-weight:700;
      margin-bottom:8px;
    }

    #gambt-mobile-wordpress .preguntas-grid-mejorado{
      display:grid;
      gap:8px;
    }

    #gambt-mobile-wordpress .pregunta-grupo-mejorado{
      border:1px solid var(--gm-line2);
      background:#fff;
      padding:8px;
    }

    #gambt-mobile-wordpress .pregunta-titulo-mejorado{
      font-size:12px;
      font-weight:900;
      margin-bottom:8px;
      line-height:1.25;
    }

    #gambt-mobile-wordpress .opciones-grid-mejorado{
      display:grid;
      grid-template-columns:1fr;
      gap:6px;
    }

    #gambt-mobile-wordpress .opcion-mejorada{
      min-height:38px;
      border:1px solid var(--gm-line2);
      background:#fff;
      padding:8px 10px;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      font-size:12px;
      font-weight:700;
      cursor:pointer;
    }

    #gambt-mobile-wordpress .opcion-mejorada.active{
      background:var(--gm-soft);
      border-width:2px;
      border-color:var(--gm-line);
    }

    #gambt-mobile-wordpress .marcador-container-mejorado{
      display:grid;
      grid-template-columns:24px 1fr auto 1fr 24px;
      gap:6px;
      align-items:center;
    }

    #gambt-mobile-wordpress .marcador-input-mejorado{
      min-height:38px;
      text-align:center;
      padding:8px;
    }

    #gambt-mobile-wordpress .marcador-separator{
      font-weight:900;
      font-size:12px;
      text-align:center;
    }

    #gambt-mobile-wordpress .gm-modal-actions{
      display:flex;
      justify-content:center;
      gap:8px;
      margin-top:12px;
      flex-wrap:wrap;
    }

    @media (max-width: 420px){
      #gambt-mobile-wordpress .gm-cards{
        grid-template-columns:1fr 1fr;
      }
      #gambt-mobile-wordpress .gm-history-head,
      #gambt-mobile-wordpress .gm-history-row{
        grid-template-columns:1fr;
      }
      #gambt-mobile-wordpress .gm-history-head{
        display:none;
      }
      #gambt-mobile-wordpress .gm-history-row div{
        border-right:none;
      }
    }

    @media (max-width: 360px){
      #gambt-mobile-wordpress .gm-cards,
      #gambt-mobile-wordpress .gm-tabs{
        grid-template-columns:1fr;
      }
      #gambt-mobile-wordpress .gm-card.gm-full{
        grid-column:auto;
      }
      #gambt-mobile-wordpress .gm-title-row{
        flex-direction:column;
        align-items:stretch;
      }
      #gambt-mobile-wordpress .gm-search{
        width:100%;
      }
    }
  </style>

  <div class="gm-screen">
    <div class="gm-topbar">
      <div class="gm-logo" id="gm-logo">GAMBT</div>
      <div class="gm-topbar-right">
        <button type="button" class="gm-user-chip" id="gm-user-chip">
          <span class="gm-user-icon">👤</span>
          <span class="gm-user-text" id="gm-user-alias">@Invitado</span>
        </button>
        <div class="gm-lang" id="gm-lang">Español ▾</div>
      </div>
    </div>

    <div class="gm-wrap">
      <div class="gm-cards">
        <div class="gm-card">
          <div class="gm-card-title">Saldo virtual</div>
          <div class="gm-card-value" id="gm-saldo">$0.00</div>
          <button type="button" class="gm-btn" id="gm-btn-recargar">RECARGAR +</button>
        </div>

        <div class="gm-card">
          <div class="gm-card-title">Puntos ganados</div>
          <div class="gm-card-value" id="gm-puntos">0 pts</div>
          <div class="gm-mini" id="gm-nivel">Nivel 0</div>
          <div class="gm-mini" id="gm-ranking">Ranking: #0 de 0 jugadores</div>
        </div>

        <div class="gm-card gm-full">
          <div class="gm-card-title">Modo classic</div>
          <div class="gm-mini">Cuotas en vivo, tickets tradicionales.</div>
          <button type="button" class="gm-btn" id="gm-btn-classic" style="margin-top:10px;">Entrar</button>
        </div>
      </div>

      <div class="gm-select-wrap">
        <div class="gm-label">Sección</div>
        <select id="gm-section-select"></select>
      </div>

      <div id="gm-tabs" class="gm-tabs"></div>
      <div id="gm-content"></div>
    </div>
  </div>

  <div class="gm-modal-overlay" id="gm-overlay-public">
    <div class="gm-modal">
      <div class="gm-modal-head">
        <div>
          <div class="gm-modal-title" id="gm-public-title">Partidos</div>
          <div class="gm-modal-sub">Selecciona tus predicciones para cada partido</div>
        </div>
        <button type="button" class="gm-btn gm-close" data-close="public">×</button>
      </div>
      <div class="gm-modal-body" id="gm-public-body"></div>
      <div class="gm-modal-actions">
        <button type="button" class="gm-btn" id="gm-send-public">Enviar apuesta</button>
        <button type="button" class="gm-btn" data-close="public">Cancelar</button>
      </div>
    </div>
  </div>

  <div class="gm-modal-overlay" id="gm-overlay-create">
    <div class="gm-modal">
      <div class="gm-modal-head">
        <div>
          <div class="gm-modal-title">Crear reto</div>
          <div class="gm-modal-sub">Selecciona tus predicciones para cada partido seleccionado</div>
        </div>
        <button type="button" class="gm-btn gm-close" data-close="create">×</button>
      </div>
      <div class="gm-modal-body" id="gm-create-body"></div>
      <div class="gm-modal-actions">
        <button type="button" class="gm-btn" id="gm-send-create">Enviar</button>
        <button type="button" class="gm-btn" data-close="create">Cancelar</button>
      </div>
    </div>
  </div>

  <div class="gm-modal-overlay" id="gm-overlay-private">
    <div class="gm-modal">
      <div class="gm-modal-head">
        <div>
          <div class="gm-modal-title" id="gm-private-title">Reto privado</div>
          <div class="gm-modal-sub">Selecciona tus predicciones para cada partido</div>
        </div>
        <button type="button" class="gm-btn gm-close" data-close="private">×</button>
      </div>
      <div class="gm-modal-body" id="gm-private-body"></div>
      <div class="gm-modal-actions">
        <button type="button" class="gm-btn" id="gm-send-private">Enviar apuesta</button>
        <button type="button" class="gm-btn" data-close="private">Cancelar</button>
      </div>
    </div>
  </div>

  <script>
    (function(){
      const root = document.getElementById('gambt-mobile-wordpress');
      if (!root || root.dataset.booted === '1') return;
      root.dataset.booted = '1';

      const ajaxUrl = '/wp-admin/admin-ajax.php';
      const SECTION_TABS = {
        "UNIRSE MESA": ["Mesas activas", "Histórico de encuentros", "Histórico de apuestas"],
        "CREAR MESA": ["Elegir Deporte", "Configurar Encuentro", "Elegir Partidos", "Histórico de encuentros", "Histórico de apuestas"],
        "MESA JUGADOR": ["Mesas activas", "Histórico de encuentros", "Histórico de apuestas"],
        "MESA PRIVADA": ["Histórico de encuentros", "Histórico de apuestas", "Mesas privadas"]
      };
      const sectionOrder = ["UNIRSE MESA", "CREAR MESA", "MESA JUGADOR", "MESA PRIVADA"];

      function parseUserDataFromStorage(){
        try{
          const raw = localStorage.getItem('user_data');
          if (!raw) return {};
          const data = JSON.parse(raw) || {};
          return data && typeof data === 'object' ? data : {};
        }catch(e){
          return {};
        }
      }

      const storageUserData = parseUserDataFromStorage();

      const state = {
        currentSection: "UNIRSE MESA",
        currentTab: "Mesas activas",
        userId: localStorage.getItem('user_id') || String(storageUserData.id || storageUserData.user_id || storageUserData.uid || ''),
        userAlias: '',
        partidosData: [],
        partidosMap: new Map(),
        deportesSeleccionados: new Set(),
        partidosSeleccionados: new Set(),
        configuracionData: {
          nombreMesa: '',
          deporte: '',
          montoMinimo: '',
          tipoReto: 'Público',
          ganadores: 'Único Ganador',
          preguntasSeleccionadas: [],
          tipoMesa: 'Torneo corto'
        },
        respuestasPartidos: {},
        privadoRespuestas: {},
        mesaActual: null,
        privadoRetoActual: null,
        activeQuestionsMap: null,
        publicRetoConfig: null,
        activeQuestionsPrivado: [],
        tipoMesaActual: null
      };

      const els = {
        sectionSelect: root.querySelector('#gm-section-select'),
        tabs: root.querySelector('#gm-tabs'),
        content: root.querySelector('#gm-content'),
        saldo: root.querySelector('#gm-saldo'),
        puntos: root.querySelector('#gm-puntos'),
        nivel: root.querySelector('#gm-nivel'),
        ranking: root.querySelector('#gm-ranking'),
        logo: root.querySelector('#gm-logo'),
        userChip: root.querySelector('#gm-user-chip'),
        userAlias: root.querySelector('#gm-user-alias'),
        classic: root.querySelector('#gm-btn-classic'),
        recargar: root.querySelector('#gm-btn-recargar'),
        overlayPublic: root.querySelector('#gm-overlay-public'),
        publicBody: root.querySelector('#gm-public-body'),
        publicTitle: root.querySelector('#gm-public-title'),
        sendPublic: root.querySelector('#gm-send-public'),
        overlayCreate: root.querySelector('#gm-overlay-create'),
        createBody: root.querySelector('#gm-create-body'),
        sendCreate: root.querySelector('#gm-send-create'),
        overlayPrivate: root.querySelector('#gm-overlay-private'),
        privateBody: root.querySelector('#gm-private-body'),
        privateTitle: root.querySelector('#gm-private-title'),
        sendPrivate: root.querySelector('#gm-send-private')
      };

      function escapeHtml(value){
        return String(value == null ? '' : value)
          .replace(/&/g,'&amp;')
          .replace(/</g,'&lt;')
          .replace(/>/g,'&gt;')
          .replace(/"/g,'&quot;')
          .replace(/'/g,'&#39;');
      }

      function buildBody(params){
        const fd = new URLSearchParams();
        Object.keys(params || {}).forEach(key => {
          if (params[key] !== undefined && params[key] !== null) fd.append(key, params[key]);
        });
        return fd.toString();
      }

      async function ajaxPost(action, payload = {}, responseType = 'json'){
        const body = buildBody(Object.assign({ action }, payload));
        const resp = await fetch(ajaxUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
          credentials: 'same-origin',
          body
        });
        if (!resp.ok) throw new Error('HTTP ' + resp.status);
        return responseType === 'text' ? resp.text() : resp.json();
      }

      async function ajaxGet(action, payload = {}){
        const qs = buildBody(Object.assign({ action }, payload));
        const resp = await fetch(ajaxUrl + '?' + qs, { credentials: 'same-origin' });
        if (!resp.ok) throw new Error('HTTP ' + resp.status);
        return resp.json();
      }

      function getSuccessData(json){
        if (json && typeof json.success === 'boolean') {
          return json.success ? (json.data !== undefined ? json.data : json) : null;
        }
        return json;
      }

      function alertMsg(msg){
        window.alert(msg);
      }

      function fillSectionSelect(){
        els.sectionSelect.innerHTML = sectionOrder.map(name => `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`).join('');
        els.sectionSelect.value = state.currentSection;
      }

      function renderTabs(){
        const tabs = SECTION_TABS[state.currentSection] || [];
        els.tabs.innerHTML = tabs.map(tab => `
          <button type="button" class="gm-tab ${tab === state.currentTab ? 'active' : ''}" data-tab="${escapeHtml(tab)}">${escapeHtml(tab)}</button>
        `).join('');
      }

      function renderMesasContainer(title, searchId, gridId){
        return `
          <div class="gm-panel">
            <div class="gm-panel-inner">
              <div class="gm-title-row">
                <div class="gm-title-lg">${escapeHtml(title)}</div>
                <input type="text" id="${searchId}" class="gm-search" placeholder="Buscar mesas...">
              </div>
              <div class="mesas-grid" id="${gridId}">
                <div class="historial-vacio">Cargando mesas...</div>
              </div>
            </div>
          </div>
        `;
      }

      function renderHistoricoEncuentros(){
        els.content.innerHTML = `
          <div class="gm-panel">
            <div class="gm-panel-inner">
              <div class="gm-title-lg" style="margin-bottom:10px;">Histórico de encuentros</div>
              <div class="gm-empty">No hay encuentros históricos disponibles</div>
            </div>
          </div>
        `;
      }

      function renderHistoricoApuestasShell(){
        els.content.innerHTML = `
          <div class="gm-panel">
            <div class="gm-panel-inner">
              <div class="gm-title-lg" style="margin-bottom:10px;">Histórico de apuestas</div>
              <div class="gm-history-table">
                <div class="gm-history-head">
                  <div>Partido</div>
                  <div>Predicción</div>
                  <div>Resultado real</div>
                  <div>Estado</div>
                  <div>Fecha</div>
                </div>
                <div id="gm-history-body">
                  <div class="gm-history-row">
                    <div></div>
                    <div></div>
                    <div>No hay apuestas en tu historial</div>
                    <div></div>
                    <div></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;
      }

      function renderElegirDeporte(){
        const nombreMesa = state.configuracionData.nombreMesa || '';
        const deporte = state.configuracionData.deporte || '';
        const deportes = ['Fútbol','Baloncesto','Tenis'];
        els.content.innerHTML = `
          <div class="gm-panel">
            <div class="gm-panel-inner">
              <div class="gm-title-lg" style="margin-bottom:10px;">Elegir deporte</div>

              <div class="gm-field">
                <div class="gm-field-title">Nombre mesa (máximo 30 caracteres)</div>
                <input type="text" id="gm-nombre-mesa" maxlength="30" value="${escapeHtml(nombreMesa)}" placeholder="Ej: Torneo de expertos">
              </div>

              <div class="gm-field">
                <div class="gm-field-title">Deporte</div>
                <div class="gm-option-col">
                  ${deportes.map(item => `
                    <div class="gm-sport ${deporte === item ? 'active' : ''}" data-sport="${escapeHtml(item)}">
                      <span>${escapeHtml(item)}</span>
                      <span>${deporte === item ? '✓' : ''}</span>
                    </div>
                  `).join('')}
                </div>
              </div>

              <div class="gm-next-wrap">
                <button type="button" class="gm-btn" id="gm-next-deporte">SIGUIENTE</button>
              </div>
            </div>
          </div>
        `;
      }

      function renderConfigurarEncuentro(){
        const cfg = state.configuracionData;
        const preguntas = [
          { key:'ganador', label:'Ganador' },
          { key:'ambos_goles', label:'¿Gol de ambos equipos?' },
          { key:'penales', label:'¿Penales?' },
          { key:'marcador', label:'Predice el marcador' }
        ];
        els.content.innerHTML = `
          <div class="gm-panel">
            <div class="gm-panel-inner">
              <div class="gm-field">
                <div class="gm-field-title">Apuesta mínima (USD)</div>
                <input type="number" id="gm-monto-minimo" min="1" step="0.01" value="${escapeHtml(cfg.montoMinimo)}" placeholder="Ej: 10">
              </div>

              <div class="gm-field">
                <div class="gm-field-title">¿Tipo de reto?</div>
                <div class="gm-radio-list">
                  ${['Público','Privado'].map(item => `
                    <div class="gm-radio ${cfg.tipoReto === item ? 'active' : ''}" data-radio-group="tipoReto" data-value="${escapeHtml(item)}">
                      <span>${escapeHtml(item)}</span>
                      <span>${cfg.tipoReto === item ? '◉' : '○'}</span>
                    </div>
                  `).join('')}
                </div>
              </div>

              <div class="gm-field">
                <div class="gm-field-title">¿Cuántos ganadores?</div>
                <div class="gm-radio-list">
                  ${['Único Ganador','Varios Ganadores'].map(item => `
                    <div class="gm-radio ${cfg.ganadores === item ? 'active' : ''}" data-radio-group="ganadores" data-value="${escapeHtml(item)}">
                      <span>${escapeHtml(item)}</span>
                      <span>${cfg.ganadores === item ? '◉' : '○'}</span>
                    </div>
                  `).join('')}
                </div>
              </div>

              <div class="gm-field">
                <div class="gm-field-title">¿Preguntas por encuentro? (Selecciona 1-4)</div>
                <div class="gm-option-col">
                  ${preguntas.map(item => `
                    <div class="gm-question ${cfg.preguntasSeleccionadas.includes(item.key) ? 'active' : ''}" data-question="${escapeHtml(item.key)}">
                      <span>${escapeHtml(item.label)}</span>
                      <span>${cfg.preguntasSeleccionadas.includes(item.key) ? '✓' : ''}</span>
                    </div>
                  `).join('')}
                </div>
              </div>

              <div class="gm-field">
                <div class="gm-field-title">¿Tipo de mesa?</div>
                <div class="gm-radio-list">
                  ${['Selección','Torneo corto','Torneo largo'].map(item => `
                    <div class="gm-radio ${cfg.tipoMesa === item ? 'active' : ''}" data-radio-group="tipoMesa" data-value="${escapeHtml(item)}">
                      <span>${escapeHtml(item)}</span>
                      <span>${cfg.tipoMesa === item ? '◉' : '○'}</span>
                    </div>
                  `).join('')}
                </div>
              </div>

              <div class="gm-next-wrap">
                <button type="button" class="gm-btn" id="gm-next-config">SIGUIENTE</button>
              </div>
            </div>
          </div>
        `;
      }

      function buildPickCard(partido){
        const selected = state.partidosSeleccionados.has(String(partido.id));
        return `
          <div class="gm-pick-card ${selected ? 'selected' : ''}" data-pick-id="${escapeHtml(partido.id)}">
            <div class="gm-pick-check"></div>
            <div>
              <div class="gm-pick-title">${escapeHtml(partido.local.nombre)} vs ${escapeHtml(partido.visita.nombre)}</div>
              <div class="gm-pick-meta">
                Horario: ${escapeHtml(partido.horario || '')}<br>
                Estado: ${escapeHtml(partido.estado || 'Disponible')}
              </div>
              <div class="gm-pick-tag">Agregar al reto</div>
            </div>
          </div>
        `;
      }

      function renderElegirPartidos(){
        els.content.innerHTML = `
          <div class="gm-panel">
            <div class="gm-panel-inner">
              <div class="gm-title-lg" style="margin-bottom:10px;">Partidos disponibles</div>
              <div class="gm-pick-cards">
                ${state.partidosData.length ? state.partidosData.map(buildPickCard).join('') : '<div class="historial-vacio">No hay partidos disponibles</div>'}
              </div>
              <div class="gm-next-wrap">
                <button type="button" class="gm-btn" id="gm-open-create-modal" ${state.partidosSeleccionados.size ? '' : 'disabled'}>ENVIAR</button>
              </div>
            </div>
          </div>
        `;
      }

      function renderMesasActivasView(){
        els.content.innerHTML = renderMesasContainer('Mesas activas disponibles', 'gm-search-activas', 'gm-grid-activas');
      }

      function renderMesasPrivadasView(){
        els.content.innerHTML = renderMesasContainer('Mesas privadas', 'gm-search-privadas', 'gm-grid-privadas');
      }

      function renderContent(){
        if (state.currentTab === 'Mesas activas') {
          renderMesasActivasView();
          loadMesasActivas();
          return;
        }
        if (state.currentTab === 'Mesas privadas') {
          renderMesasPrivadasView();
          loadMesasPrivadas();
          return;
        }
        if (state.currentTab === 'Histórico de encuentros') {
          renderHistoricoEncuentros();
          return;
        }
        if (state.currentTab === 'Histórico de apuestas') {
          renderHistoricoApuestasShell();
          loadHistorial();
          return;
        }
        if (state.currentTab === 'Elegir Deporte') {
          renderElegirDeporte();
          return;
        }
        if (state.currentTab === 'Configurar Encuentro') {
          renderConfigurarEncuentro();
          return;
        }
        if (state.currentTab === 'Elegir Partidos') {
          renderElegirPartidos();
          return;
        }
      }

      function render(){
        fillSectionSelect();
        renderTabs();
        renderContent();
      }

      function closeOverlay(which){
        if (which === 'public') {
          els.overlayPublic.style.display = 'none';
          els.publicBody.innerHTML = '';
          state.mesaActual = null;
          state.respuestasPartidos = {};
          state.activeQuestionsMap = null;
          state.publicRetoConfig = null;
          state.tipoMesaActual = null;
        }
        if (which === 'create') {
          els.overlayCreate.style.display = 'none';
          els.createBody.innerHTML = '';
          state.respuestasPartidos = {};
        }
        if (which === 'private') {
          els.overlayPrivate.style.display = 'none';
          els.privateBody.innerHTML = '';
          state.privadoRetoActual = null;
          state.privadoRespuestas = {};
          state.activeQuestionsPrivado = [];
        }
      }

      function openOverlay(which){
        if (which === 'public') els.overlayPublic.style.display = 'flex';
        if (which === 'create') els.overlayCreate.style.display = 'flex';
        if (which === 'private') els.overlayPrivate.style.display = 'flex';
      }

      function parseUserAliasFromLocalStorage(){
        const u = parseUserDataFromStorage();
        return u.alias || u.nombre || u.username || '';
      }

      function formatAlias(value){
        const clean = String(value || '').trim();
        if (!clean || clean.toLowerCase() === 'invitado') return '@Invitado';
        return clean.startsWith('@') ? clean : '@' + clean;
      }

      function paintUserAlias(){
        if (!els.userAlias) return;
        els.userAlias.textContent = formatAlias(state.userAlias || 'Invitado');
      }

      function persistResolvedUser(){
        if (state.userId) localStorage.setItem('user_id', String(state.userId));
        const current = parseUserDataFromStorage();
        const next = Object.assign({}, current);
        if (state.userAlias) next.alias = String(state.userAlias).replace(/^@+/, '');
        if (state.userId) next.user_id = String(state.userId);
        localStorage.setItem('user_data', JSON.stringify(next));
      }

      async function loadUserInfo(){
        const localAlias = parseUserAliasFromLocalStorage();
        if (localAlias) state.userAlias = localAlias;
        paintUserAlias();
        try{
          const json = await ajaxGet('gambt_user_info', {});
          const data = getSuccessData(json) || {};
          if (data.name && data.name !== 'Invitado') state.userAlias = data.name;
          if ((!state.userId || state.userId === '0') && data.user_id) {
            state.userId = String(data.user_id);
          }
          paintUserAlias();
          persistResolvedUser();
        }catch(e){
          paintUserAlias();
          if (state.userId || state.userAlias) persistResolvedUser();
        }
      }

      async function loadSaldo(){
        if (!state.userId) return;
        try{
          const json = await ajaxGet('gambt_obtener_saldo', { user_id: state.userId });
          const data = getSuccessData(json);
          if (data && typeof data.saldo !== 'undefined') {
            els.saldo.textContent = '$' + Number(data.saldo).toFixed(2);
          }
        }catch(e){}
      }

      async function loadPuntos(){
        if (!state.userId) return;
        try{
          const json = await ajaxGet('gambt_puntos_usuario', { user_id: state.userId });
          const data = getSuccessData(json);
          if (data && typeof data.puntos_actuales !== 'undefined') {
            els.puntos.textContent = Number(data.puntos_actuales).toLocaleString() + ' pts';
            els.nivel.textContent = data.nivel ? String(data.nivel) : 'Nivel 0';
            els.ranking.textContent = 'Ranking: #' + Number(data.posicion_actual || 0) + ' de ' + Number(data.cantidad_jugadores || 0) + ' jugadores';
          }
        }catch(e){}
      }

      async function loadMatches(){
        try{
          const html = await ajaxGetTextRetos();
          const temp = document.createElement('div');
          temp.innerHTML = html;
          const filas = temp.querySelectorAll('tbody tr[data-mid]');
          state.partidosData = [];
          state.partidosMap.clear();

          filas.forEach(fila => {
            const partidoId = fila.getAttribute('data-mid');
            const celdas = fila.querySelectorAll('td');
            const equipoDiv = celdas[0] ? celdas[0].querySelector('.g-row') : null;
            if (!equipoDiv) return;

            const escudos = equipoDiv.querySelectorAll('img.g-logo');
            const textos = equipoDiv.querySelectorAll('span');
            const partido = {
              id: String(partidoId),
              local: { nombre: textos[0] ? textos[0].textContent.trim() : 'Local', escudo: escudos[0] ? escudos[0].src : '' },
              visita: { nombre: textos[2] ? textos[2].textContent.trim() : 'Visitante', escudo: escudos[1] ? escudos[1].src : '' },
              horario: celdas[1] ? celdas[1].textContent.trim() : '',
              estado: 'SCHEDULED'
            };
            state.partidosData.push(partido);
            state.partidosMap.set(String(partido.id), partido);
          });

          if (!state.partidosData.length) loadStaticMatches();
        }catch(e){
          loadStaticMatches();
        }
      }

      async function ajaxGetTextRetos(){
        const resp = await fetch(ajaxUrl + '?action=gambt_retos_grupales_ajax', { credentials:'same-origin' });
        if (!resp.ok) throw new Error('HTTP ' + resp.status);
        return resp.text();
      }

      function loadStaticMatches(){
        const items = [
          { id:'p1', local:{ nombre:'Gil Vicente', escudo:'' }, visita:{ nombre:'Casa Pia', escudo:'' }, horario:'', estado:'SCHEDULED' },
          { id:'p2', local:{ nombre:'Tondela', escudo:'' }, visita:{ nombre:'CD Nacional', escudo:'' }, horario:'', estado:'SCHEDULED' },
          { id:'p3', local:{ nombre:'Santa Clara', escudo:'' }, visita:{ nombre:'Braga', escudo:'' }, horario:'', estado:'SCHEDULED' },
          { id:'p4', local:{ nombre:'AVS', escudo:'' }, visita:{ nombre:'Sporting CP', escudo:'' }, horario:'', estado:'SCHEDULED' },
          { id:'p5', local:{ nombre:'Estoril Praia', escudo:'' }, visita:{ nombre:'Famalicão', escudo:'' }, horario:'', estado:'SCHEDULED' }
        ];
        state.partidosData = items;
        state.partidosMap.clear();
        items.forEach(p => state.partidosMap.set(String(p.id), p));
      }

      async function loadMesasActivas(){
        const grid = root.querySelector('#gm-grid-activas');
        const search = root.querySelector('#gm-search-activas');
        if (!grid) return;
        grid.innerHTML = '<div class="historial-vacio">Cargando mesas activas...</div>';
        try{
          const json = await ajaxPost('gambt_cargar_mesas_activas', { cargar_mesas: 'true' });
          const data = getSuccessData(json);
          if (data && data.html) {
            grid.innerHTML = data.html;
          } else {
            grid.innerHTML = '<div class="historial-vacio">No hay mesas disponibles</div>';
          }
        }catch(e){
          grid.innerHTML = '<div class="historial-vacio">Error al cargar mesas</div>';
        }
        if (search) {
          search.value = '';
          search.addEventListener('input', filterMesasActivas, { once:false });
        }
      }

      function filterMesasActivas(){
        const grid = root.querySelector('#gm-grid-activas');
        const search = root.querySelector('#gm-search-activas');
        if (!grid || !search) return;
        const term = search.value.toLowerCase().trim();
        grid.querySelectorAll('.mesa-card').forEach(card => {
          const title = card.querySelector('.mesa-titulo');
          const text = title ? title.textContent.toLowerCase() : '';
          card.style.display = !term || text.includes(term) ? '' : 'none';
        });
      }

      async function loadMesasPrivadas(){
        const grid = root.querySelector('#gm-grid-privadas');
        const search = root.querySelector('#gm-search-privadas');
        if (!grid) return;
        grid.innerHTML = '<div class="historial-vacio">Cargando mesas privadas...</div>';
        try{
          const json = await ajaxPost('gambt_cargar_mesas_privadas', { cargar: 'true', user_id: state.userId || '' });
          const data = getSuccessData(json);
          if (data && data.html) {
            grid.innerHTML = data.html;
          } else {
            grid.innerHTML = '<div class="historial-vacio">No hay mesas privadas disponibles</div>';
          }
        }catch(e){
          grid.innerHTML = '<div class="historial-vacio">Error de conexión</div>';
        }
        if (search) {
          search.value = '';
          search.addEventListener('input', filterMesasPrivadas, { once:false });
        }
      }

      function filterMesasPrivadas(){
        const grid = root.querySelector('#gm-grid-privadas');
        const search = root.querySelector('#gm-search-privadas');
        if (!grid || !search) return;
        const term = search.value.toLowerCase().trim();
        grid.querySelectorAll('.mesa-card').forEach(card => {
          const title = card.querySelector('.mesa-titulo');
          const text = title ? title.textContent.toLowerCase() : '';
          card.style.display = !term || text.includes(term) ? '' : 'none';
        });
      }

      async function loadHistorial(){
        const body = root.querySelector('#gm-history-body');
        if (!body) return;
        if (!state.userId) {
          body.innerHTML = '<div class="gm-history-row"><div></div><div></div><div>Usuario no identificado</div><div></div><div></div></div>';
          return;
        }
        try{
          const json = await ajaxGet('gambt_obtener_historial', { user_id: state.userId });
          const data = getSuccessData(json) || {};
          const apuestas = data.apuestas || [];
          if (!apuestas.length) {
            body.innerHTML = '<div class="gm-history-row"><div></div><div></div><div>No hay apuestas en tu historial</div><div></div><div></div></div>';
            return;
          }
          body.innerHTML = apuestas.map(apuesta => {
            let fecha = '';
            try {
              fecha = new Date(apuesta.fecha_apuesta).toLocaleDateString('es-ES', {
                day:'2-digit', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit'
              });
            } catch(e){}
            const resultado = apuesta.resultado_ia || 'Pendiente';
            const cls = String(resultado).toLowerCase() === 'victoria' ? 'gm-chip-ok' : (String(resultado).toLowerCase() === 'derrota' ? 'gm-chip-bad' : '');
            return `
              <div class="gm-history-row">
                <div>${escapeHtml(apuesta.partido || ('Partido ' + (apuesta.partido_id || 'N/A')))}</div>
                <div>${escapeHtml(apuesta.ganador || 'N/A')} (${escapeHtml(apuesta.marcador_local || 0)}-${escapeHtml(apuesta.marcador_visita || 0)})</div>
                <div>${escapeHtml(apuesta.ganador_real || 'N/A')} (${escapeHtml(apuesta.marcador_local_real || 0)}-${escapeHtml(apuesta.marcador_visita_real || 0)})</div>
                <div class="${cls}">${escapeHtml(resultado)}</div>
                <div>${escapeHtml(fecha)}</div>
              </div>
            `;
          }).join('');
        }catch(e){
          body.innerHTML = '<div class="gm-history-row"><div></div><div></div><div>Error al cargar el historial</div><div></div><div></div></div>';
        }
      }

      function buildPredictionBlock(partidoId, localNombre, visitaNombre, localEscudo, visitaEscudo, activeQuestions){
        let q = 1;
        let html = '';

        if (activeQuestions.includes('ganador')) {
          html += `
            <div class="pregunta-grupo-mejorado">
              <div class="pregunta-titulo-mejorado">PREGUNTA ${q} — GANADOR</div>
              <div class="opciones-grid-mejorado">
                <div class="opcion-mejorada" data-context="public" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ganador" data-valor="Empate">Empate</div>
                <div class="opcion-mejorada" data-context="public" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ganador" data-valor="${escapeHtml(localNombre)}">${escapeHtml(localNombre)}</div>
                <div class="opcion-mejorada" data-context="public" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ganador" data-valor="${escapeHtml(visitaNombre)}">${escapeHtml(visitaNombre)}</div>
              </div>
            </div>
          `;
          q++;
        }

        if (activeQuestions.includes('ambos_goles')) {
          html += `
            <div class="pregunta-grupo-mejorado">
              <div class="pregunta-titulo-mejorado">PREGUNTA ${q} — ¿GOL DE AMBOS EQUIPOS?</div>
              <div class="opciones-grid-mejorado">
                <div class="opcion-mejorada" data-context="public" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ambos_goles" data-valor="Sí">Sí</div>
                <div class="opcion-mejorada" data-context="public" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ambos_goles" data-valor="No">No</div>
                <div class="opcion-mejorada" data-context="public" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ambos_goles" data-valor="Ninguno anota">Ninguno anota</div>
              </div>
            </div>
          `;
          q++;
        }

        if (activeQuestions.includes('penales')) {
          html += `
            <div class="pregunta-grupo-mejorado">
              <div class="pregunta-titulo-mejorado">PREGUNTA ${q} — ¿PENALES?</div>
              <div class="opciones-grid-mejorado">
                <div class="opcion-mejorada" data-context="public" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="penales" data-valor="Sí">Sí</div>
                <div class="opcion-mejorada" data-context="public" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="penales" data-valor="No">No</div>
              </div>
            </div>
          `;
          q++;
        }

        if (activeQuestions.includes('marcador')) {
          html += `
            <div class="pregunta-grupo-mejorado">
              <div class="pregunta-titulo-mejorado">PREGUNTA ${q} — PREDICE EL MARCADOR</div>
              <div class="marcador-container-mejorado">
                <img src="${escapeHtml(localEscudo || '')}" class="escudo-mejorado" alt="${escapeHtml(localNombre)}">
                <input type="number" class="marcador-input-mejorado" data-context="public" data-partido-id="${escapeHtml(partidoId)}" data-tipo="local" min="0" max="9" value="">
                <span class="marcador-separator">VS</span>
                <input type="number" class="marcador-input-mejorado" data-context="public" data-partido-id="${escapeHtml(partidoId)}" data-tipo="visitante" min="0" max="9" value="">
                <img src="${escapeHtml(visitaEscudo || '')}" class="escudo-mejorado" alt="${escapeHtml(visitaNombre)}">
              </div>
            </div>
          `;
        }

        return html;
      }

      function buildPrivatePredictionBlock(partidoId, localNombre, visitaNombre, localEscudo, visitaEscudo, activeQuestions){
        let q = 1;
        let html = '';

        if (activeQuestions.includes('ganador')) {
          html += `
            <div class="pregunta-grupo-mejorado">
              <div class="pregunta-titulo-mejorado">PREGUNTA ${q} — GANADOR</div>
              <div class="opciones-grid-mejorado">
                <div class="opcion-mejorada" data-context="private" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ganador" data-valor="Empate">Empate</div>
                <div class="opcion-mejorada" data-context="private" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ganador" data-valor="${escapeHtml(localNombre)}">${escapeHtml(localNombre)}</div>
                <div class="opcion-mejorada" data-context="private" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ganador" data-valor="${escapeHtml(visitaNombre)}">${escapeHtml(visitaNombre)}</div>
              </div>
            </div>
          `;
          q++;
        }

        if (activeQuestions.includes('ambos_goles')) {
          html += `
            <div class="pregunta-grupo-mejorado">
              <div class="pregunta-titulo-mejorado">PREGUNTA ${q} — ¿GOL DE AMBOS EQUIPOS?</div>
              <div class="opciones-grid-mejorado">
                <div class="opcion-mejorada" data-context="private" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ambos_goles" data-valor="Sí">Sí</div>
                <div class="opcion-mejorada" data-context="private" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ambos_goles" data-valor="No">No</div>
                <div class="opcion-mejorada" data-context="private" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ambos_goles" data-valor="Ninguno anota">Ninguno anota</div>
              </div>
            </div>
          `;
          q++;
        }

        if (activeQuestions.includes('penales')) {
          html += `
            <div class="pregunta-grupo-mejorado">
              <div class="pregunta-titulo-mejorado">PREGUNTA ${q} — ¿PENALES?</div>
              <div class="opciones-grid-mejorado">
                <div class="opcion-mejorada" data-context="private" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="penales" data-valor="Sí">Sí</div>
                <div class="opcion-mejorada" data-context="private" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="penales" data-valor="No">No</div>
              </div>
            </div>
          `;
          q++;
        }

        if (activeQuestions.includes('marcador')) {
          html += `
            <div class="pregunta-grupo-mejorado">
              <div class="pregunta-titulo-mejorado">PREGUNTA ${q} — PREDICE EL MARCADOR</div>
              <div class="marcador-container-mejorado">
                <img src="${escapeHtml(localEscudo || '')}" class="escudo-mejorado" alt="${escapeHtml(localNombre)}">
                <input type="number" class="marcador-input-mejorado" data-context="private" data-partido-id="${escapeHtml(partidoId)}" data-tipo="local" min="0" max="9" value="">
                <span class="marcador-separator">VS</span>
                <input type="number" class="marcador-input-mejorado" data-context="private" data-partido-id="${escapeHtml(partidoId)}" data-tipo="visitante" min="0" max="9" value="">
                <img src="${escapeHtml(visitaEscudo || '')}" class="escudo-mejorado" alt="${escapeHtml(visitaNombre)}">
              </div>
            </div>
          `;
        }

        return html;
      }

      function buildCreatePredictionBlock(partidoId, localNombre, visitaNombre, localEscudo, visitaEscudo, selectedQuestions){
        let q = 1;
        let html = '';

        if (selectedQuestions.includes('ganador')) {
          html += `
            <div class="pregunta-grupo-mejorado">
              <div class="pregunta-titulo-mejorado">PREGUNTA ${q} — GANADOR</div>
              <div class="opciones-grid-mejorado">
                <div class="opcion-mejorada" data-context="create" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ganador" data-valor="Empate">Empate</div>
                <div class="opcion-mejorada" data-context="create" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ganador" data-valor="${escapeHtml(localNombre)}">${escapeHtml(localNombre)}</div>
                <div class="opcion-mejorada" data-context="create" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ganador" data-valor="${escapeHtml(visitaNombre)}">${escapeHtml(visitaNombre)}</div>
              </div>
            </div>
          `;
          q++;
        }

        if (selectedQuestions.includes('ambos_goles')) {
          html += `
            <div class="pregunta-grupo-mejorado">
              <div class="pregunta-titulo-mejorado">PREGUNTA ${q} — ¿GOL DE AMBOS EQUIPOS?</div>
              <div class="opciones-grid-mejorado">
                <div class="opcion-mejorada" data-context="create" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ambos_goles" data-valor="Sí">Sí</div>
                <div class="opcion-mejorada" data-context="create" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ambos_goles" data-valor="No">No</div>
                <div class="opcion-mejorada" data-context="create" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="ambos_goles" data-valor="Ninguno anota">Ninguno anota</div>
              </div>
            </div>
          `;
          q++;
        }

        if (selectedQuestions.includes('penales')) {
          html += `
            <div class="pregunta-grupo-mejorado">
              <div class="pregunta-titulo-mejorado">PREGUNTA ${q} — ¿PENALES?</div>
              <div class="opciones-grid-mejorado">
                <div class="opcion-mejorada" data-context="create" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="penales" data-valor="Sí">Sí</div>
                <div class="opcion-mejorada" data-context="create" data-partido-id="${escapeHtml(partidoId)}" data-pregunta="penales" data-valor="No">No</div>
              </div>
            </div>
          `;
          q++;
        }

        if (selectedQuestions.includes('marcador')) {
          html += `
            <div class="pregunta-grupo-mejorado">
              <div class="pregunta-titulo-mejorado">PREGUNTA ${q} — PREDICE EL MARCADOR</div>
              <div class="marcador-container-mejorado">
                <img src="${escapeHtml(localEscudo || '')}" class="escudo-mejorado" alt="${escapeHtml(localNombre)}">
                <input type="number" class="marcador-input-mejorado" data-context="create" data-partido-id="${escapeHtml(partidoId)}" data-tipo="local" min="0" max="9" value="">
                <span class="marcador-separator">VS</span>
                <input type="number" class="marcador-input-mejorado" data-context="create" data-partido-id="${escapeHtml(partidoId)}" data-tipo="visitante" min="0" max="9" value="">
                <img src="${escapeHtml(visitaEscudo || '')}" class="escudo-mejorado" alt="${escapeHtml(visitaNombre)}">
              </div>
            </div>
          `;
        }

        return html;
      }

      function ensureResponseContainer(context, partidoId){
        if (context === 'public') {
          if (!state.respuestasPartidos[partidoId]) {
            state.respuestasPartidos[partidoId] = { id_partido: partidoId, estado_partido:'SCHEDULED', ganador:'', ambos_goles:'', penales:'', marcador:{ local:'', visitante:'' } };
          }
          return state.respuestasPartidos[partidoId];
        }
        if (context === 'create') {
          if (!state.respuestasPartidos[partidoId]) {
            state.respuestasPartidos[partidoId] = { id_partido: partidoId, estado_partido:'SCHEDULED', ganador:'NO_APLICA', ambos_goles:99, penales:99, marcador:{ local:99, visitante:99 } };
          }
          return state.respuestasPartidos[partidoId];
        }
        if (context === 'private') {
          if (!state.privadoRespuestas[partidoId]) {
            state.privadoRespuestas[partidoId] = { id_partido: partidoId, estado_partido:'SCHEDULED', ganador:'NO_APLICA', ambos_goles:99, penales:99, marcador:{ local:99, visitante:99 } };
          }
          return state.privadoRespuestas[partidoId];
        }
        return null;
      }

      function handleOptionSelection(el){
        const context = el.getAttribute('data-context');
        const partidoId = el.getAttribute('data-partido-id');
        const pregunta = el.getAttribute('data-pregunta');
        const valor = el.getAttribute('data-valor');
        if (!context || !partidoId || !pregunta) return;
        const wrap = el.closest('.pregunta-grupo-mejorado');
        if (wrap) {
          wrap.querySelectorAll('.opcion-mejorada').forEach(opt => {
            if (opt.getAttribute('data-pregunta') === pregunta && opt.getAttribute('data-partido-id') === partidoId) {
              opt.classList.remove('active');
            }
          });
        }
        el.classList.add('active');
        const target = ensureResponseContainer(context, partidoId);
        if (target) target[pregunta] = valor;
      }

      function handleScoreInput(el){
        const context = el.getAttribute('data-context');
        const partidoId = el.getAttribute('data-partido-id');
        const tipo = el.getAttribute('data-tipo');
        let value = el.value;
        if (value === '') value = '';
        else {
          value = Math.max(0, Math.min(9, parseInt(value, 10) || 0));
          el.value = value;
        }
        const target = ensureResponseContainer(context, partidoId);
        if (!target) return;
        if (!target.marcador || typeof target.marcador !== 'object') target.marcador = {};
        target.marcador[tipo] = value;
      }

      async function showPartidosPublicos(llave, nombreMesa){
        state.tipoMesaActual = 'publica';
        state.mesaActual = llave;
        state.respuestasPartidos = {};
        state.activeQuestionsMap = {};
        state.publicRetoConfig = null;
        els.publicTitle.textContent = 'Partidos - ' + nombreMesa;
        els.publicBody.innerHTML = '<div class="historial-vacio">Cargando partidos...</div>';
        openOverlay('public');

        try{
          const json = await ajaxPost('gambt_cargar_partidos_publicos', { llave });
          const data = getSuccessData(json);
          if (!data || !data.partidos || !data.partidos.length) {
            alertMsg('No hay partidos en este reto');
            closeOverlay('public');
            return;
          }
          const partidos = data.partidos;
          const config = data.config || {};
          const first = partidos[0];
          const activeQuestions = [];
          if (first.ganador !== 'NO_APLICA') activeQuestions.push('ganador');
          if (Number(first.ambos_anotan) != 99) activeQuestions.push('ambos_goles');
          if (Number(first.penales) != 99) activeQuestions.push('penales');
          if (Number(first.marcador_local) != 99 || Number(first.marcador_visita) != 99) activeQuestions.push('marcador');

          state.publicRetoConfig = {
            nombre_mesa: config.nombre_mesa || nombreMesa,
            apuesta_minima_usd: Number(config.apuesta_minima_usd || 0),
            preguntas_por_encuentro: activeQuestions.length
          };

          els.publicBody.innerHTML = partidos.map(p => {
            const partidoId = String(p.partido_id);
            state.activeQuestionsMap[partidoId] = activeQuestions.slice();
            state.respuestasPartidos[partidoId] = {
              id_partido: partidoId,
              estado_partido: 'SCHEDULED',
              ganador: activeQuestions.includes('ganador') ? '' : 'NO_APLICA',
              ambos_goles: activeQuestions.includes('ambos_goles') ? '' : 99,
              penales: activeQuestions.includes('penales') ? '' : 99,
              marcador: activeQuestions.includes('marcador') ? { local:'', visitante:'' } : { local:99, visitante:99 }
            };
            return `
              <div class="partido-item-mejorado" data-partido-id="${escapeHtml(partidoId)}">
                <div class="partido-header-mejorado">
                  <img src="${escapeHtml(p.local_escudo || '')}" class="escudo-mejorado" alt="${escapeHtml(p.local_nombre)}">
                  <span class="equipo-nombre-mejorado">${escapeHtml(p.local_nombre)}</span>
                  <span class="vs-separator-mejorado">VS</span>
                  <img src="${escapeHtml(p.visita_escudo || '')}" class="escudo-mejorado" alt="${escapeHtml(p.visita_nombre)}">
                  <span class="equipo-nombre-mejorado">${escapeHtml(p.visita_nombre)}</span>
                </div>
                <div class="preguntas-grid-mejorado">
                  ${buildPredictionBlock(partidoId, p.local_nombre, p.visita_nombre, p.local_escudo, p.visita_escudo, activeQuestions)}
                </div>
              </div>
            `;
          }).join('');
        }catch(e){
          alertMsg('Error de conexión al cargar partidos');
          closeOverlay('public');
        }
      }

      async function showPartidosMesa(grupoRango, nombreMesa, apuestaMinima){
        state.tipoMesaActual = 'local';
        state.mesaActual = grupoRango;
        state.respuestasPartidos = {};
        state.activeQuestionsMap = null;
        state.publicRetoConfig = {
          nombre_mesa: nombreMesa,
          apuesta_minima_usd: Number(apuestaMinima || 10),
          preguntas_por_encuentro: 4
        };
        els.publicTitle.textContent = 'Partidos - ' + nombreMesa;
        els.publicBody.innerHTML = '<div class="historial-vacio">Cargando partidos...</div>';
        openOverlay('public');

        try{
          const json = await ajaxPost('gambt_cargar_partidos_mesa', { grupo_rango: grupoRango });
          const data = getSuccessData(json);
          if (!data || !data.html) {
            alertMsg('No se encontraron partidos');
            closeOverlay('public');
            return;
          }
          els.publicBody.innerHTML = data.html;
          els.publicBody.querySelectorAll('.partido-item-mejorado').forEach(item => {
            const partidoId = String(item.getAttribute('data-partido-id'));
            const estadoEl = item.querySelector('.estado-partido');
            const estado = estadoEl ? estadoEl.textContent.trim() : 'SCHEDULED';
            state.respuestasPartidos[partidoId] = {
              id_partido: partidoId,
              estado_partido: estado,
              ganador: '',
              ambos_goles: '',
              penales: '',
              marcador: { local:0, visitante:0 }
            };
          });
        }catch(e){
          alertMsg('Error de conexión al cargar partidos');
          closeOverlay('public');
        }
      }

      function validatePublicResponses(){
        const partidos = els.publicBody.querySelectorAll('.partido-item-mejorado');
        if (!partidos.length) return false;
        for (const partido of partidos) {
          const partidoId = partido.getAttribute('data-partido-id');
          const respuestas = state.respuestasPartidos[partidoId];
          if (!respuestas) return false;
          let required = ['ganador','ambos_goles','penales'];
          if (state.activeQuestionsMap && state.activeQuestionsMap[partidoId]) required = state.activeQuestionsMap[partidoId];
          for (const pregunta of required) {
            if (pregunta === 'marcador') continue;
            if (respuestas[pregunta] === '' || respuestas[pregunta] === undefined || respuestas[pregunta] === null) return false;
          }
        }
        return true;
      }

      async function sendPublicBet(){
        if (!validatePublicResponses()) {
          alertMsg('Por favor responde todas las preguntas para cada partido');
          return;
        }
        if (!state.userId) {
          alertMsg('Usuario no identificado');
          return;
        }

        Object.keys(state.respuestasPartidos).forEach(partidoId => {
          const resp = state.respuestasPartidos[partidoId];
          if (resp.marcador) {
            if (resp.marcador.local === '' || resp.marcador.local === null || resp.marcador.local === undefined) resp.marcador.local = 0;
            if (resp.marcador.visitante === '' || resp.marcador.visitante === null || resp.marcador.visitante === undefined) resp.marcador.visitante = 0;
          } else {
            resp.marcador = { local:0, visitante:0 };
          }
        });

        const apuestaData = {
          user_id: state.userId,
          grupo_rango: state.mesaActual,
          fecha_apuesta: new Date().toISOString().slice(0, 19).replace('T', ' '),
          respuestas: state.respuestasPartidos
        };

        if (state.tipoMesaActual === 'publica') apuestaData.modo_forzado = 'Acepta_reto';
        if (state.tipoMesaActual === 'local') apuestaData.modo_forzado = 'Acepta_reto_local';

        if (state.publicRetoConfig) {
          apuestaData.apuesta_minima_usd = state.publicRetoConfig.apuesta_minima_usd;
          apuestaData.nombre_mesa = state.publicRetoConfig.nombre_mesa;
          apuestaData.preguntas_por_encuentro = state.publicRetoConfig.preguntas_por_encuentro;
        }

        try{
          const json = await ajaxPost('gambt_guardar_apuesta_ppm', { apuesta_data: JSON.stringify(apuestaData) });
          if (json && json.success) {
            alertMsg('Apuesta guardada correctamente');
            closeOverlay('public');
            await Promise.all([loadSaldo(), loadPuntos()]);
            if (state.currentTab === 'Mesas activas') loadMesasActivas();
          } else {
            alertMsg('Error al guardar la apuesta: ' + ((json && json.data) || ''));
          }
        }catch(e){
          alertMsg('Error de conexión al enviar apuesta');
        }
      }

      function validateCreateConfig(){
        const nombreMesa = root.querySelector('#gm-nombre-mesa');
        if (nombreMesa) state.configuracionData.nombreMesa = nombreMesa.value.trim();
        if (!state.configuracionData.nombreMesa) {
          alertMsg('El nombre de la mesa es obligatorio');
          return false;
        }
        if (!state.configuracionData.deporte) {
          alertMsg('Debes seleccionar un deporte');
          return false;
        }
        return true;
      }

      function validateConfigStep(){
        const monto = root.querySelector('#gm-monto-minimo');
        if (monto) state.configuracionData.montoMinimo = monto.value;
        const montoN = Number(state.configuracionData.montoMinimo || 0);
        if (!(montoN > 0)) {
          alertMsg('La apuesta mínima es obligatoria');
          return false;
        }
        if (!state.configuracionData.preguntasSeleccionadas.length) {
          alertMsg('Debes seleccionar mínimo una pregunta');
          return false;
        }
        return true;
      }

      function openCreateModal(){
        if (!state.partidosSeleccionados.size) {
          alertMsg('Por favor selecciona al menos un partido');
          return;
        }
        if (!state.configuracionData.preguntasSeleccionadas.length) {
          alertMsg('Primero debes configurar las preguntas en Configurar Encuentro');
          state.currentTab = 'Configurar Encuentro';
          render();
          return;
        }
        if (!state.configuracionData.nombreMesa) {
          alertMsg('El nombre de la mesa es obligatorio');
          state.currentTab = 'Elegir Deporte';
          render();
          return;
        }

        state.respuestasPartidos = {};
        const selected = Array.from(state.partidosSeleccionados);
        els.createBody.innerHTML = selected.map(id => {
          const partido = state.partidosMap.get(String(id));
          if (!partido) return '';
          const selectedQuestions = state.configuracionData.preguntasSeleccionadas.slice();
          state.respuestasPartidos[String(id)] = {
            id_partido: String(id),
            estado_partido: partido.estado || 'SCHEDULED',
            ganador: selectedQuestions.includes('ganador') ? '' : 'NO_APLICA',
            ambos_goles: selectedQuestions.includes('ambos_goles') ? '' : 99,
            penales: selectedQuestions.includes('penales') ? '' : 99,
            marcador: selectedQuestions.includes('marcador') ? { local:'', visitante:'' } : { local:99, visitante:99 }
          };
          return `
            <div class="partido-item-mejorado" data-partido-id="${escapeHtml(id)}">
              <div class="partido-header-mejorado">
                <img src="${escapeHtml(partido.local.escudo || '')}" class="escudo-mejorado" alt="${escapeHtml(partido.local.nombre)}">
                <span class="equipo-nombre-mejorado">${escapeHtml(partido.local.nombre)}</span>
                <span class="vs-separator-mejorado">VS</span>
                <img src="${escapeHtml(partido.visita.escudo || '')}" class="escudo-mejorado" alt="${escapeHtml(partido.visita.nombre)}">
                <span class="equipo-nombre-mejorado">${escapeHtml(partido.visita.nombre)}</span>
              </div>
              <div class="estado-partido">${escapeHtml(partido.estado || 'SCHEDULED')}</div>
              <div class="preguntas-grid-mejorado">
                ${buildCreatePredictionBlock(id, partido.local.nombre, partido.visita.nombre, partido.local.escudo, partido.visita.escudo, selectedQuestions)}
              </div>
            </div>
          `;
        }).join('');
        openOverlay('create');
      }

      function validateCreatePredictions(){
        const partidos = els.createBody.querySelectorAll('.partido-item-mejorado');
        if (!partidos.length) return false;
        const preguntas = state.configuracionData.preguntasSeleccionadas || [];
        for (const partido of partidos) {
          const partidoId = partido.getAttribute('data-partido-id');
          const respuestas = state.respuestasPartidos[partidoId];
          if (!respuestas) return false;
          for (const pregunta of preguntas) {
            if (pregunta === 'marcador') continue;
            if (respuestas[pregunta] === '' || respuestas[pregunta] === undefined || respuestas[pregunta] === null) return false;
          }
        }
        return true;
      }

      async function sendCreateBet(){
        if (!validateCreatePredictions()) {
          alertMsg('Por favor responde todas las preguntas obligatorias');
          return;
        }
        if (!state.userId) {
          alertMsg('Usuario no identificado');
          return;
        }

        Object.keys(state.respuestasPartidos).forEach(partidoId => {
          const resp = state.respuestasPartidos[partidoId];
          if ((state.configuracionData.preguntasSeleccionadas || []).includes('marcador')) {
            if (!resp.marcador) resp.marcador = { local:0, visitante:0 };
            if (resp.marcador.local === '' || resp.marcador.local === null || resp.marcador.local === undefined) resp.marcador.local = 0;
            if (resp.marcador.visitante === '' || resp.marcador.visitante === null || resp.marcador.visitante === undefined) resp.marcador.visitante = 0;
          } else {
            resp.marcador = { local:99, visitante:99 };
          }
        });

        const grupoRango = 'user_created_challenge_' + Date.now();
        const partidosSeleccionadosArray = Array.from(state.partidosSeleccionados);
        const llave = [state.userId].concat(partidosSeleccionadosArray).join('-');

        const apuestaData = {
          user_id: state.userId,
          grupo_rango: grupoRango,
          fecha_apuesta: new Date().toISOString().slice(0, 19).replace('T', ' '),
          respuestas: state.respuestasPartidos,
          configuracion: state.configuracionData,
          apuesta_minima_usd: Number(state.configuracionData.montoMinimo || 0),
          preguntas_por_encuentro: (state.configuracionData.preguntasSeleccionadas || []).length,
          tipo_reto: state.configuracionData.tipoReto || 'Público',
          tipo_mesa: state.configuracionData.tipoMesa || 'Torneo corto',
          pregunta_cuantos_ganadores: state.configuracionData.ganadores || 'Único Ganador',
          llave: llave,
          nombre_mesa: state.configuracionData.nombreMesa || '',
          modo_forzado: 'Crear_reto'
        };

        if ((state.configuracionData.tipoReto || 'Público') === 'Privado' && state.userAlias) {
          apuestaData.user_alias = String(state.userAlias).replace(/^@+/, '');
        }

        try{
          const json = await ajaxPost('gambt_guardar_apuesta_ppm', { apuesta_data: JSON.stringify(apuestaData) });
          if (json && json.success) {
            alertMsg('Reto creado correctamente');
            closeOverlay('create');
            state.partidosSeleccionados.clear();
            renderElegirPartidos();
            await Promise.all([loadSaldo(), loadPuntos()]);
            if (state.currentTab === 'Mesas activas') loadMesasActivas();
          } else {
            alertMsg('Error al crear el reto: ' + ((json && json.data) || ''));
          }
        }catch(e){
          alertMsg('Error de conexión al enviar reto');
        }
      }

      async function validatePrivatePassword(btn){
        const card = btn.closest('.mesa-card');
        const retoLlave = btn.getAttribute('data-llave');
        const passwordInput = card ? card.querySelector('.privado-password-input') : null;
        const password = passwordInput ? passwordInput.value.trim() : '';
        if (!password) {
          alertMsg('Ingresa la contraseña');
          return;
        }
        try{
          const json = await ajaxPost('gambt_validar_llave_privada', { reto_llave: retoLlave, password });
          if (json && json.success) {
            const container = card.querySelector('.privado-password-container');
            const acceptBtn = card.querySelector('.btn-aceptar-privado');
            if (container) container.style.display = 'none';
            if (acceptBtn) acceptBtn.style.display = 'inline-flex';
          } else {
            alertMsg('Contraseña incorrecta');
          }
        }catch(e){
          alertMsg('Error de conexión');
        }
      }

      async function showPartidosPrivados(retoLlave, nombreMesa){
        state.privadoRetoActual = retoLlave;
        state.privadoRespuestas = {};
        state.activeQuestionsPrivado = [];
        els.privateTitle.textContent = 'Partidos - ' + nombreMesa;
        els.privateBody.innerHTML = '<div class="historial-vacio">Cargando partidos...</div>';
        openOverlay('private');

        try{
          const json = await ajaxPost('gambt_cargar_preguntas_privadas', { reto_llave: retoLlave });
          const data = getSuccessData(json);
          if (!data || !data.partidos || !data.partidos.length) {
            alertMsg('No hay partidos en este reto');
            closeOverlay('private');
            return;
          }
          const partidos = data.partidos;
          const config = data.config || {};
          state.activeQuestionsPrivado = config.activeQuestions || [];

          els.privateBody.innerHTML = partidos.map(p => {
            const partidoId = String(p.partido_id);
            state.privadoRespuestas[partidoId] = {
              id_partido: partidoId,
              estado_partido: 'SCHEDULED',
              ganador: state.activeQuestionsPrivado.includes('ganador') ? '' : 'NO_APLICA',
              ambos_goles: state.activeQuestionsPrivado.includes('ambos_goles') ? '' : 99,
              penales: state.activeQuestionsPrivado.includes('penales') ? '' : 99,
              marcador: state.activeQuestionsPrivado.includes('marcador') ? { local:'', visitante:'' } : { local:99, visitante:99 }
            };
            return `
              <div class="partido-item-mejorado" data-partido-id="${escapeHtml(partidoId)}">
                <div class="partido-header-mejorado">
                  <img src="${escapeHtml(p.local_escudo || '')}" class="escudo-mejorado" alt="${escapeHtml(p.local_nombre)}">
                  <span class="equipo-nombre-mejorado">${escapeHtml(p.local_nombre)}</span>
                  <span class="vs-separator-mejorado">VS</span>
                  <img src="${escapeHtml(p.visita_escudo || '')}" class="escudo-mejorado" alt="${escapeHtml(p.visita_nombre)}">
                  <span class="equipo-nombre-mejorado">${escapeHtml(p.visita_nombre)}</span>
                </div>
                <div class="preguntas-grid-mejorado">
                  ${buildPrivatePredictionBlock(partidoId, p.local_nombre, p.visita_nombre, p.local_escudo, p.visita_escudo, state.activeQuestionsPrivado)}
                </div>
              </div>
            `;
          }).join('');
        }catch(e){
          alertMsg('Error de conexión al cargar partidos');
          closeOverlay('private');
        }
      }

      function validatePrivateResponses(){
        const partidos = els.privateBody.querySelectorAll('.partido-item-mejorado');
        if (!partidos.length) return false;
        for (const partido of partidos) {
          const partidoId = partido.getAttribute('data-partido-id');
          const resp = state.privadoRespuestas[partidoId];
          if (!resp) return false;
          if (state.activeQuestionsPrivado.includes('ganador') && !resp.ganador) return false;
          if (state.activeQuestionsPrivado.includes('ambos_goles') && (resp.ambos_goles === '' || resp.ambos_goles === 99)) return false;
          if (state.activeQuestionsPrivado.includes('penales') && (resp.penales === '' || resp.penales === 99)) return false;
        }
        return true;
      }

      async function sendPrivateBet(){
        if (!validatePrivateResponses()) {
          alertMsg('Por favor responde todas las preguntas obligatorias');
          return;
        }
        if (!state.userId) {
          alertMsg('Usuario no identificado');
          return;
        }
        Object.keys(state.privadoRespuestas).forEach(partidoId => {
          const resp = state.privadoRespuestas[partidoId];
          if (state.activeQuestionsPrivado.includes('marcador')) {
            if (!resp.marcador) resp.marcador = { local:0, visitante:0 };
            if (resp.marcador.local === '' || resp.marcador.local === null) resp.marcador.local = 0;
            if (resp.marcador.visitante === '' || resp.marcador.visitante === null) resp.marcador.visitante = 0;
          } else {
            resp.marcador = { local:99, visitante:99 };
          }
        });

        const apuestaData = {
          reto_llave: state.privadoRetoActual,
          user_id: state.userId,
          respuestas: state.privadoRespuestas
        };

        try{
          const json = await ajaxPost('gambt_guardar_apuesta_privada', { apuesta_data: JSON.stringify(apuestaData) });
          if (json && json.success) {
            alertMsg('Apuesta guardada correctamente');
            closeOverlay('private');
            await Promise.all([loadSaldo(), loadPuntos()]);
            if (state.currentTab === 'Mesas privadas') loadMesasPrivadas();
          } else {
            alertMsg('Error: ' + ((json && json.data) || 'Error desconocido'));
          }
        }catch(e){
          alertMsg('Error de conexión');
        }
      }

      function copyKey(btn){
        const codigo = btn.getAttribute('data-codigo') || '';
        if (!codigo) return;
        navigator.clipboard.writeText(codigo).then(() => {
          alertMsg('Código copiado al portapapeles');
        }).catch(() => {
          alertMsg('Error al copiar');
        });
      }

      function redirectClassic(){
        const currentLang = localStorage.getItem('gambt_lang') || 'es';
        window.location.href = currentLang === 'en'
          ? 'https://www.gambt.online/elementor-1641-en/'
          : 'https://www.gambt.online/elementor-1641/';
      }

      function redirectHome(){
        const currentLang = localStorage.getItem('gambt_lang') || 'es';
        window.location.href = currentLang === 'en'
          ? 'https://www.gambt.online/Inicio%20GAMBT-en/'
          : 'https://www.gambt.online/Inicio%20GAMBT/';
      }

      function redirectUserArea(){
        window.location.href = 'https://www.gambt.online/entorno-usuario/';
      }

      function setupEvents(){
        els.sectionSelect.addEventListener('change', (e) => {
          state.currentSection = e.target.value;
          state.currentTab = (SECTION_TABS[state.currentSection] || [])[0];
          render();
        });

        els.tabs.addEventListener('click', (e) => {
          const btn = e.target.closest('.gm-tab');
          if (!btn) return;
          state.currentTab = btn.getAttribute('data-tab');
          render();
        });

        els.recargar.addEventListener('click', async () => {
          await Promise.all([loadSaldo(), loadPuntos()]);
          if (state.currentTab === 'Mesas activas') loadMesasActivas();
          if (state.currentTab === 'Mesas privadas') loadMesasPrivadas();
          if (state.currentTab === 'Histórico de apuestas') loadHistorial();
        });

        els.classic.addEventListener('click', redirectClassic);
        els.logo.addEventListener('click', redirectHome);
        if (els.userChip) els.userChip.addEventListener('click', redirectUserArea);

        root.addEventListener('click', (e) => {
          const sport = e.target.closest('.gm-sport');
          if (sport) {
            state.configuracionData.deporte = sport.getAttribute('data-sport') || '';
            renderElegirDeporte();
            return;
          }

          const q = e.target.closest('.gm-question');
          if (q) {
            const key = q.getAttribute('data-question');
            const selected = state.configuracionData.preguntasSeleccionadas.slice();
            const idx = selected.indexOf(key);
            if (idx >= 0) selected.splice(idx, 1);
            else {
              if (selected.length >= 4) {
                alertMsg('Máximo 4 preguntas');
                return;
              }
              selected.push(key);
            }
            state.configuracionData.preguntasSeleccionadas = selected;
            renderConfigurarEncuentro();
            return;
          }

          const radio = e.target.closest('.gm-radio');
          if (radio) {
            const group = radio.getAttribute('data-radio-group');
            const value = radio.getAttribute('data-value');
            if (group === 'tipoReto') state.configuracionData.tipoReto = value;
            if (group === 'ganadores') state.configuracionData.ganadores = value;
            if (group === 'tipoMesa') state.configuracionData.tipoMesa = value;
            renderConfigurarEncuentro();
            return;
          }

          const nextDep = e.target.closest('#gm-next-deporte');
          if (nextDep) {
            if (!validateCreateConfig()) return;
            state.currentTab = 'Configurar Encuentro';
            render();
            return;
          }

          const nextCfg = e.target.closest('#gm-next-config');
          if (nextCfg) {
            if (!validateConfigStep()) return;
            state.currentTab = 'Elegir Partidos';
            render();
            return;
          }

          const pick = e.target.closest('.gm-pick-card');
          if (pick) {
            const id = String(pick.getAttribute('data-pick-id'));
            if (state.partidosSeleccionados.has(id)) state.partidosSeleccionados.delete(id);
            else state.partidosSeleccionados.add(id);
            renderElegirPartidos();
            return;
          }

          const openCreate = e.target.closest('#gm-open-create-modal');
          if (openCreate) {
            openCreateModal();
            return;
          }

          const btnUnirse = e.target.closest('.btn-unirse');
          if (btnUnirse) {
            const card = btnUnirse.closest('.mesa-card');
            const grupoRango = btnUnirse.getAttribute('data-grupo-rango') || btnUnirse.getAttribute('data-llave-id') || '';
            const nombreMesa = btnUnirse.getAttribute('data-nombre-mesa') || '';
            const apuestaMinima = btnUnirse.getAttribute('data-apuesta-minima') || '0';
            if (!grupoRango || !nombreMesa) return;
            if (card && card.classList.contains('mesa-card-publica')) showPartidosPublicos(grupoRango, nombreMesa);
            else showPartidosMesa(grupoRango, nombreMesa, apuestaMinima);
            return;
          }

          const opt = e.target.closest('.opcion-mejorada');
          if (opt) {
            handleOptionSelection(opt);
            return;
          }

          const btnCopy = e.target.closest('.btn-copy-code');
          if (btnCopy) {
            copyKey(btnCopy);
            return;
          }

          const btnValidate = e.target.closest('.btn-validar-privado');
          if (btnValidate) {
            validatePrivatePassword(btnValidate);
            return;
          }

          const btnAcceptPrivate = e.target.closest('.btn-aceptar-privado');
          if (btnAcceptPrivate) {
            const llave = btnAcceptPrivate.getAttribute('data-llave');
            const nombreMesa = btnAcceptPrivate.getAttribute('data-nombre-mesa') || 'Reto privado';
            showPartidosPrivados(llave, nombreMesa);
            return;
          }

          const close = e.target.closest('[data-close]');
          if (close) {
            closeOverlay(close.getAttribute('data-close'));
            return;
          }

          if (e.target === els.overlayPublic) closeOverlay('public');
          if (e.target === els.overlayCreate) closeOverlay('create');
          if (e.target === els.overlayPrivate) closeOverlay('private');
        });

        root.addEventListener('input', (e) => {
          if (e.target.id === 'gm-nombre-mesa') {
            state.configuracionData.nombreMesa = e.target.value;
            return;
          }
          if (e.target.id === 'gm-monto-minimo') {
            state.configuracionData.montoMinimo = e.target.value;
            return;
          }
          if (e.target.classList.contains('marcador-input-mejorado')) {
            handleScoreInput(e.target);
            return;
          }
          if (e.target.id === 'gm-search-activas') filterMesasActivas();
          if (e.target.id === 'gm-search-privadas') filterMesasPrivadas();
        });

        els.sendPublic.addEventListener('click', sendPublicBet);
        els.sendCreate.addEventListener('click', sendCreateBet);
        els.sendPrivate.addEventListener('click', sendPrivateBet);

        document.addEventListener('keydown', (e) => {
          if (e.key === 'Escape') {
            closeOverlay('public');
            closeOverlay('create');
            closeOverlay('private');
          }
        });
      }

      async function init(){
        setupEvents();
        await loadUserInfo();
        await Promise.all([loadSaldo(), loadPuntos(), loadMatches()]);
        render();
        paintUserAlias();
      }

      init();
    })();
  </script>
</div>
