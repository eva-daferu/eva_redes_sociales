# app.py
import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES =====
PAD_X_PX = 8
PAD_TOP_PX = 8
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"
CANVAS_HEIGHT_VH = 185

# Coordenadas en % sobre el canvas móvil
BLOCKS = [
    {"id": "HEADER_BG", "label": "HEADER SUPERIOR", "note": "Logo + redes + idioma + ajustes + usuario", "left": 2, "top": 1, "width": 96, "height": 13, "kind": "header"},
    {"id": "LOGO", "label": "LOGO GAMBT", "left": 26, "top": 2, "width": 48, "height": 4, "kind": "header"},
    {"id": "SOCIALES", "label": "REDES", "note": "Iconos sociales", "left": 4, "top": 7, "width": 44, "height": 3.5, "kind": "button"},
    {"id": "IDIOMA", "label": "IDIOMA", "note": "Español", "left": 52, "top": 7, "width": 44, "height": 3.5, "kind": "button"},
    {"id": "AJUSTES", "label": "AJUSTES", "left": 4, "top": 10.8, "width": 44, "height": 3.5, "kind": "button"},
    {"id": "USUARIO", "label": "@pablico", "left": 52, "top": 10.8, "width": 44, "height": 3.5, "kind": "button"},

    {"id": "SALDO", "label": "SALDO", "note": "$30.00 / Recargar", "left": 3, "top": 16, "width": 45, "height": 8, "kind": "stat"},
    {"id": "PUNTOS", "label": "PUNTOS", "note": "0 pts / Nivel 0", "left": 52, "top": 16, "width": 45, "height": 8, "kind": "stat"},
    {"id": "RETOS_ACTIVOS", "label": "RETOS ACTIVOS", "note": "1", "left": 3, "top": 25, "width": 45, "height": 8, "kind": "stat"},
    {"id": "RETOS_CERRADOS_CARD", "label": "RETOS CERRADOS", "note": "0", "left": 52, "top": 25, "width": 45, "height": 8, "kind": "stat"},

    {"id": "TITULO", "label": "OPEN / CLOSED CHALLENGES", "left": 3, "top": 35, "width": 94, "height": 4, "kind": "title"},
    {"id": "TAB_ABIERTOS", "label": "RETOS ABIERTOS", "left": 3, "top": 40, "width": 47, "height": 5, "kind": "tab"},
    {"id": "TAB_CERRADOS", "label": "RETOS CERRADOS", "left": 50, "top": 40, "width": 47, "height": 5, "kind": "tab"},

    {"id": "BUSCAR_PARTIDO", "label": "BUSCAR PARTIDO", "left": 3, "top": 46.5, "width": 94, "height": 4.5, "kind": "search"},

    {"id": "FICHA_RETO", "label": "FICHA DE RETO", "note": "Tabla web convertida a card móvil", "left": 3, "top": 52.5, "width": 94, "height": 26, "kind": "panel"},
    {"id": "NOMBRE_MESA", "label": "Nombre Mesa", "note": "Creo mesa privada - Diana", "left": 5, "top": 55, "width": 90, "height": 3.8, "kind": "row"},
    {"id": "PARTIDO", "label": "Partido", "note": "Club Atlético de Madrid vs Athletic Club", "left": 5, "top": 59.3, "width": 90, "height": 3.8, "kind": "row"},
    {"id": "ESTADO", "label": "Estado", "note": "Retos Abiertos", "left": 5, "top": 63.6, "width": 43.5, "height": 3.8, "kind": "row"},
    {"id": "GANADOR", "label": "Ganador", "note": "NO_APLICA", "left": 51.5, "top": 63.6, "width": 43.5, "height": 3.8, "kind": "row"},
    {"id": "GOL_AMBOS", "label": "Gol Ambos", "note": "X", "left": 5, "top": 67.9, "width": 43.5, "height": 3.8, "kind": "row"},
    {"id": "PENALES", "label": "Penales", "note": "No", "left": 51.5, "top": 67.9, "width": 43.5, "height": 3.8, "kind": "row"},
    {"id": "MARCADOR", "label": "Marcador", "note": "X", "left": 5, "top": 72.2, "width": 43.5, "height": 3.8, "kind": "row"},
    {"id": "APUESTA_ACCIONES", "label": "Apuesta / Acción", "note": "$3.00 / Ver / Unirse / Editar", "left": 51.5, "top": 72.2, "width": 43.5, "height": 3.8, "kind": "row"},

    {"id": "PARTICIPANTES_TITULO", "label": "PARTICIPANTES DEL RETO", "left": 3, "top": 81, "width": 55, "height": 4, "kind": "title"},
    {"id": "BUSCAR_USUARIO", "label": "BUSCAR USUARIO", "left": 60, "top": 81, "width": 37, "height": 4, "kind": "search"},

    {"id": "PART_CARD_1", "label": "PARTICIPANTE 1", "note": "test1234 / Partido / Ganador / Bolsa $9.00", "left": 3, "top": 87, "width": 94, "height": 11, "kind": "card"},
    {"id": "PART_CARD_2", "label": "PARTICIPANTE 2", "note": "pablico / Partido / Ganador / Bolsa $9.00", "left": 3, "top": 99.5, "width": 94, "height": 11, "kind": "card"},
    {"id": "PART_CARD_3", "label": "PARTICIPANTE 3", "note": "Diana / Partido / Ganador / Bolsa $9.00", "left": 3, "top": 112, "width": 94, "height": 11, "kind": "card"},

    {"id": "USUARIOS_PANEL", "label": "USUARIOS", "note": "Panel derecho web convertido a sección móvil", "left": 3, "top": 127, "width": 94, "height": 23, "kind": "panel"},
    {"id": "BUSCAR_ALIAS", "label": "BUSCAR ALIAS", "left": 6, "top": 132, "width": 88, "height": 4.5, "kind": "search"},
    {"id": "USUARIOS_GRID", "label": "LISTA USUARIOS", "note": "Blanco / cristihan_gc / David / Diana / EliasMuki / Enano / Fantasma / Gym / Hulk / pablico", "left": 6, "top": 138, "width": 88, "height": 9, "kind": "card"},

    {"id": "ESPACIO_MENU", "label": "ESPACIO RESERVADO", "note": "Evita que el menú inferior tape contenido", "left": 3, "top": 154, "width": 94, "height": 8, "kind": "spacer"},
]

# Bloques fijos sobre el viewport móvil
FIXED_BLOCKS = [
    {"id": "MENU_BOTTOM", "label": "MENU INFERIOR FIJO", "left": 0, "top": 92, "width": 100, "height": 8, "kind": "fixed"},
    {"id": "CHAT", "label": "Chat", "left": 3, "top": 93, "width": 16, "height": 5.5, "kind": "fixed_item"},
    {"id": "USER_MENU", "label": "Usuario", "left": 22, "top": 93, "width": 16, "height": 5.5, "kind": "fixed_item"},
    {"id": "TABLA", "label": "Tabla", "left": 41, "top": 93, "width": 16, "height": 5.5, "kind": "fixed_item"},
    {"id": "ALERTA", "label": "Alerta", "left": 60, "top": 93, "width": 16, "height": 5.5, "kind": "fixed_item"},
    {"id": "SETTINGS", "label": "Config", "left": 79, "top": 93, "width": 18, "height": 5.5, "kind": "fixed_item"},
]
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

def blocks_to_html(blocks, fixed=False):
    out = []
    base_cls = "blk fixed-blk" if fixed else "blk"

    for b in blocks:
        note = b.get("note", "")
        note_html = f'<span class="blk-note">{note}</span>' if note else ""

        out.append(
            f"""
            <div class="{base_cls}"
                 data-kind="{b.get('kind', 'default')}"
                 style="left:{b['left']}%; top:{b['top']}%;
                        width:{b['width']}%; height:{b['height']}%;">
              <span class="blk-label">{b['label']}</span>
              {note_html}
              <span class="blk-coord">{b['id']} · ({b['left']},{b['top']}) {b['width']}x{b['height']}</span>
            </div>
            """
        )

    return "\n".join(out)

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
      --canvas-h:{CANVAS_HEIGHT_VH}vh;
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
      background:var(--bg);
      overflow-y:auto;
      overflow-x:hidden;
      -webkit-overflow-scrolling:touch;
    }}

    #canvas{{
      position:relative;
      width:100vw;
      min-height:var(--canvas-h);
      background:var(--bg);
      box-sizing:border-box;
    }}

    #frame{{
      position:absolute;
      left:var(--padx);
      right:var(--padx);
      top:var(--padtop);
      bottom:0;
      border-left:var(--b) solid var(--bc);
      border-right:var(--b) solid var(--bc);
      border-top:var(--b) solid var(--bc);
      box-sizing:border-box;
      background:transparent;
      pointer-events:none;
      z-index:1;
    }}

    #overlay{{
      position:absolute;
      inset:0;
      pointer-events:none;
      z-index:3;
    }}

    .grid{{
      position:absolute;
      inset:0;
      background-image:
        linear-gradient(to right, rgba(0,0,0,0.10) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0,0,0,0.10) 1px, transparent 1px);
      background-size:10% 5%;
      z-index:0;
    }}

    .mid-v{{
      position:absolute;
      left:50%;
      top:0;
      bottom:0;
      width:1px;
      background:rgba(0,0,0,.25);
      z-index:2;
    }}

    .mid-h{{
      position:absolute;
      top:50%;
      left:0;
      right:0;
      height:1px;
      background:rgba(0,0,0,.25);
      z-index:2;
    }}

    #hud{{
      position:fixed;
      top:6px;
      left:6px;
      max-width:calc(100vw - 12px);
      font:11px Arial, sans-serif;
      background:rgba(255,255,255,.94);
      border:1px solid rgba(0,0,0,.25);
      border-radius:6px;
      padding:5px 8px;
      pointer-events:none;
      z-index:999999;
      box-sizing:border-box;
      color:#111;
    }}

    .blk{{
      position:absolute;
      border:2px dashed rgba(0,0,0,.58);
      box-sizing:border-box;
      background:rgba(0,0,0,.035);
      overflow:hidden;
      border-radius:10px;
      z-index:4;
    }}

    .fixed-blk{{
      position:fixed;
      z-index:99999;
    }}

    .blk-label{{
      position:absolute;
      top:4px;
      left:6px;
      right:6px;
      font:700 11px Arial, sans-serif;
      line-height:1.15;
      color:#111;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }}

    .blk-note{{
      position:absolute;
      left:6px;
      right:6px;
      top:22px;
      font:10px Arial, sans-serif;
      line-height:1.15;
      color:#222;
      opacity:.92;
    }}

    .blk-coord{{
      position:absolute;
      left:6px;
      bottom:4px;
      font:9px Arial, sans-serif;
      color:#555;
      opacity:.75;
      white-space:nowrap;
    }}

    .blk[data-kind="header"]{{
      border-style:solid;
      background:rgba(0,0,0,.05);
    }}

    .blk[data-kind="button"]{{
      background:rgba(0,180,220,.08);
    }}

    .blk[data-kind="stat"]{{
      background:rgba(0,0,0,.04);
    }}

    .blk[data-kind="title"]{{
      border-style:solid;
      background:rgba(255,220,0,.10);
    }}

    .blk[data-kind="tab"]{{
      border-style:solid;
      background:rgba(255,220,0,.08);
    }}

    .blk[data-kind="search"]{{
      border-style:solid;
      background:rgba(0,180,220,.07);
      border-radius:999px;
    }}

    .blk[data-kind="panel"]{{
      border-style:solid;
      background:rgba(0,0,0,.035);
    }}

    .blk[data-kind="row"]{{
      border-style:dashed;
      border-radius:6px;
      background:rgba(255,255,255,.45);
    }}

    .blk[data-kind="card"]{{
      border-style:solid;
      background:rgba(0,0,0,.035);
    }}

    .blk[data-kind="spacer"]{{
      border-style:dotted;
      background:rgba(0,0,0,.02);
    }}

    .blk[data-kind="fixed"]{{
      border-style:solid;
      border-radius:16px 16px 0 0;
      background:rgba(255,255,255,.96);
    }}

    .blk[data-kind="fixed_item"]{{
      border-radius:999px;
      background:rgba(0,180,220,.10);
    }}

    @media (max-width:420px){{
      .blk-label{{
        font-size:10px;
      }}

      .blk-note{{
        font-size:9px;
      }}

      .blk-coord{{
        font-size:8px;
      }}
    }}
  </style>
</head>

<body>
  <div id="stage">
    <div id="canvas">
      <div class="grid"></div>
      <div id="frame"></div>

      <div id="overlay">
        <div class="mid-v"></div>
        <div class="mid-h"></div>
        {blocks_to_html(BLOCKS)}
      </div>
    </div>
  </div>

  <div id="fixedOverlay">
    {blocks_to_html(FIXED_BLOCKS, fixed=True)}
  </div>

  <div id="hud">Cargando...</div>

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

      var hud = document.getElementById("hud");
      var canvas = document.getElementById("canvas");
      var stage = document.getElementById("stage");

      function update(){{
        var vw = Math.round(window.innerWidth);
        var vh = Math.round(window.innerHeight);
        var ch = Math.round(canvas.scrollHeight);

        hud.textContent =
          "Viewport: " + vw + " x " + vh +
          " | Canvas: " + ch + "px" +
          " | Scroll: " + Math.round(stage.scrollTop) +
          " | 10% ancho=" + Math.round(vw * 0.10) + "px";
      }}

      window.addEventListener("resize", update);
      stage.addEventListener("scroll", update);
      update();
    }})();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
