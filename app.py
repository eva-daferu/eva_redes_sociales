import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES =====
PAD_X_PX = 8
PAD_TOP_PX = 8
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"

# PLANO WEB SEGÚN TU ESTRUCTURA
# Contenedor1 aumentado 4 veces en alto.
# Todos los bloques posteriores fueron bajados +36 puntos en top.
BLOCKS = [
    {"id": "Contenedor1", "left": 2, "top": 1, "width": 96, "height": 48},

    {"id": "Texto1", "left": 18, "top": 51, "width": 74, "height": 2.2},

    {"id": "Video1", "left": 18, "top": 55, "width": 22, "height": 8},
    {"id": "Video2", "left": 47, "top": 55, "width": 21, "height": 8},
    {"id": "Video3", "left": 78, "top": 55, "width": 15, "height": 8},

    {"id": "Texto2", "left": 29, "top": 65, "width": 48, "height": 2.2},

    {"id": "Contenedor2", "left": 2, "top": 69, "width": 17, "height": 8},
    {"id": "Contenedor3", "left": 29, "top": 69, "width": 18, "height": 8},
    {"id": "Contenedor4", "left": 59, "top": 69, "width": 18, "height": 8},
    {"id": "Contenedor5", "left": 83, "top": 69, "width": 15, "height": 8},

    {"id": "Texto3", "left": 29, "top": 79, "width": 48, "height": 2.2},

    {"id": "Contenedor6", "left": 13, "top": 83, "width": 17, "height": 8},
    {"id": "Contenedor7", "left": 41, "top": 83, "width": 19, "height": 8},
    {"id": "Contenedor8", "left": 67, "top": 83, "width": 25, "height": 8},

    {"id": "Texto4", "left": 29, "top": 93, "width": 38, "height": 2.2},

    {"id": "Contenedor9", "left": 13, "top": 97, "width": 17, "height": 8},
    {"id": "Contenedor10", "left": 41, "top": 97, "width": 19, "height": 8},
    {"id": "Contenedor11", "left": 67, "top": 97, "width": 25, "height": 8},

    {"id": "Icono1 y texto", "left": 29, "top": 107, "width": 19, "height": 2.2},
    {"id": "Icono2 y texto", "left": 59, "top": 107, "width": 18, "height": 2.2},

    {"id": "Icono 3 y texto", "left": 13, "top": 111, "width": 28, "height": 4},
    {"id": "Icono 4 y texto", "left": 41, "top": 111, "width": 27, "height": 4},
    {"id": "Icono 5 y texto", "left": 68, "top": 111, "width": 24, "height": 4},

    {"id": "Texto5", "left": 29, "top": 117, "width": 38, "height": 2.2},

    {"id": "Comentario1", "left": 13, "top": 121, "width": 17, "height": 8},
    {"id": "Comentario2", "left": 41, "top": 121, "width": 19, "height": 8},
    {"id": "Comentario3", "left": 67, "top": 121, "width": 25, "height": 8},

    {"id": "Listado", "left": 2, "top": 131, "width": 38, "height": 8},
    {"id": "Foto", "left": 47, "top": 131, "width": 51, "height": 8},

    {"id": "Header", "left": 0, "top": 141, "width": 100, "height": 7},
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
      height:148vh;
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

    .blk{{
      position:absolute;
      border:2px solid #111;
      box-sizing:border-box;
      background:#fff;
    }}

    .blk-label{{
      position:absolute;
      top:4px;
      left:5px;
      font:15px Arial, sans-serif;
      color:#000;
      white-space:nowrap;
    }}
  </style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>
    <div id="overlay">
      {blocks_to_html(BLOCKS)}
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
    }})();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=True)
