<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GAMBT · Parley</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* ===== RESET Y VARIABLES (BASE PLANO1 + NEÓN PARLEY) ===== */
        :root {
            --bg: #0b0f14;
            --panel: rgba(0, 15, 25, 0.78);
            --panel-solid: #0a1a24;
            --line: #00eaff;
            --line2: #ffe855;
            --text: #d6f7ff;
            --muted: #9bb8c7;
            --soft: #1e2f3c;
            --neon-cyan: #00eaff;
            --neon-yellow: #ffe855;
            --neon-pink: #ff66cc;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html, body {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: var(--bg) url('https://files.catbox.moe/5ova8s.jpg') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Orbitron', 'Segoe UI', Arial, sans-serif;
            color: var(--text);
        }

        #stage {
            position: fixed;
            inset: 0;
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            background: transparent;
        }

        #phone {
            width: 100%;
            height: 100%;
            overflow-y: auto;
            overflow-x: hidden;
            -webkit-overflow-scrolling: touch;
        }

        #screen {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding: 0 0 20px 0;
        }

        /* ===== TOPBAR NEÓN (ESTILO PARLEY_ACTUAL) ===== */
        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            padding: 8px 12px;
            background: linear-gradient(90deg, rgba(0,10,20,0.95) 0%, rgba(10,20,30,0.92) 100%);
            border-bottom: 2px solid transparent;
            box-shadow: 0 5px 25px rgba(0,234,255,0.3);
            backdrop-filter: blur(10px);
            border-image: linear-gradient(45deg, #00eaff, #ffe855, #ff66cc, #00eaff) 1;
            animation: borderNeon 3s linear infinite;
            color: white;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        @keyframes borderNeon {
            0% { border-image-source: linear-gradient(45deg, #00eaff, #ffe855, #ff66cc, #00eaff); }
            25% { border-image-source: linear-gradient(45deg, #ffe855, #ff66cc, #00eaff, #ffe855); }
            50% { border-image-source: linear-gradient(45deg, #ff66cc, #00eaff, #ffe855, #ff66cc); }
            75% { border-image-source: linear-gradient(45deg, #00eaff, #ffe855, #ff66cc, #00eaff); }
            100% { border-image-source: linear-gradient(45deg, #ffe855, #ff66cc, #00eaff, #ffe855); }
        }

        .logo {
            display: flex;
            align-items: center;
            text-decoration: none;
        }

        .logo span {
            font-size: 28px;
            font-weight: 900;
            background: linear-gradient(45deg, #00eaff, #ffe855, #ff66cc, #00eaff);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 2px 15px rgba(0,234,255,0.3);
        }

        .lang-selector {
            display: flex;
            align-items: center;
            padding: 6px 14px;
            border-radius: 999px;
            border: 1px solid #0ce3ff55;
            background: linear-gradient(180deg, #041a27, #041321);
            box-shadow: 0 6px 20px #00e7ff22;
            color: #c8f6ff;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            gap: 6px;
        }

        .user-menu {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 999px;
            border: 1px solid #0ce3ff55;
            background: linear-gradient(180deg, #041a27, #041321);
            box-shadow: 0 6px 20px #00e7ff22;
            color: #c8f6ff;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
        }

        /* ===== TARJETAS PRINCIPALES ===== */
        .cards-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            padding: 10px 12px;
        }

        .card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 14px 12px;
            box-shadow: 0 0 20px #00eaff55, inset 0 0 10px #00eaff22;
            backdrop-filter: blur(4px);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .card.full-width {
            grid-column: 1 / -1;
        }

        .card-label {
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            opacity: 0.9;
            letter-spacing: 0.5px;
        }

        .card-value {
            font-size: 28px;
            font-weight: 900;
            line-height: 1.2;
            color: white;
            text-shadow: 0 0 8px var(--neon-cyan);
        }

        .card-info {
            font-size: 12px;
            color: var(--muted);
            margin: 4px 0;
        }

        .btn-action {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: var(--neon-cyan);
            color: #00151f;
            border: none;
            border-radius: 30px;
            padding: 8px 16px;
            font-weight: 800;
            font-size: 13px;
            cursor: pointer;
            box-shadow: 0 0 15px #00eaff;
            transition: 0.2s;
            width: fit-content;
            margin-top: 8px;
        }

        .btn-action:hover {
            background: var(--neon-yellow);
            box-shadow: 0 0 20px #ffe855;
            transform: scale(1.02);
        }

        /* ===== SELECTOR DE SECCIÓN ===== */
        .section-wrap {
            padding: 0 12px;
        }

        .select-custom {
            width: 100%;
            padding: 12px 16px;
            border-radius: 40px;
            border: 2px solid var(--line);
            background: var(--panel);
            color: white;
            font-weight: 700;
            font-size: 16px;
            outline: none;
            backdrop-filter: blur(4px);
            box-shadow: 0 0 15px #00eaff66;
        }

        /* ===== TABS DINÁMICOS ===== */
        .tabs-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 8px 12px;
        }

        .tab-btn {
            flex: 1 0 calc(33% - 8px);
            min-width: 100px;
            padding: 12px 4px;
            border-radius: 40px;
            border: 2px solid #00eaff77;
            background: rgba(0,15,25,0.6);
            color: white;
            font-weight: 700;
            font-size: 13px;
            text-align: center;
            cursor: pointer;
            backdrop-filter: blur(4px);
            box-shadow: inset 0 0 10px #00eaff55;
            transition: 0.2s;
        }

        .tab-btn.active {
            border-color: var(--neon-yellow);
            box-shadow: 0 0 20px #ffe855aa, inset 0 0 12px #ffe855;
            background: rgba(255,232,133,0.15);
        }

        /* ===== CONTENEDOR PRINCIPAL ===== */
        #content {
            padding: 0 12px 20px;
        }

        /* ===== PANELES Y TARJETAS DE MESA ===== */
        .panel {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 16px;
            backdrop-filter: blur(5px);
            box-shadow: 0 0 25px #00eaff55;
        }

        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }

        .panel-title {
            font-size: 20px;
            font-weight: 900;
            color: var(--neon-yellow);
            text-shadow: 0 0 10px #ffe855;
        }

        .search-box {
            display: flex;
            align-items: center;
            background: rgba(0,0,0,0.3);
            border: 1px solid var(--line);
            border-radius: 30px;
            padding: 6px 12px;
        }

        .search-box i {
            color: var(--neon-cyan);
            margin-right: 8px;
        }

        .search-box input {
            background: transparent;
            border: none;
            color: white;
            outline: none;
            font-size: 14px;
            width: 160px;
        }

        .mesa-grid {
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-height: 450px;
            overflow-y: auto;
            padding-right: 4px;
        }

        .mesa-card {
            background: rgba(0,20,35,0.85);
            border: 1.5px solid var(--line);
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 0 18px #00eaff55;
            backdrop-filter: blur(4px);
            transition: 0.2s;
            cursor: pointer;
        }

        .mesa-card.publica {
            border-color: var(--neon-yellow);
            box-shadow: 0 0 20px #ffe85588;
        }

        .mesa-card.privada {
            border-color: var(--neon-pink);
            box-shadow: 0 0 20px #ff66cc88;
        }

        .mesa-title {
            font-size: 18px;
            font-weight: 900;
            color: white;
            margin-bottom: 8px;
        }

        .mesa-info {
            font-size: 14px;
            color: #b0e0ff;
            margin: 4px 0;
        }

        .btn-unirse {
            background: var(--neon-cyan);
            border: none;
            border-radius: 30px;
            padding: 10px 0;
            font-weight: 800;
            color: #00151f;
            margin-top: 12px;
            cursor: pointer;
            text-align: center;
            box-shadow: 0 0 12px #00eaff;
            transition: 0.2s;
        }

        .btn-unirse:hover {
            background: var(--neon-yellow);
            box-shadow: 0 0 20px #ffe855;
        }

        /* ===== FORMULARIOS (CREAR MESA) ===== */
        .form-group {
            margin-bottom: 20px;
        }

        .form-label {
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--neon-yellow);
        }

        .input-field {
            width: 100%;
            padding: 14px 16px;
            border-radius: 30px;
            border: 2px solid var(--line);
            background: rgba(0,0,0,0.4);
            color: white;
            font-weight: 600;
            outline: none;
        }

        .radio-group {
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
        }

        .radio-group label {
            display: flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
        }

        .checkbox-group {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .btn-next {
            background: linear-gradient(135deg, #00eaff, #00c8ff);
            border: none;
            border-radius: 40px;
            padding: 16px 30px;
            font-weight: 900;
            font-size: 18px;
            color: #00151f;
            width: 100%;
            cursor: pointer;
            box-shadow: 0 0 25px #00eaff;
            transition: 0.2s;
        }

        .btn-next:disabled {
            opacity: 0.4;
            box-shadow: none;
            cursor: not-allowed;
        }

        /* ===== MODAL PREDICCIONES ===== */
        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.85);
            backdrop-filter: blur(8px);
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 16px;
        }

        .modal-container {
            background: linear-gradient(145deg, #0a1f2c 0%, #05141e 100%);
            border: 2px solid var(--neon-yellow);
            border-radius: 24px;
            width: 100%;
            max-width: 550px;
            max-height: 85vh;
            overflow-y: auto;
            padding: 24px 20px;
            box-shadow: 0 0 60px #ffe85566;
            position: relative;
        }

        .modal-close {
            position: absolute;
            top: 12px;
            right: 16px;
            font-size: 28px;
            color: var(--neon-yellow);
            cursor: pointer;
            background: none;
            border: none;
        }

        .modal-title {
            font-size: 22px;
            font-weight: 900;
            color: var(--neon-yellow);
            text-align: center;
            margin-bottom: 6px;
        }

        .modal-subtitle {
            text-align: center;
            color: var(--neon-cyan);
            margin-bottom: 20px;
            font-size: 14px;
        }

        .prediction-item {
            background: rgba(0,30,45,0.7);
            border: 1px solid #00eaff55;
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 16px;
        }

        .prediction-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            font-weight: 800;
            margin-bottom: 16px;
        }

        .prediction-options {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
        }

        .prediction-option {
            background: rgba(0,234,255,0.15);
            border: 1.5px solid var(--neon-cyan);
            border-radius: 40px;
            padding: 10px 16px;
            font-weight: 700;
            cursor: pointer;
            transition: 0.2s;
            flex: 1 0 100px;
            text-align: center;
        }

        .prediction-option.selected {
            background: var(--neon-cyan);
            color: #00151f;
            border-color: var(--neon-yellow);
            box-shadow: 0 0 15px #00eaff;
        }

        .modal-actions {
            display: flex;
            gap: 12px;
            margin-top: 24px;
        }

        .btn-primary {
            background: linear-gradient(135deg, #00eaff, #00c8ff);
            border: none;
            border-radius: 40px;
            padding: 14px;
            font-weight: 900;
            color: #00151f;
            flex: 2;
            cursor: pointer;
            box-shadow: 0 0 20px #00eaff;
        }

        .btn-secondary {
            background: transparent;
            border: 2px solid var(--neon-yellow);
            border-radius: 40px;
            padding: 14px;
            font-weight: 900;
            color: var(--neon-yellow);
            flex: 1;
            cursor: pointer;
        }

        /* Utilidades */
        .hidden {
            display: none !important;
        }

        .empty-message {
            text-align: center;
            padding: 30px;
            color: var(--muted);
            font-style: italic;
        }
    </style>
</head>
<body>
<div id="stage">
    <div id="phone">
        <div id="screen">
            <!-- TOPBAR -->
            <div class="topbar">
                <a href="#" class="logo" id="logo-link"><span>GAMBT</span></a>
                <div class="lang-selector" id="lang-toggle">🇪🇸 Español</div>
                <div class="user-menu" id="user-menu-btn"><i class="fas fa-user-circle"></i> <span id="user-name-top">@Invitado</span></div>
            </div>

            <!-- TARJETAS SALDO / PUNTOS / CLASSIC -->
            <div class="cards-grid">
                <div class="card">
                    <div class="card-label">SALDO VIRTUAL</div>
                    <div class="card-value" id="saldo-usuario">$0.00</div>
                    <div class="btn-action" id="btn-recargar">RECARGAR +</div>
                </div>
                <div class="card">
                    <div class="card-label">PUNTOS GANADOS</div>
                    <div class="card-value" id="user-puntos">0 pts</div>
                    <div class="card-info" id="user-nivel">Nivel 0</div>
                    <div class="card-info" id="user-posicion">Ranking: #0</div>
                </div>
                <div class="card full-width">
                    <div class="card-label">MODO CLASSIC</div>
                    <div class="card-info">Cuotas en vivo, tickets tradicionales.</div>
                    <div class="btn-action" id="btn-entrar-classic">Entrar</div>
                </div>
            </div>

            <!-- SELECTOR SECCIÓN -->
            <div class="section-wrap">
                <select class="select-custom" id="sectionSelect"></select>
            </div>

            <!-- TABS -->
            <div id="tabs" class="tabs-container"></div>

            <!-- CONTENIDO DINÁMICO -->
            <div id="content"></div>
        </div>
    </div>
</div>

<!-- MODAL PREDICCIONES -->
<div class="modal-overlay" id="modal-overlay">
    <div class="modal-container">
        <button class="modal-close" id="modal-close">&times;</button>
        <div class="modal-title" id="modal-titulo">Predicciones</div>
        <div class="modal-subtitle" id="modal-subtitulo">Selecciona tus predicciones</div>
        <div id="modal-contenido"></div>
        <div class="modal-actions">
            <button class="btn-primary" id="modal-enviar">Enviar</button>
            <button class="btn-secondary" id="modal-cancelar">Cancelar</button>
        </div>
    </div>
</div>

<script>
(function(){
    // ========== CONFIGURACIÓN INICIAL ==========
    const SECTION_TABS = {
        "UNIRSE MESA": ["Mesas activas", "Histórico de encuentros", "Histórico de apuestas"],
        "CREAR MESA": ["Elegir Deporte", "Configurar Encuentro", "Elegir Partidos", "Histórico de encuentros", "Histórico de apuestas"],
        "MESA JUGADOR": ["Mesas activas", "Histórico de encuentros", "Histórico de apuestas"],
        "MESA PRIVADA": ["Histórico de encuentros", "Histórico de apuestas", "Mesas privadas"]
    };
    const sectionOrder = ["UNIRSE MESA", "CREAR MESA", "MESA JUGADOR", "MESA PRIVADA"];

    // Estado global
    let currentSection = "UNIRSE MESA";
    let currentTab = SECTION_TABS[currentSection][0];
    
    // Crear mesa
    let deportesSeleccionados = new Set();
    let configuracionData = {};
    let partidosSeleccionados = new Set();
    let partidosData = [], partidosMap = new Map();
    
    // Predicciones
    let respuestasPartidos = {};
    let mesaActual = null;
    let tipoMesaActual = null;
    let publicRetoConfig = null;
    let activeQuestionsMap = null;

    // DOM elements
    const sectionSelect = document.getElementById('sectionSelect');
    const tabsEl = document.getElementById('tabs');
    const contentEl = document.getElementById('content');
    
    // Modal
    const modalOverlay = document.getElementById('modal-overlay');
    const modalTitulo = document.getElementById('modal-titulo');
    const modalSubtitulo = document.getElementById('modal-subtitulo');
    const modalContenido = document.getElementById('modal-contenido');
    const modalEnviar = document.getElementById('modal-enviar');
    const modalCancelar = document.getElementById('modal-cancelar');
    const modalClose = document.getElementById('modal-close');

    // ========== USUARIO ==========
    function cargarDatosUsuario() {
        try {
            const raw = localStorage.getItem("user_data");
            if (!raw) return;
            const u = JSON.parse(raw) || {};
            const alias = u.alias || u.nombre || "Invitado";
            document.getElementById("user-name-top").textContent = alias.startsWith("@") ? alias : `@${alias}`;
        } catch (_) {}
    }

    async function cargarSaldo() {
        const uid = localStorage.getItem("user_id");
        if (!uid) return;
        try {
            const r = await fetch(`https://gambt.pythonanywhere.com/ppm/saldo/${uid}`);
            const d = await r.json();
            if (d && typeof d.saldo !== "undefined") {
                document.getElementById("saldo-usuario").textContent = `$${parseFloat(d.saldo).toFixed(2)}`;
            }
        } catch (_) {}
    }

    async function cargarPuntos() {
        const uid = localStorage.getItem("user_id");
        if (!uid) return;
        try {
            const r = await fetch(`https://gambt.pythonanywhere.com/ppm/puntos/${uid}`);
            const d = await r.json();
            if (d) {
                document.getElementById("user-puntos").textContent = `${Number(d.puntos_actuales).toLocaleString()} pts`;
                document.getElementById("user-nivel").textContent = `${d.nivel} - ${d.descripcion_nivel || ""}`;
                document.getElementById("user-posicion").textContent = `Ranking: #${d.posicion_actual} de ${d.cantidad_jugadores}`;
            }
        } catch (_) {}
    }

    async function refrescarDatos() {
        await Promise.all([cargarSaldo(), cargarPuntos()]);
    }

    // ========== NAVEGACIÓN ==========
    function llenarSelect() {
        sectionSelect.innerHTML = "";
        sectionOrder.forEach(sec => {
            const opt = document.createElement("option");
            opt.value = sec;
            opt.textContent = sec;
            sectionSelect.appendChild(opt);
        });
        sectionSelect.value = currentSection;
        sectionSelect.addEventListener("change", (e) => {
            currentSection = e.target.value;
            currentTab = SECTION_TABS[currentSection][0];
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
            <div class="tab-btn ${tab === currentTab ? 'active' : ''}" data-tab="${tab}">${tab}</div>
        `).join("");
        tabsEl.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener("click", () => {
                currentTab = btn.dataset.tab;
                render();
            });
        });
    }

    // ========== RENDERIZADO DE VISTAS ==========
    async function renderMesasActivas() {
        contentEl.innerHTML = `
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">Mesas activas</div>
                    <div class="search-box"><i class="fas fa-search"></i><input type="text" id="buscador-mesas" placeholder="Buscar mesas..."></div>
                </div>
                <div id="mesas-grid" class="mesa-grid">Cargando...</div>
            </div>
        `;
        const grid = document.getElementById("mesas-grid");
        try {
            const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_cargar_mesas_activas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'cargar_mesas=true'
            });
            const data = await resp.json();
            if (data.success && data.data.html) {
                grid.innerHTML = data.data.html;
                // Adjuntar eventos Unirse
                grid.querySelectorAll('.btn-unirse').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        const grupo = btn.dataset.grupoRango;
                        const nombre = btn.dataset.nombreMesa;
                        const card = btn.closest('.mesa-card');
                        if (card && card.classList.contains('mesa-card-publica')) {
                            mostrarModalPublico(grupo, nombre);
                        } else {
                            mostrarModalMesa(grupo, nombre);
                        }
                    });
                });
            } else {
                grid.innerHTML = '<div class="empty-message">No hay mesas disponibles</div>';
            }
        } catch (e) {
            grid.innerHTML = '<div class="empty-message">Error de conexión</div>';
        }
        document.getElementById("buscador-mesas")?.addEventListener("input", (e) => {
            const term = e.target.value.toLowerCase();
            grid.querySelectorAll('.mesa-card').forEach(c => {
                c.style.display = c.textContent.toLowerCase().includes(term) ? '' : 'none';
            });
        });
    }

    async function renderMesasPrivadas() {
        contentEl.innerHTML = `
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">Mesas privadas</div>
                    <div class="search-box"><i class="fas fa-search"></i><input type="text" id="buscador-privadas" placeholder="Buscar..."></div>
                </div>
                <div id="mesas-privadas-grid" class="mesa-grid">Cargando...</div>
            </div>
        `;
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
                // Eventos para botones privados
                grid.querySelectorAll('.btn-copy-code').forEach(b => {
                    b.addEventListener('click', (e) => {
                        e.stopPropagation();
                        navigator.clipboard?.writeText(b.dataset.codigo);
                        alert('Código copiado');
                    });
                });
                grid.querySelectorAll('.btn-validar-privado').forEach(b => {
                    b.addEventListener('click', async (e) => {
                        e.stopPropagation();
                        const card = b.closest('.mesa-card');
                        const pwd = card.querySelector('.privado-password-input').value;
                        if (!pwd) return alert('Ingresa contraseña');
                        const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_validar_llave_privada', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: `reto_llave=${b.dataset.llave}&password=${pwd}`
                        });
                        const d = await resp.json();
                        if (d.success) {
                            card.querySelector('.privado-password-container').style.display = 'none';
                            card.querySelector('.btn-aceptar-privado').style.display = 'block';
                        } else alert('Contraseña incorrecta');
                    });
                });
                grid.querySelectorAll('.btn-aceptar-privado').forEach(b => {
                    b.addEventListener('click', (e) => {
                        e.stopPropagation();
                        mostrarModalPrivado(b.dataset.llave, b.dataset.nombreMesa);
                    });
                });
            } else {
                grid.innerHTML = '<div class="empty-message">No hay mesas privadas</div>';
            }
        } catch (e) {
            grid.innerHTML = '<div class="empty-message">Error de conexión</div>';
        }
        document.getElementById("buscador-privadas")?.addEventListener("input", (e) => {
            const term = e.target.value.toLowerCase();
            grid.querySelectorAll('.mesa-card').forEach(c => {
                c.style.display = c.textContent.toLowerCase().includes(term) ? '' : 'none';
            });
        });
    }

    function renderElegirDeporte() {
        contentEl.innerHTML = `
            <div class="panel">
                <div class="form-group">
                    <div class="form-label">Nombre mesa (máx 30)</div>
                    <input class="input-field" id="nombre-mesa" maxlength="30" placeholder="Ej: Torneo de expertos" value="${configuracionData.nombreMesa || ''}">
                </div>
                <div class="form-group">
                    <div class="form-label">Deportes</div>
                    <div class="checkbox-group">
                        ${['Fútbol','Baloncesto','Tenis'].map(d => `
                            <label class="checkbox-item"><input type="checkbox" value="${d}" ${deportesSeleccionados.has(d)?'checked':''}> ${d}</label>
                        `).join('')}
                    </div>
                </div>
                <button class="btn-next" id="btn-next-deportes" ${deportesSeleccionados.size>0?'':'disabled'}>SIGUIENTE</button>
            </div>
        `;
        const nombreInp = document.getElementById('nombre-mesa');
        const btnNext = document.getElementById('btn-next-deportes');
        const cbs = document.querySelectorAll('input[type=checkbox]');
        const actualizar = () => {
            const valido = nombreInp.value.trim().length > 0 && nombreInp.value.length <= 30;
            btnNext.disabled = !(deportesSeleccionados.size > 0 && valido);
        };
        nombreInp.addEventListener('input', actualizar);
        cbs.forEach(cb => cb.addEventListener('change', (e) => {
            if (cb.checked) deportesSeleccionados.add(cb.value);
            else deportesSeleccionados.delete(cb.value);
            actualizar();
        }));
        btnNext.addEventListener('click', () => {
            configuracionData.nombreMesa = nombreInp.value.trim();
            configuracionData.deportes = Array.from(deportesSeleccionados);
            currentTab = "Configurar Encuentro";
            render();
        });
        actualizar();
    }

    function renderConfigurarEncuentro() {
        const pregGuardadas = configuracionData.preguntasSeleccionadas || ['ganador'];
        contentEl.innerHTML = `
            <div class="panel">
                <div class="form-group"><div class="form-label">Apuesta mínima (USD)</div><input class="input-field" id="monto-min" type="number" min="1" value="${configuracionData.montoMinimo||''}"></div>
                <div class="form-group"><div class="form-label">Tipo de reto</div><div class="radio-group"><label><input type="radio" name="tipo-reto" value="Público" ${configuracionData.tipoReto!=='Privado'?'checked':''}> Público</label><label><input type="radio" name="tipo-reto" value="Privado" ${configuracionData.tipoReto==='Privado'?'checked':''}> Privado</label></div></div>
                <div class="form-group"><div class="form-label">Ganadores</div><div class="radio-group"><label><input type="radio" name="ganadores" value="Único Ganador" ${configuracionData.ganadores!=='Varios Ganadores'?'checked':''}> Único</label><label><input type="radio" name="ganadores" value="Varios Ganadores" ${configuracionData.ganadores==='Varios Ganadores'?'checked':''}> Varios</label></div></div>
                <div class="form-group"><div class="form-label">Preguntas (1-4)</div><div class="checkbox-group">
                    <label class="checkbox-item"><input type="checkbox" value="ganador" ${pregGuardadas.includes('ganador')?'checked':''}> Definir ganador</label>
                    <label class="checkbox-item"><input type="checkbox" value="ambos_goles" ${pregGuardadas.includes('ambos_goles')?'checked':''}> ¿Gol de ambos?</label>
                    <label class="checkbox-item"><input type="checkbox" value="penales" ${pregGuardadas.includes('penales')?'checked':''}> ¿Penales?</label>
                    <label class="checkbox-item"><input type="checkbox" value="marcador" ${pregGuardadas.includes('marcador')?'checked':''}> Predice marcador</label>
                </div></div>
                <div class="form-group"><div class="form-label">Tipo de Mesa</div><div class="radio-group">
                    <label><input type="radio" name="tipo-mesa" value="Selección" ${configuracionData.tipoMesa!=='Torneo corto'&&configuracionData.tipoMesa!=='Torneo Largo'?'checked':''}> Selección</label>
                    <label><input type="radio" name="tipo-mesa" value="Torneo corto" ${configuracionData.tipoMesa==='Torneo corto'?'checked':''}> Torneo corto</label>
                    <label><input type="radio" name="tipo-mesa" value="Torneo Largo" ${configuracionData.tipoMesa==='Torneo Largo'?'checked':''}> Torneo largo</label>
                </div></div>
                <button class="btn-next" id="btn-next-config" disabled>SIGUIENTE</button>
            </div>
        `;
        const monto = document.getElementById('monto-min');
        const btn = document.getElementById('btn-next-config');
        const cbs = document.querySelectorAll('input[name="preguntas"]');
        const validar = () => {
            const sel = Array.from(cbs).filter(c=>c.checked).length;
            btn.disabled = !(parseFloat(monto.value)>0 && sel>=1 && sel<=4);
        };
        monto.addEventListener('input', validar);
        cbs.forEach(c=>c.addEventListener('change', validar));
        validar();
        btn.addEventListener('click', () => {
            configuracionData.montoMinimo = monto.value;
            configuracionData.tipoReto = document.querySelector('input[name="tipo-reto"]:checked').value;
            configuracionData.ganadores = document.querySelector('input[name="ganadores"]:checked').value;
            configuracionData.preguntasSeleccionadas = Array.from(document.querySelectorAll('input[name="preguntas"]:checked')).map(c=>c.value);
            configuracionData.tipoMesa = document.querySelector('input[name="tipo-mesa"]:checked').value;
            currentTab = "Elegir Partidos";
            render();
        });
    }

    async function renderElegirPartidos() {
        contentEl.innerHTML = `<div class="panel"><div class="panel-title">Partidos disponibles</div><div id="partidos-lista" class="mesa-grid">Cargando...</div><button class="btn-next" id="btn-enviar-partidos" disabled>ENVIAR</button></div>`;
        try {
            const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_retos_grupales_ajax');
            const html = await resp.text();
            const div = document.createElement('div');
            div.innerHTML = html;
            partidosData = [];
            partidosMap.clear();
            div.querySelectorAll('tbody tr[data-mid]').forEach(fila => {
                const id = fila.dataset.mid;
                const celdas = fila.querySelectorAll('td');
                const eq = celdas[0]?.querySelector('.g-row');
                const nombres = eq?.querySelectorAll('span');
                partidosData.push({
                    id, local: nombres?.[0]?.textContent||'Local', visita: nombres?.[2]?.textContent||'Visitante',
                    horario: celdas[1]?.textContent||''
                });
                partidosMap.set(id, partidosData[partidosData.length-1]);
            });
        } catch (e) { /* fallback */ }
        const lista = document.getElementById('partidos-lista');
        lista.innerHTML = partidosData.map(p => `
            <div class="mesa-card ${partidosSeleccionados.has(p.id)?'selected':''}" data-id="${p.id}" style="border-color:${partidosSeleccionados.has(p.id)?'#ffe855':'#00eaff'}">
                <div class="mesa-title">${p.local} vs ${p.visita}</div>
                <div class="mesa-info">${p.horario}</div>
            </div>
        `).join('');
        const btnEnviar = document.getElementById('btn-enviar-partidos');
        const actualizarBtn = () => { btnEnviar.disabled = partidosSeleccionados.size===0; };
        lista.querySelectorAll('.mesa-card').forEach(card => {
            card.addEventListener('click', () => {
                const id = card.dataset.id;
                if (partidosSeleccionados.has(id)) partidosSeleccionados.delete(id);
                else partidosSeleccionados.add(id);
                card.style.borderColor = partidosSeleccionados.has(id)?'#ffe855':'#00eaff';
                actualizarBtn();
            });
        });
        btnEnviar.addEventListener('click', mostrarModalCrearReto);
        actualizarBtn();
    }

    function renderHistorial(tipo) {
        contentEl.innerHTML = `<div class="panel"><div class="panel-title">Histórico de ${tipo}</div><div class="empty-message">No hay datos</div></div>`;
    }

    // ========== MODALES ==========
    function cerrarModal() { modalOverlay.style.display = 'none'; respuestasPartidos = {}; }

    async function mostrarModalPublico(llave, nombre) {
        tipoMesaActual = 'publica'; mesaActual = llave;
        modalTitulo.textContent = `Reto: ${nombre}`;
        modalOverlay.style.display = 'flex';
        modalContenido.innerHTML = 'Cargando...';
        const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_cargar_partidos_publicos', {
            method: 'POST', headers: {'Content-Type':'application/x-www-form-urlencoded'}, body: `llave=${llave}`
        });
        const data = await resp.json();
        if (!data.success) { alert('Error'); return cerrarModal(); }
        const partidos = data.data.partidos;
        publicRetoConfig = data.data.config;
        let html = '';
        partidos.forEach(p => {
            respuestasPartidos[p.partido_id] = { id_partido: p.partido_id };
            html += `<div class="prediction-item"><div class="prediction-header">${p.local_nombre} vs ${p.visita_nombre}</div>`;
            html += `<div class="prediction-options">${['Local','Empate','Visitante'].map(v=>`<div class="prediction-option" data-pid="${p.partido_id}" data-preg="ganador" data-val="${v}">${v}</div>`).join('')}</div>`;
            html += `</div>`;
        });
        modalContenido.innerHTML = html;
        modalContenido.querySelectorAll('.prediction-option').forEach(opt => {
            opt.addEventListener('click', () => {
                const pid = opt.dataset.pid, preg = opt.dataset.preg, val = opt.dataset.val;
                respuestasPartidos[pid][preg] = val;
                opt.parentNode.querySelectorAll('.prediction-option').forEach(o=>o.classList.remove('selected'));
                opt.classList.add('selected');
            });
        });
        modalEnviar.onclick = enviarApuesta;
    }

    async function mostrarModalMesa(grupo, nombre) {
        tipoMesaActual = 'local'; mesaActual = grupo;
        modalTitulo.textContent = `Mesa: ${nombre}`;
        modalOverlay.style.display = 'flex';
        modalContenido.innerHTML = 'Cargando...';
        const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_cargar_partidos_mesa', {
            method: 'POST', headers: {'Content-Type':'application/x-www-form-urlencoded'}, body: `grupo_rango=${grupo}`
        });
        const data = await resp.json();
        if (!data.success) { alert('Error'); return cerrarModal(); }
        modalContenido.innerHTML = data.data.html;
        modalContenido.querySelectorAll('.partido-item-mejorado').forEach(item => {
            const pid = item.dataset.partidoId;
            respuestasPartidos[pid] = { id_partido: pid };
        });
        modalContenido.querySelectorAll('.opcion-mejorada').forEach(opt => {
            opt.addEventListener('click', () => {
                const pid = opt.dataset.partidoId, preg = opt.dataset.pregunta, val = opt.dataset.valor;
                respuestasPartidos[pid][preg] = val;
                opt.closest('.opciones-grid-mejorado').querySelectorAll('.opcion-mejorada').forEach(o=>o.classList.remove('selected'));
                opt.classList.add('selected');
            });
        });
        modalEnviar.onclick = enviarApuesta;
    }

    async function mostrarModalPrivado(llave, nombre) {
        tipoMesaActual = 'privada'; mesaActual = llave;
        modalTitulo.textContent = `Privado: ${nombre}`;
        modalOverlay.style.display = 'flex';
        modalContenido.innerHTML = 'Cargando...';
        const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_cargar_preguntas_privadas', {
            method: 'POST', headers: {'Content-Type':'application/x-www-form-urlencoded'}, body: `reto_llave=${llave}`
        });
        const data = await resp.json();
        if (!data.success) { alert('Error'); return cerrarModal(); }
        let html = '';
        data.data.partidos.forEach(p => {
            respuestasPartidos[p.partido_id] = { id_partido: p.partido_id };
            html += `<div class="prediction-item"><div class="prediction-header">${p.local_nombre} vs ${p.visita_nombre}</div>`;
            html += `<div class="prediction-options">${['Local','Empate','Visitante'].map(v=>`<div class="prediction-option" data-pid="${p.partido_id}" data-preg="ganador" data-val="${v}">${v}</div>`).join('')}</div>`;
            html += `</div>`;
        });
        modalContenido.innerHTML = html;
        modalContenido.querySelectorAll('.prediction-option').forEach(opt => {
            opt.addEventListener('click', () => {
                const pid = opt.dataset.pid, preg = opt.dataset.preg, val = opt.dataset.val;
                respuestasPartidos[pid][preg] = val;
                opt.parentNode.querySelectorAll('.prediction-option').forEach(o=>o.classList.remove('selected'));
                opt.classList.add('selected');
            });
        });
        modalEnviar.onclick = enviarApuesta;
    }

    function mostrarModalCrearReto() {
        if (partidosSeleccionados.size===0) return alert('Selecciona partidos');
        respuestasPartidos = {};
        modalTitulo.textContent = 'Crear Reto';
        modalOverlay.style.display = 'flex';
        let html = '';
        Array.from(partidosSeleccionados).forEach(id => {
            const p = partidosMap.get(id);
            respuestasPartidos[id] = { id_partido: id };
            html += `<div class="prediction-item"><div class="prediction-header">${p.local} vs ${p.visita}</div>`;
            html += `<div class="prediction-options">${['Local','Empate','Visitante'].map(v=>`<div class="prediction-option" data-pid="${id}" data-preg="ganador" data-val="${v}">${v}</div>`).join('')}</div>`;
            html += `</div>`;
        });
        modalContenido.innerHTML = html;
        modalContenido.querySelectorAll('.prediction-option').forEach(opt => {
            opt.addEventListener('click', () => {
                const pid = opt.dataset.pid, preg = opt.dataset.preg, val = opt.dataset.val;
                respuestasPartidos[pid][preg] = val;
                opt.parentNode.querySelectorAll('.prediction-option').forEach(o=>o.classList.remove('selected'));
                opt.classList.add('selected');
            });
        });
        modalEnviar.onclick = async () => {
            const userId = localStorage.getItem('user_id');
            const llave = [userId, ...Array.from(partidosSeleccionados)].join('-');
            const data = {
                user_id: userId, grupo_rango: 'creado_'+Date.now(), respuestas: respuestasPartidos,
                apuesta_minima_usd: configuracionData.montoMinimo, preguntas_por_encuentro: configuracionData.preguntasSeleccionadas.length,
                tipo_reto: configuracionData.tipoReto, tipo_mesa: configuracionData.tipoMesa,
                pregunta_cuantos_ganadores: configuracionData.ganadores, llave, nombre_mesa: configuracionData.nombreMesa,
                modo_forzado: 'Crear_reto'
            };
            const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_guardar_apuesta_ppm', {
                method: 'POST', headers: {'Content-Type':'application/x-www-form-urlencoded'},
                body: `apuesta_data=${encodeURIComponent(JSON.stringify(data))}`
            });
            const d = await resp.json();
            if (d.success) { alert('Reto creado'); cerrarModal(); partidosSeleccionados.clear(); refrescarDatos(); }
            else alert('Error: '+d.data);
        };
    }

    async function enviarApuesta() {
        const userId = localStorage.getItem('user_id');
        const apuesta = { user_id: userId, grupo_rango: mesaActual, respuestas: respuestasPartidos };
        if (tipoMesaActual==='publica') apuesta.modo_forzado = 'Acepta_reto';
        else if (tipoMesaActual==='local') apuesta.modo_forzado = 'Acepta_reto_local';
        else apuesta.modo_forzado = 'Acepta reto privado';
        const resp = await fetch('/wp-admin/admin-ajax.php?action=gambt_guardar_apuesta_ppm', {
            method: 'POST', headers: {'Content-Type':'application/x-www-form-urlencoded'},
            body: `apuesta_data=${encodeURIComponent(JSON.stringify(apuesta))}`
        });
        const d = await resp.json();
        if (d.success) { alert('Apuesta registrada'); cerrarModal(); refrescarDatos(); }
        else alert('Error: '+d.data);
    }

    // ========== RENDER PRINCIPAL ==========
    function renderContent() {
        if (currentTab === "Mesas activas") renderMesasActivas();
        else if (currentTab === "Mesas privadas") renderMesasPrivadas();
        else if (currentTab === "Elegir Deporte") renderElegirDeporte();
        else if (currentTab === "Configurar Encuentro") renderConfigurarEncuentro();
        else if (currentTab === "Elegir Partidos") renderElegirPartidos();
        else if (currentTab.includes("Histórico")) renderHistorial(currentTab);
        else contentEl.innerHTML = `<div class="panel"><div class="empty-message">Vista no implementada</div></div>`;
    }

    function render() { renderTabs(); renderContent(); }

    // Eventos globales
    document.getElementById('logo-link').addEventListener('click', e=>{ e.preventDefault(); window.location.href='https://www.gambt.online/Inicio GAMBT/'; });
    document.getElementById('btn-entrar-classic').addEventListener('click', ()=> window.location.href='https://www.gambt.online/elementor-1641/');
    document.getElementById('user-menu-btn').addEventListener('click', ()=> window.location.href='https://www.gambt.online/entorno-usuario/');
    modalClose.onclick = cerrarModal; modalCancelar.onclick = cerrarModal;
    modalOverlay.addEventListener('click', e=>{ if(e.target===modalOverlay) cerrarModal(); });

    // Inicio
    cargarDatosUsuario(); refrescarDatos(); llenarSelect(); render();
    setInterval(refrescarDatos, 30000);
})();
</script>
</body>
</html>
