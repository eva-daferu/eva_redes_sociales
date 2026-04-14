# app.py
import streamlit as st
import streamlit.components.v1 as components

# ===== AJUSTES =====
PHONE_W_PX = 390
PHONE_H_PX = 844
PHONE_BORDER_PX = 3
PHONE_BORDER_COLOR = "#111111"
PHONE_BG = "#FFFFFF"
OUTSIDE_BG = "#EDEDED"

GRID_COLOR = "rgba(0,0,0,0.10)"
MID_COLOR = "rgba(0,0,0,0.25)"
BLOCK_BORDER = "2px dashed rgba(0,0,0,.55)"
BLOCK_BG = "rgba(0,0,0,.03)"
LABEL_BG = "rgba(255,255,255,.92)"

# BLOQUES MOBILE (0–100 dentro del área total scrollable del teléfono)
# id, left, top, width, height
BLOCKS = [
    # HEADER
    {"id": "SOCIALS",               "left": 4,  "top": 2.0,  "width": 22, "height": 3.2},
    {"id": "LOGO",                  "left": 27, "top": 1.2,  "width": 46, "height": 5.0},
    {"id": "LANGUAGE",              "left": 6,  "top": 8.2,  "width": 40, "height": 4.8},
    {"id": "SETTINGS",              "left": 54, "top": 8.2,  "width": 40, "height": 4.8},
    {"id": "USER",                  "left": 6,  "top": 14.0, "width": 88, "height": 4.8},

    # MODOS
    {"id": "CARD_PPM",              "left": 6,  "top": 22.0, "width": 88, "height": 8.8},
    {"id": "CARD_CLASSIC",          "left": 6,  "top": 32.2, "width": 88, "height": 8.8},

    # WALLET
    {"id": "CARD_WALLET",           "left": 6,  "top": 42.4, "width": 88, "height": 13.8},
    {"id": "WALLET_USD",            "left": 10, "top": 46.4, "width": 36, "height": 4.4},
    {"id": "WALLET_POINTS",         "left": 54, "top": 46.4, "width": 36, "height": 4.4},
    {"id": "WALLET_RECARGAR",       "left": 10, "top": 52.0, "width": 36, "height": 4.2},
    {"id": "WALLET_CANJEAR",        "left": 54, "top": 52.0, "width": 36, "height": 4.2},

    # POZO RETOS GRUPALES
    {"id": "POZO_PANEL",            "left": 6,  "top": 58.6, "width": 88, "height": 10.8},
    {"id": "POZO_PARTICIPANTES",    "left": 58, "top": 60.4, "width": 14, "height": 3.8},
    {"id": "POZO_BOLSA",            "left": 76, "top": 60.4, "width": 14, "height": 3.8},
    {"id": "POZO_BTN_UNIRSE",       "left": 10, "top": 65.0, "width": 36, "height": 4.4},
    {"id": "POZO_BTN_HISTORIAL",    "left": 54, "top": 65.0, "width": 36, "height": 4.4},

    # RETOS GRUPALES -> en móvil pasa de tabla a tarjetas
    {"id": "RETOS_TITULO",          "left": 8,  "top": 72.2, "width": 42, "height": 3.0},
    {"id": "RETO_CARD_01",          "left": 6,  "top": 76.0, "width": 88, "height": 5.4},
    {"id": "RETO_CARD_02",          "left": 6,  "top": 82.2, "width": 88, "height": 5.4},
    {"id": "RETO_CARD_03",          "left": 6,  "top": 88.4, "width": 88, "height": 5.4},
    {"id": "RETO_CARD_04",          "left": 6,  "top": 94.6, "width": 88, "height": 5.0},

    # ASISTENTE -> en móvil se colapsa a botón flotante
    {"id": "ASISTENTE_FLOAT",       "left": 78, "top": 70.5, "width": 16, "height": 4.8},
]
# ===================

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
      --phone-w:{PHONE_W_PX}px;
      --phone-h:{PHONE_H_PX}px;
      --phone-border:{PHONE_BORDER_PX}px;
      --phone-border-color:{PHONE_BORDER_COLOR};
      --phone-bg:{PHONE_BG};
      --outside-bg:{OUTSIDE_BG};
      --grid-color:{GRID_COLOR};
      --mid-color:{MID_COLOR};
      --block-border:{BLOCK_BORDER};
      --block-bg:{BLOCK_BG};
      --label-bg:{LABEL_BG};
    }}

    *{{box-sizing:border-box;}}
    html, body{{
      margin:0;
      padding:0;
      width:100%;
      height:100%;
      overflow:hidden;
      background:var(--outside-bg);
      font-family:Arial, sans-serif;
    }}

    #stage{{
      position:fixed;
      inset:0;
      width:100vw;
      height:100vh;
      display:flex;
      align-items:center;
      justify-content:center;
      background:var(--outside-bg);
    }}

    #phone{{
      position:relative;
      width:min(var(--phone-w), 96vw);
      height:min(var(--phone-h), 96vh);
      aspect-ratio:390 / 844;
      border:var(--phone-border) solid var(--phone-border-color);
      border-radius:28px;
      background:var(--phone-bg);
      overflow:auto;
      box-shadow:0 10px 35px rgba(0,0,0,.18);
    }}

    #screen{{
      position:relative;
      width:100%;
      height:215%;
      background:var(--phone-bg);
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
        linear-gradient(to right, var(--grid-color) 1px, transparent 1px),
        linear-gradient(to bottom, var(--grid-color) 1px, transparent 1px);
      background-size:10% 10%;
    }}

    .mid-v{{
      position:absolute;
      left:50%;
      top:0;
      bottom:0;
      width:1px;
      background:var(--mid-color);
    }}

    .mid-h{{
      position:absolute;
      top:50%;
      left:0;
      right:0;
      height:1px;
      background:var(--mid-color);
    }}

    .blk{{
      position:absolute;
      border:var(--block-border);
      background:var(--block-bg);
    }}

    .blk-label{{
      position:absolute;
      top:2px;
      left:2px;
      font:11px Arial, sans-serif;
      background:var(--label-bg);
      border:1px solid rgba(0,0,0,.15);
      border-radius:4px;
      padding:2px 6px;
      white-space:nowrap;
    }}

    #hud{{
      position:sticky;
      top:8px;
      left:8px;
      margin:8px;
      width:max-content;
      font:12px Arial, sans-serif;
      background:rgba(255,255,255,.95);
      border:1px solid rgba(0,0,0,.2);
      border-radius:6px;
      padding:6px 10px;
      z-index:3;
      pointer-events:none;
    }}
  </style>
</head>
<body>
  <div id="stage">
    <div id="phone">
      <div id="screen">
        <div id="overlay">
          <div class="grid"></div>
          <div class="mid-v"></div>
          <div class="mid-h"></div>
          {blocks_to_html(BLOCKS)}
        </div>
        <div id="hud">Cargando...</div>
      </div>
    </div>
  </div>

  <script>
    (function(){{
      var hud = document.getElementById("hud");
      var phone = document.getElementById("phone");
      var screen = document.getElementById("screen");

      function update(){{
        var pw = Math.round(phone.clientWidth);
        var ph = Math.round(phone.clientHeight);
        var sh = Math.round(screen.clientHeight);

        hud.textContent =
          "Phone(px): " + pw + " x " + ph +
          " | Alto plano: " + sh +
          " | 10% ancho=" + Math.round(pw * 0.10) + "px" +
          " | 10% alto plano=" + Math.round(sh * 0.10) + "px";
      }}

      window.addEventListener("resize", update);
      update();
    }})();
  </script>
</body>
</html>
"""

components.html(html, height=960, scrolling=False)
