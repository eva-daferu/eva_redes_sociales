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
OUTER_BORDER = "2px dashed rgba(0,0,0,.60)"
INNER_BORDER = "1.5px dashed rgba(0,0,0,.45)"
OUTER_BG = "rgba(0,0,0,.04)"
INNER_BG = "rgba(0,0,0,.02)"
LABEL_BG = "rgba(255,255,255,.94)"

SCREEN_HEIGHT_VH = 180
# ====================

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

BLOCKS = []

def add_block(id_, left, top, width, height, kind="outer"):
    BLOCKS.append({
        "id": id_,
        "left": left,
        "top": top,
        "width": width,
        "height": height,
        "kind": kind,
    })

# ===== HEADER =====
add_block("SOCIALS",    4.0,  1.8, 22.0, 2.6, "outer")
add_block("LOGO",      27.0,  1.0, 46.0, 4.0, "outer")
add_block("LANGUAGE",   6.0,  6.0, 42.0, 3.5, "outer")
add_block("SETTINGS",  52.0,  6.0, 42.0, 3.5, "outer")
add_block("USER",       6.0, 10.6, 88.0, 3.5, "outer")

# ===== MODOS =====
add_block("CARD_PPM",       6.0, 15.8, 88.0, 6.4, "outer")
add_block("PPM_TITLE",     10.0, 16.7, 50.0, 1.3, "inner")
add_block("PPM_DESC",      10.0, 18.2, 66.0, 1.0, "inner")
add_block("PPM_BTN",       10.0, 19.7, 20.0, 1.7, "inner")

add_block("CARD_CLASSIC",   6.0, 23.2, 88.0, 6.4, "outer")
add_block("CLASSIC_TITLE", 10.0, 24.1, 56.0, 1.3, "inner")
add_block("CLASSIC_DESC",  10.0, 25.6, 68.0, 1.0, "inner")
add_block("CLASSIC_BTN",   10.0, 27.1, 20.0, 1.7, "inner")

# ===== WALLET =====
add_block("CARD_WALLET",      6.0, 30.8, 88.0, 10.0, "outer")
add_block("WALLET_TITLE",    32.0, 31.7, 36.0, 1.4, "inner")
add_block("WALLET_USD",      10.0, 34.0, 36.0, 2.5, "inner")
add_block("WALLET_POINTS",   54.0, 34.0, 36.0, 2.5, "inner")
add_block("WALLET_RECARGAR", 10.0, 37.6, 36.0, 1.8, "inner")
add_block("WALLET_CANJEAR",  54.0, 37.6, 36.0, 1.8, "inner")

# ===== POZO =====
add_block("POZO_PANEL",          6.0, 42.0, 88.0, 4.8, "outer")
add_block("POZO_TITLE",         10.0, 42.9, 40.0, 1.4, "inner")
add_block("POZO_PARTICIPANTES", 60.0, 42.9, 12.0, 1.8, "inner")
add_block("POZO_BOLSA",         76.0, 42.9, 12.0, 1.8, "inner")

# ===== RETOS =====
add_block("RETOS_PANEL",   4.5, 48.2, 91.0, 43.8, "outer")
add_block("RETOS_TITULO",  8.0, 49.0, 42.0, 1.6, "inner")

def add_reto_card(name, top):
    card_left = 6.5
    card_width = 87.0
    card_height = 8.2

    label_left = 9.5
    label_width = 18.0
    value_left = 29.5
    value_width = 58.0
    row_height = 0.9

    row_tops = [
        top + 0.55,
        top + 1.75,
        top + 2.95,
        top + 4.15,
        top + 5.35,
        top + 6.55,
    ]

    row_names = [
        "RETO",
        "HORARIO",
        "BOLSA",
        "ESTADO",
        "INGRESO_MESA",
        "ACCION",
    ]

    add_block(f"{name}_CARD", card_left, top, card_width, card_height, "outer")

    for row_name, row_top in zip(row_names, row_tops):
        add_block(f"{name}_{row_name}_LABEL", label_left, row_top, label_width, row_height, "inner")
        add_block(f"{name}_{row_name}_VALUE", value_left, row_top, value_width, row_height, "inner")

add_reto_card("RETO_01", 52.0)
add_reto_card("RETO_02", 61.0)
add_reto_card("RETO_03", 70.0)
add_reto_card("RETO_04", 79.0)

# ===== ASISTENTE =====
add_block("ASISTENTE_FLOAT", 78.0, 93.2, 16.0, 2.4, "outer")

def blocks_to_html(blocks):
    out = []
    for b in blocks:
        border = OUTER_BORDER if b["kind"] == "outer" else INNER_BORDER
        bg = OUTER_BG if b["kind"] == "outer" else INNER_BG
        label_class = "blk-label outer-label" if b["kind"] == "outer" else "blk-label inner-label"

        out.append(
            f"""
            <div class="blk"
                 style="
                    left:{b['left']}%;
                    top:{b['top']}%;
                    width:{b['width']}%;
                    height:{b['height']}%;
                    border:{border};
                    background:{bg};
                 ">
              <span class="{label_class}">{b['id']}</span>
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
      height:{SCREEN_HEIGHT_VH}%;
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
      box-sizing:border-box;
    }}

    .blk-label{{
      position:absolute;
      top:1px;
      left:1px;
      background:var(--label-bg);
      border:1px solid rgba(0,0,0,.15);
      border-radius:4px;
      padding:1px 3px;
      white-space:nowrap;
      line-height:1.0;
    }}

    .outer-label{{
      font:9px Arial, sans-serif;
      font-weight:700;
    }}

    .inner-label{{
      font:7px Arial, sans-serif;
      font-weight:400;
    }}

    #hud{{
      position:sticky;
      top:8px;
      left:8px;
      margin:8px;
      width:max-content;
      font:12px Arial, sans-serif;
      background:rgba(255,255,255,.96);
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
