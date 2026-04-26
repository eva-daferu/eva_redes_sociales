import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES =====
PAD_X_PX = 8
PAD_TOP_PX = 8
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"

# ESTRUCTURA MÓVIL SEGÚN TOP FIRE PROTECT
BLOCKS = [
    {"id": "BLOQUE_PRINCIPAL_HERO", "left": 4, "top": 2, "width": 92, "height": 22},

    {"id": "TEXTO_DEBAJO_HERO", "left": 4, "top": 25, "width": 92, "height": 5},

    {"id": "VIDEO_1", "left": 4, "top": 31, "width": 92, "height": 10},
    {"id": "VIDEO_2", "left": 4, "top": 42, "width": 92, "height": 10},
    {"id": "VIDEO_3", "left": 4, "top": 53, "width": 92, "height": 10},

    {"id": "TITULO_SOBRE_CAJAS_CENTRALES", "left": 4, "top": 65, "width": 92, "height": 5},

    {"id": "CAJA_1_INFO", "left": 4, "top": 71, "width": 44, "height": 10},
    {"id": "CAJA_2_INFO", "left": 52, "top": 71, "width": 44, "height": 10},
    {"id": "CAJA_3_INFO", "left": 4, "top": 82, "width": 44, "height": 10},
    {"id": "CAJA_4_INFO", "left": 52, "top": 82, "width": 44, "height": 10},

    {"id": "TEXTO_ABAJO_1", "left": 4, "top": 94, "width": 92, "height": 5},

    {"id": "PASO_1_TEXTO_IMAGEN", "left": 4, "top": 100, "width": 92, "height": 12},
    {"id": "PASO_2_TEXTO_IMAGEN", "left": 4, "top": 113, "width": 92, "height": 12},
    {"id": "PASO_3_TEXTO_IMAGEN", "left": 4, "top": 126, "width": 92, "height": 12},

    {"id": "TEXTO_ABAJO_2", "left": 4, "top": 140, "width": 92, "height": 5},

    {"id": "PRODUCTO_1_TEXTO_IMAGEN", "left": 4, "top": 146, "width": 92, "height": 14},
    {"id": "PRODUCTO_2_TEXTO_IMAGEN", "left": 4, "top": 161, "width": 92, "height": 14},
    {"id": "PRODUCTO_3_TEXTO_IMAGEN", "left": 4, "top": 176, "width": 92, "height": 14},

    {"id": "ICONO_1_ENVIO", "left": 12, "top": 192, "width": 34, "height": 6},
    {"id": "ICONO_2_GARANTIA", "left": 54, "top": 192, "width": 34, "height": 6},

    {"id": "INFO_GRIS_1", "left": 4, "top": 200, "width": 92, "height": 8},
    {"id": "INFO_GRIS_2", "left": 4, "top": 209, "width": 92, "height": 8},
    {"id": "INFO_GRIS_3", "left": 4, "top": 218, "width": 92, "height": 8},

    {"id": "TEXTO_TESTIMONIOS", "left": 4, "top": 228, "width": 92, "height": 5},

    {"id": "COMENTARIO_1_IMAGEN_TEXTO", "left": 4, "top": 234, "width": 92, "height": 11},
    {"id": "COMENTARIO_2_IMAGEN_TEXTO", "left": 4, "top": 246, "width": 92, "height": 11},
    {"id": "COMENTARIO_3_IMAGEN_TEXTO", "left": 4, "top": 258, "width": 92, "height": 11},

    {"id": "FAQ_LISTADO_IZQUIERDA", "left": 4, "top": 272, "width": 44, "height": 18},
    {"id": "BLOQUE_GRANDE_DERECHA", "left": 52, "top": 272, "width": 44, "height": 18},

    {"id": "HEADER_FOOTER_FINAL", "left": 0, "top": 292, "width": 100, "height": 14},
]

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

def blocks_to_html(blocks):
    out = []
    for b in blocks:
        out.append(
            f"""
            <div class="blk"
                 style="left:{b["left"]}%; top:{b["top"]}%;
                        width:{b["width"]}%; height:{b["height"]}%;">
              <span class="blk-label">{b["id"]}</span>
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
    }}

    html, body{{
      margin:0;
      padding:0;
      width:100%;
      min-height:100%;
      overflow:auto;
      background:var(--bg);
    }}

    #stage{{
      position:relative;
      width:100vw;
      height:306vh;
      background:var(--bg);
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
      pointer-events:none;
    }}

    #overlay{{
      position:absolute;
      inset:0;
      pointer-events:none;
    }}

    .grid{{
      position:absolute;
      inset:0;
      background-image:
        linear-gradient(to right, rgba(0,0,0,0.08) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0,0,0,0.08) 1px, transparent 1px);
      background-size:10% 5%;
    }}

    .mid-v{{
      position:absolute;
      left:50%;
      top:0;
      bottom:0;
      width:1px;
      background:rgba(255,80,20,.45);
    }}

    #hud{{
      position:fixed;
      top:8px;
      left:8px;
      font:11px Arial, sans-serif;
      background:rgba(255,255,255,.95);
      border:1px solid rgba(0,0,0,.2);
      border-radius:6px;
      padding:5px 8px;
      z-index:20;
      pointer-events:none;
    }}

    .blk{{
      position:absolute;
      border:2px dashed rgba(255,80,20,.75);
      box-sizing:border-box;
      background:rgba(255,80,20,.045);
      border-radius:8px;
    }}

    .blk-label{{
      position:absolute;
      top:4px;
      left:4px;
      font:10px Arial, sans-serif;
      font-weight:700;
      color:#111;
      background:rgba(255,255,255,.95);
      border:1px solid rgba(0,0,0,.14);
      border-radius:4px;
      padding:2px 5px;
      white-space:nowrap;
      max-width:92%;
      overflow:hidden;
      text-overflow:ellipsis;
    }}
  </style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>
    <div id="overlay">
      <div class="grid"></div>
      <div class="mid-v"></div>
      {blocks_to_html(BLOCKS)}
      <div id="hud">Cargando...</div>
    </div>
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

      var hud = document.getElementById("hud");

      function update(){{
        var vw = Math.round(window.innerWidth);
        var vh = Math.round(window.innerHeight);
        hud.textContent = "Top Fire Protect móvil | " + vw + " x " + vh;
      }}

      window.addEventListener("resize", update);
      update();
    }})();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=True)
