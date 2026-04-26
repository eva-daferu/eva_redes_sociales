import streamlit as st
import streamlit.components.v1 as components

PAD_X_PX = 8
PAD_TOP_PX = 8
BORDER_PX = 2
BORDER_COLOR = "#111111"
BG_COLOR = "#FFFFFF"

BLOCKS = [
    {"id": "HERO_TEXTO", "left": 4, "top": 3, "width": 92, "height": 18},
    {"id": "HERO_IMAGEN", "left": 4, "top": 22, "width": 92, "height": 22},
    {"id": "BENEFICIOS_2X2", "left": 4, "top": 45, "width": 92, "height": 14},

    {"id": "VIDEOS_TITULO", "left": 4, "top": 60, "width": 92, "height": 4},
    {"id": "VIDEO_1", "left": 4, "top": 65, "width": 92, "height": 10},
    {"id": "VIDEO_2", "left": 4, "top": 76, "width": 92, "height": 10},
    {"id": "VIDEO_3", "left": 4, "top": 87, "width": 92, "height": 10},

    {"id": "WHY_CHOOSE", "left": 4, "top": 99, "width": 92, "height": 20},
    {"id": "HOW_IT_WORKS", "left": 4, "top": 121, "width": 92, "height": 22},

    {"id": "PACK_1", "left": 4, "top": 145, "width": 92, "height": 15},
    {"id": "PACK_2_DESTACADO", "left": 4, "top": 162, "width": 92, "height": 16},
    {"id": "PACK_3", "left": 4, "top": 180, "width": 92, "height": 15},

    {"id": "GARANTIAS", "left": 4, "top": 197, "width": 92, "height": 14},
    {"id": "TESTIMONIOS", "left": 4, "top": 213, "width": 92, "height": 22},
    {"id": "FAQ", "left": 4, "top": 237, "width": 92, "height": 18},
    {"id": "CTA_FINAL", "left": 4, "top": 257, "width": 92, "height": 14},
    {"id": "FOOTER", "left": 0, "top": 273, "width": 100, "height": 18},
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
      height:291vh;
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
      background:transparent;
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
      background-size: 10% 5%;
    }}

    .mid-v{{
      position:absolute;
      left:50%;
      top:0;
      bottom:0;
      width:1px;
      background:rgba(255,90,20,.45);
    }}

    #hud{{
      position:fixed;
      top:8px;
      left:8px;
      font:11px Arial, sans-serif;
      background:rgba(255,255,255,.94);
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
      background:rgba(255,255,255,.94);
      border:1px solid rgba(0,0,0,.14);
      border-radius:4px;
      padding:2px 5px;
      white-space:nowrap;
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
        hud.textContent = "Móvil Top Fire Protect | Viewport: " + vw + " x " + vh;
      }}

      window.addEventListener("resize", update);
      update();
    }})();
  </script>
</body>
</html>
"""

components.html(html, height=10, scrolling=True)
