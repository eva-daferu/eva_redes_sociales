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
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>
    :root {
      --bg:#071423;
      --panel:#071d2c;
      --panel2:#082235;
      --line:#1ee7ff;
      --line2:#ffe84c;
      --text:#eaf7ff;
      --muted:#b7d2df;
      --btn:#20dfff;
    }

    *{box-sizing:border-box;}
    html,body{
      margin:0;
      padding:0;
      background:#dfe3e8;
      font-family:Arial,sans-serif;
      overflow:hidden;
    }

    #stage{
      position:fixed;
      inset:0;
      display:flex;
      align-items:center;
      justify-content:center;
      padding:8px;
    }

    #phone{
      width:min(390px,96vw);
      height:min(844px,96vh);
      border:3px solid #111;
      border-radius:28px;
      overflow:auto;
      background:
        radial-gradient(circle at 20% 15%, rgba(255,255,255,.22), transparent 18%),
        radial-gradient(circle at 85% 18%, rgba(255,255,255,.20), transparent 16%),
        linear-gradient(180deg, #0c1728 0%, #13233a 40%, #101c2f 100%);
      box-shadow:0 10px 35px rgba(0,0,0,.22);
    }

    #screen{
      min-height:100%;
      padding:12px 12px 22px;
      color:var(--text);
    }

    .topbar{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:8px;
      margin-bottom:12px;
    }

    .logo{
      height:44px;
      border:2px solid var(--line);
      border-radius:16px;
      display:flex;
      align-items:center;
      justify-content:center;
      padding:0 14px;
      font-weight:900;
      font-size:22px;
      letter-spacing:1px;
      background:rgba(0,0,0,.28);
      box-shadow:0 0 16px rgba(30,231,255,.18);
    }

    .lang{
      min-width:110px;
      height:36px;
      border:1.6px solid var(--line);
      border-radius:18px;
      background:rgba(0,0,0,.28);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:700;
      font-size:14px;
    }

    .cards{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:10px;
      margin-bottom:10px;
    }

    .card{
      background:rgba(0,0,0,.36);
      border:1.6px solid var(--line);
      border-radius:18px;
      padding:12px;
      min-height:92px;
      box-shadow:0 0 18px rgba(30,231,255,.14);
    }

    .card.full{
      grid-column:1/-1;
      min-height:84px;
    }

    .card-title{
      font-size:12px;
      font-weight:700;
      color:#d6effa;
      margin-bottom:8px;
      text-transform:uppercase;
    }

    .card-value{
      font-size:26px;
      font-weight:900;
      line-height:1;
      margin-bottom:8px;
    }

    .mini{
      font-size:12px;
      line-height:1.2;
      color:var(--muted);
    }

    .action-btn{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      height:34px;
      padding:0 18px;
      border-radius:12px;
      background:var(--btn);
      color:#05131f;
      font-weight:900;
      font-size:14px;
    }

    .select-wrap{
      background:rgba(0,0,0,.36);
      border:1.6px solid var(--line);
      border-radius:18px;
      padding:10px 12px;
      margin-bottom:10px;
    }

    .select-label{
      font-size:12px;
      font-weight:700;
      color:#d6effa;
      margin-bottom:6px;
      text-transform:uppercase;
    }

    select{
      width:100%;
      height:40px;
      border-radius:12px;
      border:1.4px solid var(--line);
      background:#071b2c;
      color:var(--text);
      padding:0 12px;
      font-size:14px;
      font-weight:700;
      outline:none;
    }

    .tabs{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:8px;
      margin-bottom:10px;
    }

    .tab{
      min-height:40px;
      border:1.4px solid var(--line);
      border-radius:12px;
      background:rgba(8,34,53,.82);
      color:var(--text);
      font-weight:700;
      font-size:13px;
      padding:8px 10px;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      cursor:pointer;
    }

    .tab.active{
      border-color:var(--line2);
      box-shadow:inset 0 0 0 1px rgba(255,232,76,.25);
    }

    .panel{
      background:rgba(0,0,0,.34);
      border:1.8px solid var(--line);
      border-radius:18px;
      padding:12px;
      box-shadow:0 0 18px rgba(30,231,255,.12);
    }

    .panel-inner{
      border:1.4px solid var(--line2);
      border-radius:16px;
      padding:12px;
      background:rgba(0,0,0,.22);
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
      color:#ffe84c;
      text-transform:uppercase;
    }

    .search{
      height:38px;
      border:1.4px solid var(--line);
      border-radius:19px;
      padding:0 12px;
      background:#071b2c;
      color:#dfefff;
      display:flex;
      align-items:center;
      font-size:13px;
      min-width:140px;
    }

    .mesa-list{
      display:grid;
      grid-template-columns:1fr;
      gap:10px;
    }

    .mesa-card{
      border:1.4px solid var(--line2);
      border-radius:14px;
      background:rgba(0,0,0,.28);
      padding:12px;
    }

    .mesa-name{
      font-size:14px;
      font-weight:900;
      color:#ffe84c;
      margin-bottom:8px;
    }

    .mesa-meta{
      font-size:13px;
      line-height:1.35;
      color:#dceaf3;
      margin-bottom:10px;
    }

    .mesa-btn{
      height:34px;
      border-radius:10px;
      background:var(--btn);
      display:flex;
      align-items:center;
      justify-content:center;
      color:#05131f;
      font-weight:900;
    }

    .empty{
      min-height:280px;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      color:#ffe84c;
      font-size:14px;
      font-weight:700;
      line-height:1.35;
    }

    .form-stack{
      display:grid;
      grid-template-columns:1fr;
      gap:10px;
    }

    .field{
      border:1.4px solid var(--line);
      border-radius:14px;
      padding:12px;
      background:rgba(0,0,0,.20);
    }

    .field-title{
      font-size:13px;
      font-weight:900;
      color:#ffe84c;
      margin-bottom:10px;
    }

    .input{
      height:42px;
      border-radius:10px;
      border:1px solid #a9bfcb;
      background:#e8ecef;
      color:#444;
      display:flex;
      align-items:center;
      padding:0 12px;
      font-weight:700;
    }

    .option-col{
      display:grid;
      grid-template-columns:1fr;
      gap:8px;
    }

    .option{
      min-height:44px;
      border:1.2px solid var(--line);
      border-radius:12px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      padding:10px 12px;
      font-weight:700;
      background:rgba(0,0,0,.16);
      gap:10px;
    }

    .toggle{
      width:42px;
      height:24px;
      border-radius:12px;
      border:1.2px solid var(--line);
      background:#082235;
      position:relative;
      flex:0 0 auto;
    }

    .toggle::after{
      content:"";
      position:absolute;
      top:2px;
      left:20px;
      width:18px;
      height:18px;
      border-radius:50%;
      background:var(--btn);
    }

    .radio-line{
      display:flex;
      flex-wrap:wrap;
      gap:12px;
      color:#e8f4fb;
      font-weight:700;
      font-size:13px;
    }

    .table-wrap{
      border:1.4px solid var(--line2);
      border-radius:14px;
      overflow:hidden;
      background:rgba(0,0,0,.18);
    }

    .thead,.trow{
      display:grid;
      grid-template-columns:72px 1fr 110px;
    }

    .thead div{
      background:rgba(255,232,76,.18);
      color:#ffe84c;
      font-weight:900;
      padding:10px;
      border-right:1px solid rgba(255,255,255,.25);
    }

    .thead div:last-child,
    .trow div:last-child{
      border-right:none;
    }

    .trow div{
      padding:10px;
      border-top:1px solid rgba(255,255,255,.12);
      border-right:1px solid rgba(255,255,255,.16);
      min-height:42px;
      display:flex;
      align-items:center;
      color:#e8f4fb;
    }

    .check{
      width:22px;
      height:22px;
      border:2px solid var(--line);
      border-radius:6px;
    }

    .team-grid{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:10px;
      margin-bottom:10px;
    }

    .team-card{
      border:1.4px solid var(--line2);
      border-radius:14px;
      min-height:108px;
      padding:10px;
      display:flex;
      flex-direction:column;
      align-items:center;
      justify-content:center;
      background:rgba(0,0,0,.18);
      color:#ffe84c;
      font-weight:900;
      text-align:center;
    }

    .team-logo{
      width:52px;
      height:52px;
      border:1.2px solid var(--line);
      border-radius:12px;
      margin-bottom:10px;
      background:rgba(255,255,255,.05);
    }

    .next-wrap{
      margin-top:12px;
      display:flex;
      justify-content:center;
    }

    .next-btn{
      height:42px;
      min-width:160px;
      padding:0 24px;
      border-radius:12px;
      background:rgba(255,232,76,.45);
      display:flex;
      align-items:center;
      justify-content:center;
      color:#fff2a0;
      font-weight:900;
      font-size:16px;
    }

    .history-table{
      border:1.4px solid var(--line2);
      border-radius:14px;
      overflow:hidden;
    }

    .history-head,
    .history-empty{
      display:grid;
      grid-template-columns:1.1fr 1.1fr 1.2fr .9fr .8fr;
    }

    .history-head div{
      background:rgba(255,232,76,.18);
      padding:10px;
      border-right:1px solid rgba(255,255,255,.25);
      color:#ffe84c;
      font-weight:900;
    }

    .history-head div:last-child,
    .history-empty div:last-child{
      border-right:none;
    }

    .history-empty div{
      padding:12px;
      border-top:1px solid rgba(255,255,255,.12);
      border-right:1px solid rgba(255,255,255,.16);
      min-height:46px;
      display:flex;
      align-items:center;
      justify-content:center;
      color:#ffe84c;
      font-style:italic;
    }
  </style>
</head>
<body>
  <div id="stage">
    <div id="phone">
      <div id="screen">
        <div class="topbar">
          <div class="logo">GAMBT</div>
          <div class="lang">🇪🇸 Español ▾</div>
        </div>

        <div class="cards">
          <div class="card">
            <div class="card-title">Saldo virtual</div>
            <div class="card-value">$0.00</div>
            <div class="action-btn">RECARGAR +</div>
          </div>

          <div class="card">
            <div class="card-title">Puntos ganados</div>
            <div class="card-value">40 pts</div>
          </div>

          <div class="card full">
            <div class="card-title">Modo classic</div>
            <div class="mini">Cuotas en vivo, tickets tradicionales.</div>
            <div style="margin-top:10px;" class="action-btn">Entrar</div>
          </div>
        </div>

        <div class="select-wrap">
          <div class="select-label">Sección</div>
          <select id="sectionSelect"></select>
        </div>

        <div id="tabs" class="tabs"></div>

        <div id="content"></div>
      </div>
    </div>
  </div>

  <script>
    const SECTION_TABS = __SECTION_TABS__;
    const sectionOrder = ["UNIRSE MESA", "CREAR MESA", "MESA JUGADOR", "MESA PRIVADA"];

    let currentSection = "UNIRSE MESA";
    let currentTab = SECTION_TABS[currentSection][0];

    const sectionSelect = document.getElementById("sectionSelect");
    const tabsEl = document.getElementById("tabs");
    const contentEl = document.getElementById("content");

    function fillSelect() {
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

    function mesacard(title, amount) {
      return `
        <div class="mesa-card">
          <div class="mesa-name">${title}</div>
          <div class="mesa-meta">
            Deporte: Reto<br>
            Partidos: 2<br>
            Apuesta mínima: ${amount}
          </div>
          <div class="mesa-btn">Unirse</div>
        </div>
      `;
    }

    function renderMesas(titleText) {
      contentEl.innerHTML = `
        <div class="panel">
          <div class="panel-inner">
            <div class="title-row">
              <div class="title-lg">${titleText}</div>
              <div class="search">🔎&nbsp;&nbsp;Buscar mesas...</div>
            </div>

            <div class="mesa-list">
              ${mesacard("Forzce - Gym", "$11.00")}
              ${mesacard("Creo mesa publica - Diana", "$2.00")}
              ${mesacard("New - Diana", "$10.00")}
              ${mesacard("ddd - Blanco", "$6.00")}
            </div>
          </div>
        </div>
      `;
    }

    function renderHistEncuentros() {
      contentEl.innerHTML = `
        <div class="panel">
          <div class="panel-inner">
            <div class="title-lg" style="margin-bottom:10px;">HISTÓRICO DE ENCUENTROS</div>
            <div class="empty">No hay encuentros históricos disponibles</div>
          </div>
        </div>
      `;
    }

    function renderHistApuestas() {
      contentEl.innerHTML = `
        <div class="panel">
          <div class="panel-inner">
            <div class="title-lg" style="margin-bottom:10px;">HISTÓRICO DE APUESTAS</div>

            <div class="history-table">
              <div class="history-head">
                <div>Partido</div>
                <div>Predicción</div>
                <div>Resultado Real</div>
                <div>Estado</div>
                <div>Fecha</div>
              </div>

              <div class="history-empty">
                <div></div>
                <div></div>
                <div>No hay apuestas en tu historial</div>
                <div></div>
                <div></div>
              </div>
            </div>

            <div style="height:180px;"></div>
          </div>
        </div>
      `;
    }

    function renderElegirDeporte() {
      contentEl.innerHTML = `
        <div class="panel">
          <div class="panel-inner">
            <div class="title-lg" style="margin-bottom:10px;">SPORTS</div>

            <div class="field">
              <div class="field-title">Nombre Mesa (máximo 30 caracteres)</div>
              <div class="input">Ej: Torneo de expertos</div>
            </div>

            <div style="height:10px;"></div>

            <div class="option-col">
              <div class="option"><span>⚽ Fútbol</span><span class="toggle"></span></div>
              <div class="option"><span>🏀 Baloncesto</span><span class="toggle"></span></div>
              <div class="option"><span>🎾 Tenis</span><span class="toggle"></span></div>
            </div>

            <div class="next-wrap">
              <div class="next-btn">SIGUIENTE</div>
            </div>
          </div>
        </div>
      `;
    }

    function renderConfigurarEncuentro() {
      contentEl.innerHTML = `
        <div class="panel">
          <div class="panel-inner">
            <div class="form-stack">
              <div class="field">
                <div class="field-title">Apuesta mínima (USD)</div>
                <div class="input">Ej: 17</div>
              </div>

              <div class="field">
                <div class="field-title">¿Tipo de reto?</div>
                <div class="radio-line">
                  <span>◉ Público</span>
                  <span>○ Privado</span>
                </div>
              </div>

              <div class="field">
                <div class="field-title">¿Preguntas por encuentro? (Selecciona 1-4)</div>
                <div class="option-col">
                  <div class="option"><span>☑ DEFINIR GANADOR</span><span></span></div>
                  <div class="option"><span>☐ ¿GOL DE AMBOS EQUIPOS?</span><span></span></div>
                  <div class="option"><span>☐ ¿PENALES?</span><span></span></div>
                  <div class="option"><span>☐ PREDICE EL MARCADOR</span><span></span></div>
                </div>
              </div>

              <div class="field">
                <div class="field-title">¿Pregunta cuántos ganadores?</div>
                <div class="radio-line">
                  <span>◉ Único ganador</span>
                  <span>○ Varios ganadores</span>
                </div>
              </div>

              <div class="field">
                <div class="field-title">¿Tipo de mesa?</div>
                <div class="radio-line">
                  <span>◉ Selección</span>
                  <span>○ Torneo corto</span>
                  <span>○ Torneo largo</span>
                </div>
              </div>
            </div>

            <div class="next-wrap">
              <div class="next-btn">SIGUIENTE</div>
            </div>
          </div>
        </div>
      `;
    }

    function renderElegirPartidos() {
      contentEl.innerHTML = `
        <div class="panel">
          <div class="panel-inner">
            <div class="team-grid">
              <div class="team-card">
                <div class="team-logo"></div>
                Gil Vicente
              </div>

              <div class="team-card">
                <div class="team-logo"></div>
                Casa Pia
              </div>
            </div>

            <div class="title-lg" style="margin-bottom:10px;">TABLA DE PARTIDOS</div>

            <div class="table-wrap">
              <div class="thead">
                <div>Seleccionar</div>
                <div>Reto</div>
                <div>Horario</div>
              </div>

              <div class="trow">
                <div><div class="check"></div></div>
                <div>Gil Vicente vs Casa Pia</div>
                <div>26 abr 2026, 00:00</div>
              </div>

              <div class="trow">
                <div><div class="check"></div></div>
                <div>Tondela vs CD Nacional</div>
                <div>26 abr 2026, 00:00</div>
              </div>

              <div class="trow">
                <div><div class="check"></div></div>
                <div>Santa Clara vs Braga</div>
                <div>26 abr 2026, 00:00</div>
              </div>

              <div class="trow">
                <div><div class="check"></div></div>
                <div>AVS vs Sporting CP</div>
                <div>26 abr 2026, 00:00</div>
              </div>
            </div>

            <div class="next-wrap">
              <div class="next-btn">ENVIAR</div>
            </div>
          </div>
        </div>
      `;
    }

    function renderContent() {
      if (currentTab === "Mesas activas") {
        renderMesas("MESAS ACTIVAS DISPONIBLES");
        return;
      }

      if (currentTab === "Mesas privadas") {
        renderMesas("MESAS PRIVADAS DISPONIBLES");
        return;
      }

      if (currentTab === "Histórico de encuentros") {
        renderHistEncuentros();
        return;
      }

      if (currentTab === "Histórico de apuestas") {
        renderHistApuestas();
        return;
      }

      if (currentTab === "Elegir Deporte") {
        renderElegirDeporte();
        return;
      }

      if (currentTab === "Configurar Encuentro") {
        renderConfigurarEncuentro();
        return;
      }

      if (currentTab === "Elegir Partidos") {
        renderElegirPartidos();
        return;
      }
    }

    function render() {
      renderTabs();
      renderContent();
      sectionSelect.value = currentSection;
    }

    fillSelect();
    render();
  </script>
</body>
</html>
"""

html = html.replace("__SECTION_TABS__", json.dumps(SECTION_TABS, ensure_ascii=False))
components.html(html, height=930, scrolling=False)
