# app.py
import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES (EDITA SOLO ESTO) =====
PAD_X_PX = 10
PAD_TOP_PX = 10
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"

# BLOQUES (0–100 en % del viewport)
# id, left, top, width, height
BLOCKS = [
    {"id": "BTN1", "left": 10, "top": 10, "width": 20, "height": 10},
    {"id": "BTN2", "left": 32, "top": 10, "width": 20, "height": 10},
    {"id": "BTN3", "left": 54, "top": 10, "width": 20, "height": 10},
    {"id": "BTN4", "left": 76, "top": 10, "width": 14, "height": 10},
]
# ====================================

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
              <span class="blk-label">{b["id"]} ({b["left"]},{b["top"]}) {b["width"]}x{b["height"]}</span>
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
    html, body{{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:var(--bg);}}

    #stage{{position:fixed;inset:0;width:100vw;height:100vh;background:var(--bg);}}

    /* Marco (izq/der/sup) */
    #frame{{
      position:absolute;
      left:var(--padx); right:var(--padx);
      top:var(--padtop); bottom:0;
      border-left:var(--b) solid var(--bc);
      border-right:var(--b) solid var(--bc);
      border-top:var(--b) solid var(--bc);
      box-sizing:border-box;
      background:transparent;
      pointer-events:none;
    }}

    /* Overlay en coordenadas % (0–100) */
    #overlay{{
      position:absolute;
      inset:0;
      pointer-events:none;
    }}

    /* Líneas 50% (mitad) */
    .mid-v{{position:absolute;left:50%;top:0;bottom:0;width:1px;background:rgba(0,0,0,.25);}}
    .mid-h{{position:absolute;top:50%;left:0;right:0;height:1px;background:rgba(0,0,0,.25);}}

    /* Regla cada 10% */
    .grid{{
      position:absolute; inset:0;
      background-image:
        linear-gradient(to right, rgba(0,0,0,0.10) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0,0,0,0.10) 1px, transparent 1px);
      background-size: 10% 10%;
    }}

    /* Etiqueta medidas px */
    #hud{{
      position:absolute; top:8px; left:8px;
      font: 12px Arial, sans-serif;
      background: rgba(255,255,255,.92);
      border: 1px solid rgba(0,0,0,.2);
      border-radius: 6px;
      padding: 6px 10px;
      pointer-events:none;
    }}

    /* Bloques (rectángulos de referencia) */
    .blk{{
      position:absolute;
      border: 2px dashed rgba(0,0,0,.55);
      box-sizing:border-box;
      background: rgba(0,0,0,.03);
    }}
    .blk-label{{
      position:absolute;
      top:2px; left:2px;
      font: 11px Arial, sans-serif;
      background: rgba(255,255,255,.9);
      border: 1px solid rgba(0,0,0,.15);
      border-radius: 4px;
      padding: 2px 6px;
      white-space: nowrap;
    }}
  </style>
</head>
<body>
  <div id="stage">
    <div id="frame"></div>

    <div id="overlay">
      <div class="grid"></div>
      <div class="mid-v"></div>
      <div class="mid-h"></div>
      {blocks_to_html(BLOCKS)}
      <div id="hud">Cargando...</div>
    </div>
  </div>

  <script>
    (function(){{
      // Full-screen real del iframe
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
        hud.textContent = "Viewport(px): " + vw + " x " + vh + " | Mitad: " + Math.round(vw/2) + " x " + Math.round(vh/2)
          + " | %->px: 10%=" + Math.round(vw*0.10) + "px, 20%=" + Math.round(vw*0.20) + "px";
      }}
      window.addEventListener("resize", update);
      update();
    }})();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=False)
