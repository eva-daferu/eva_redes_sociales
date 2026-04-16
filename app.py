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
MID_COLOR = "rgba(0,0,0,0.22)"
OUTER_BORDER = "2px dashed rgba(0,0,0,.62)"
INNER_BORDER = "1.4px dashed rgba(0,0,0,.45)"
OUTER_BG = "rgba(0,0,0,.04)"
INNER_BG = "rgba(0,0,0,.02)"
LABEL_BG = "rgba(255,255,255,.95)"

SCREEN_HEIGHT_VH = 205
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

# =========================
# HEADER
# =========================
add_block("SOCIALS",     4.0,  1.8, 22.0, 2.7, "outer")
add_block("LOGO",       27.0,  1.0, 46.0, 4.1, "outer")
add_block("LANGUAGE",    6.0,  6.0, 42.0, 3.6, "outer")
add_block("SETTINGS",   52.0,  6.0, 42.0, 3.6, "outer")
add_block("USER",        6.0, 10.5, 88.0, 3.6, "outer")

# =========================
# CARDS SUPERIORES
# =========================
# Fila 1
add_block("CARD_SALDO",   6.0, 15.8, 42.0, 8.0, "outer")
add_block("SALDO_TITULO", 9.5, 17.0, 18.0, 1.2, "inner")
add_block("SALDO_VALOR",  9.5, 19.0, 18.0, 1.6, "inner")
add_block("SALDO_BTN",    9.5, 21.3, 24.0, 1.7, "inner")

add_block("CARD_PUNTOS",   52.0, 15.8, 42.0, 8.0, "outer")
add_block("PUNTOS_TITULO", 55.5, 17.0, 20.0, 1.2, "inner")
add_block("PUNTOS_VALOR",  55.5, 19.0, 16.0, 1.6, "inner")
add_block("PUNTOS_META_1", 55.5, 21.0, 24.0, 1.0, "inner")
add_block("PUNTOS_META_2", 55.5, 22.2, 24.0, 1.0, "inner")

# Fila 2
add_block("CARD_CLASSIC",      6.0, 25.4, 88.0, 6.8, "outer")
add_block("CLASSIC_TITULO",   10.0, 26.5, 28.0, 1.3, "inner")
add_block("CLASSIC_DESC_1",   10.0, 28.1, 34.0, 1.0, "inner")
add_block("CLASSIC_DESC_2",   10.0, 29.2, 28.0, 1.0, "inner")
add_block("CLASSIC_BTN",      68.0, 27.3, 18.0, 1.8, "inner")

# =========================
# MENÚ ACCIONES 2x2
# =========================
add_block("MENU_BTN_UNIRSE",       6.0, 34.0, 42.0, 4.4, "outer")
add_block("MENU_BTN_CREAR",       52.0, 34.0, 42.0, 4.4, "outer")
add_block("MENU_BTN_JUGADOR",      6.0, 39.5, 42.0, 4.4, "outer")
add_block("MENU_BTN_PRIVADA",     52.0, 39.5, 42.0, 4.4, "outer")

# =========================
# TABS HISTÓRICOS
# =========================
add_block("TAB_ACTIVAS",         6.0, 45.5, 28.0, 3.2, "outer")
add_block("TAB_ENCUENTROS",     36.0, 45.5, 28.0, 3.2, "outer")
add_block("TAB_APUESTAS",       66.0, 45.5, 28.0, 3.2, "outer")

# =========================
# PANEL PRINCIPAL
# =========================
add_block("MESAS_PANEL",         4.5, 50.0, 91.0, 73.0, "outer")
add_block("MESAS_TITULO",        8.0, 51.4, 46.0, 1.8, "inner")
add_block("MESAS_SEARCH",       58.0, 51.3, 32.0, 2.0, "inner")
add_block("MESAS_SCROLL_WRAP",   6.8, 55.0, 86.5, 65.5, "outer")

def add_mesa_card(name, top):
    # tarjeta compacta con 4 filas + CTA
    add_block(f"{name}_CARD",            8.5, top,      82.0, 12.0, "outer")
    add_block(f"{name}_TITULO",         11.0, top+0.8,  44.0, 1.2,  "inner")
    add_block(f"{name}_DEPORTE_LBL",    11.0, top+2.5,  18.0, 1.0,  "inner")
    add_block(f"{name}_DEPORTE_VAL",    31.0, top+2.5,  22.0, 1.0,  "inner")
    add_block(f"{name}_PARTIDOS_LBL",   11.0, top+4.1,  18.0, 1.0,  "inner")
    add_block(f"{name}_PARTIDOS_VAL",   31.0, top+4.1,  12.0, 1.0,  "inner")
    add_block(f"{name}_APUESTA_LBL",    11.0, top+5.7,  22.0, 1.0,  "inner")
    add_block(f"{name}_APUESTA_VAL",    35.0, top+5.7,  18.0, 1.0,  "inner")
    add_block(f"{name}_BTN",            11.0, top+8.4,  66.0, 1.8,  "inner")

add_mesa_card("MESA_01", 57.0)
add_mesa_card("MESA_02", 70.3)
add_mesa_card("MESA_03", 83.6)
add_mesa_card("MESA_04", 96.9)
add_mesa_card("MESA_05", 110.2)

# barra scroll visual del panel
add_block("MESAS_SCROLLBAR",     91.8, 56.5, 1.5, 62.0, "inner")

# =========================
# BOTÓN FLOTANTE / CHAT
# =========================
add_block("CHAT_FLOAT",          76.5, 124.5, 17.5, 2.6, "outer")

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
