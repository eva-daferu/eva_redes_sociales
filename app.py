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
    :root{
      --bg:#f3f3f3;
      --panel:#ffffff;
      --panel2:#f7f7f7;
      --line:#202020;
      --line2:#6d6d6d;
      --text:#111111;
      --muted:#555555;
      --soft:#e7e7e7;
    }

    *{box-sizing:border-box;}

    html,body{
      margin:0;
      padding:0;
      width:100%;
      height:100%;
      overflow:hidden;
      background:var(--bg);
      font-family:Arial,sans-serif;
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

    .topbar{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:8px;
      padding:10px;
      background:var(--panel);
      border-bottom:1px solid var(--line);
    }

    .logo{
      min-width:120px;
      height:42px;
      border:1px solid var(--line);
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:900;
      font-size:24px;
      background:var(--panel2);
    }

    .lang{
      min-width:120px;
      height:36px;
      border:1px solid var(--line);
      background:var(--panel2);
      display:flex;
      align-items:center;
      justify-content:center;
      font-size:14px;
      font-weight:700;
    }

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
      font-size:26px;
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
    }

    .select-wrap{
      background:var(--panel);
      border:1px solid var(--line);
      padding:10px;
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
    }

    .tabs{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:8px;
    }

    .tab{
      min-height:40px;
      border:1px solid var(--line);
      background:var(--panel);
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
      background:var(--soft);
      border-width:2px;
    }

    .panel{
      background:var(--panel);
      border:1px solid var(--line);
      padding:10px;
    }

    .panel-inner{
      border:1px solid var(--line2);
      padding:10px;
      background:#fff;
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
    }

    .mesa-list{
      display:grid;
      grid-template-columns:1fr;
      gap:10px;
    }

    .mesa-card{
      border:1px solid var(--line);
      background:var(--panel2);
      padding:12px;
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
    }

    .empty{
      min-height:280px;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      color:var(--muted);
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
      border:1px solid var(--line);
      padding:12px;
      background:#fff;
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
    }

    .toggle{
      width:42px;
      height:24px;
      border:1px solid var(--line);
      background:#fff;
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
      background:#bbb;
      border:1px solid var(--line);
    }

    .radio-line{
      display:flex;
      flex-wrap:wrap;
      gap:12px;
      color:#111;
      font-weight:700;
      font-size:13px;
    }

    .team-grid{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:10px;
      margin-bottom:10px;
    }

    .team-card{
      border:1px solid var(--line);
      min-height:108px;
      padding:10px;
      display:flex;
      flex-direction:column;
      align-items:center;
      justify-content:center;
      background:var(--panel2);
      font-weight:900;
      text-align:center;
    }

    .team-logo{
      width:52px;
      height:52px;
      border:1px solid var(--line2);
      margin-bottom:10px;
      background:#fff;
    }

    /* CAMBIO TÁCTICO: cards en Elegir Partidos */
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
    }

    .history-table{
      border:1px solid var(--line2);
      overflow:hidden;
    }

    .history-head,
    .history-empty{
      display:grid;
      grid-template-columns:1.1fr 1.1fr 1.2fr .9fr .8fr;
    }

    .history-head div{
      background:var(--soft);
      padding:10px;
      border-right:1px solid var(--line2);
      font-weight:900;
    }

    .history-head div:last-child,
    .history-empty div:last-child{
      border-right:none;
    }

    .history-empty div{
      padding:12px;
      border-top:1px solid var(--line2);
      border-right:1px solid var(--line2);
      min-height:46px;
      display:flex;
      align-items:center;
      justify-content:center;
      color:var(--muted);
      font-style:italic;
      background:#fff;
    }

    @media (max-width:360px){
      .cards{
        grid-template-columns:1fr;
      }

      .card.full{
        grid-column:auto;
      }

      .tabs{
        grid-template-columns:1fr;
      }

      .title-row{
        flex-direction:column;
        align-items:stretch;
      }

      .team-grid{
        grid-template-columns:1fr;
      }
    }
  </style>
</head>
<body>
  <div id="stage">
    <div id="phone">
      <div id="screen">
        <div class="topbar">
          <div class="logo">GAMBT</div>
          <div class="lang">Español ▾</div>
        </div>

        <div class="content-wrap">
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
  </div>

  <script>
    const SECTION_TABS = __SECTION_TABS__;
    const sectionOrder = ["UNIRSE MESA", "CREAR MESA", "MESA JUGADOR", "MESA PRIVADA"];

    let currentSection = "UNIRSE MESA";
    let currentTab = SECTION_TABS[currentSection][0];
    const selectedMatches = new Set();

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
              <div class="search">Buscar mesas...</div>
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
            <div class="title-lg" style="margin-bottom:10px;">Histórico de encuentros</div>
            <div class="empty">No hay encuentros históricos disponibles</div>
          </div>
        </div>
      `;
    }

    function renderHistApuestas() {
      contentEl.innerHTML = `
        <div class="panel">
          <div class="panel-inner">
            <div class="title-lg" style="margin-bottom:10px;">Histórico de apuestas</div>

            <div class="history-table">
              <div class="history-head">
                <div>Partido</div>
                <div>Predicción</div>
                <div>Resultado real</div>
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
            <div class="title-lg" style="margin-bottom:10px;">Sports</div>

            <div class="field">
              <div class="field-title">Nombre mesa (máximo 30 caracteres)</div>
              <div class="input">Ej: Torneo de expertos</div>
            </div>

            <div style="height:10px;"></div>

            <div class="option-col">
              <div class="option"><span>Fútbol</span><span class="toggle"></span></div>
              <div class="option"><span>Baloncesto</span><span class="toggle"></span></div>
              <div class="option"><span>Tenis</span><span class="toggle"></span></div>
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
                  <div class="option"><span>☑ Definir ganador</span><span></span></div>
                  <div class="option"><span>☐ ¿Gol de ambos equipos?</span><span></span></div>
                  <div class="option"><span>☐ ¿Penales?</span><span></span></div>
                  <div class="option"><span>☐ Predice el marcador</span><span></span></div>
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

    function buildPickCard(id, title, schedule) {
      const selectedClass = selectedMatches.has(id) ? "selected" : "";
      return `
        <div class="pick-card ${selectedClass}" data-pick-id="${id}">
          <div class="pick-check"></div>
          <div>
            <div class="pick-title">${title}</div>
            <div class="pick-meta">
              Horario: ${schedule}<br>
              Estado: Disponible
            </div>
            <div class="pick-tag">Agregar al reto</div>
          </div>
        </div>
      `;
    }

    function bindPickCards() {
      contentEl.querySelectorAll(".pick-card").forEach(card => {
        card.addEventListener("click", () => {
          const id = card.dataset.pickId;
          if (selectedMatches.has(id)) {
            selectedMatches.delete(id);
          } else {
            selectedMatches.add(id);
          }
          renderElegirPartidos();
        });
      });
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

            <div class="title-lg" style="margin-bottom:10px;">Partidos disponibles</div>

            <div class="pick-cards">
              ${buildPickCard("p1", "Gil Vicente vs Casa Pia", "26 abr 2026, 00:00")}
              ${buildPickCard("p2", "Tondela vs CD Nacional", "26 abr 2026, 00:00")}
              ${buildPickCard("p3", "Santa Clara vs Braga", "26 abr 2026, 00:00")}
              ${buildPickCard("p4", "AVS vs Sporting CP", "26 abr 2026, 00:00")}
              ${buildPickCard("p5", "Estoril Praia vs Famalicão", "26 abr 2026, 00:00")}
            </div>

            <div class="next-wrap">
              <div class="next-btn">ENVIAR</div>
            </div>
          </div>
        </div>
      `;
      bindPickCards();
    }

    function renderContent() {
      if (currentTab === "Mesas activas") {
        renderMesas("Mesas activas disponibles");
        return;
      }

      if (currentTab === "Mesas privadas") {
        renderMesas("Mesas privadas disponibles");
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
