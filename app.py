import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Dashboard de Redes Sociales", layout="wide", page_icon="📊")

@st.cache_data
def cargar_datos():
    youtobe_data = pd.DataFrame({
        'duracion_video': ['00:45:00', '03:39:00', '03:58:00', '00:04:53', '00:05:36', '00:00:45', '00:01:30', '00:00:49', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42'],
        'titulo': ['Amazonía al borde: el bosque que decide el futuro del planeta.', 'El costo oculto de botar comida', '¿Salvar el planeta o arriesgarlo todo? - GEOINGENIERIA SOLAR', 'Todavía decides tú Cómo las redes sociales nos manipulan en silencio.', 'El científico que más dañó al planeta... y el científico que lo detuvo.', 'Especie única en Colombia el colibrí barbudito paramuno.', 'La Llegada.', 'La transición energética y los centros de datos, qué involucra? #energialimpa #datos #tecnología', 'Lluvias históricas ponen en riesgo Cundinamarca y Antioquía. #cambioclimático #lluvia #clima', 'Una tecnología que “recicla el aire” en casa. Descubre cómo. #aerotermia #energia #energialimpa', '¿Un robot en casa? mira su impacto ambiental... hablemos de NEO The Home Robot #robot #robots', 'nuevas imágenes del cometa 3i ATLAS #3iatlas #aliens #extraterrestre #cometa #nasa', 'Una peli que te impulsa y te inspira,Talentos Ocultos. Te va a encantar #talentosocultos #peliculas', 'Ciertos cosméticos, pueden contener plomo real, un metal tóxico que afecta tu salud. #makeup', 'Todo ese calor no desaparece… termina en el océano. #clima', '¿Qué hay detrás del teflón? la pelicula Dark Waters lo revela.', 'Lo digital también contamina. Cada archivo que guardas tiene un costo #cambioclimático #basura', 'Pero la ciencia habló… y la verdad fue otra. ¿Tú qué crees que era realmente? 👽✨ #3iatlas #cometa', 'energía limpia sobre el agua, paneles solares flotantes! #panelessolares #energiasolar', 'El calor extremo ya no es futuro, está pasando. ¿Estamos preparados? #oladecalor #cambioclimático', 'Cuando la tecnología se conecta con la naturaleza 🌱 #ia #inteligenciaartificial', 'La tormenta Raymond y la "DANA" nos recuerdan que el cambio climático no da tregua. #clima', 'Innovar no debería costarle tanto al planeta 🌱 ¿Tú qué piensas? #openai #sora #sora2 #ia', 'Si el cambio empieza en lo cercano, ¿qué eliges hoy?   #cambioclimático #mercadolocal #organico', '¿comprar o reparar, qué opinas del iPhone 17, o de estas versiones? #iphone #iphone17 #consumismo', 'Sorprende que sigamos actuando como si no tuviera nada que ver con nosotros. #medioambiente #earth', 'Estamos rodeados de basura aprovechable, y lo que más sobra no es plástico, es indiferencia. #basura', '¿El problema es falta de educación o falta de interés? #cambioclimático #naturaleza #basura', 'No es una amenaza, es una oportunidad para actuar. #cambioclimático #calentamientoglobal', 'Mientras algunos países convirtieron su basura, otros aún la dejan acumular🌱 #naturaleza #sabiasque', 'Basura infinita? #cambioclimático #naturaleza #cambioclimático #co2 #ciencia', 'La selva se está quedando sin refugio. Cuando cae un árbol, no solo desaparece un paisaje.', 'La selva se está quedando sin refugio. Cuando cae un árbol, no solo desaparece un paisaje.', 'La Amazonía al borde ¿Qué crees que todavía podemos salvar?', 'Mitos del Cambio Climático. tu que opinas? 🤔', 'El costo oculto de desperdiciar comida #cambioclimático #efectoinvernadero #desperdício #comedyfilms', '¡Es momento de probar alternativas como la bici o caminar! 🚴‍♀️ #movilidadsostenible #co2', 'bloquear el sol para enfriar la tierra? #cambioclimático #medioambiente #climatechange #clima', 'Las corrientes Oceánicas podrían colapsar antes del 2055 #oceanoatlantico  #oceano #medioambiente', 'El científico que más dañó al planeta… y el científico que lo detuvo', 'CÁPSULA informativa de la semana, cuéntenme que opinas! #noticias #planetatierra #tecnología', 'qué piensas de las medidas que se están tomando, que harías tú? #noticias #santamartacolombia', '¡Hola, Soy Eva!'],
        'fecha_publicacion': ['01/10/2025', '23/09/2025', '16/09/2025', '08/09/2025', '29/08/2025', '03/12/2025', '26/11/2025', '25/11/2025', '24/11/2025', '21/11/2025', '19/11/2025', '17/11/2025', '15/11/2025', '14/11/2025', '12/11/2025', '08/11/2025', '06/11/2025', '04/11/2025', '04/11/2025', '30/10/2025', '29/10/2025', '27/10/2025', '25/10/2025', '23/10/2025', '17/10/2025', '16/10/2025', '15/10/2025', '14/10/2025', '10/10/2025', '09/10/2025', '07/10/2025', '04/10/2025', '03/10/2025', '02/10/2025', '27/09/2025', '24/09/2025', '19/09/2025', '16/09/2025', '13/09/2025', '06/09/2025', '25/08/2025', '23/08/2025', '23/08/2025'],
        'privacidad': ['Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Creado para niños'],
        'visualizaciones': [18, 22, 8, 50, 298, 37, 123, 1395, 1130, 67, 104, 2362, 103, 1373, 98, 236, 152, 1251, 57, 343, 2589, 135, 197, 274, 1476, 270, 58, 1310, 73, 567, 413, 497, 398, 1722, 142, 22651, 206, 479, 986, 2287, 87, 640, 424],
        'me_gusta': [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        'comentarios': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    })

    tiktok_data = pd.DataFrame({
        'duracion_video': ['00:44', '01:33', '', '01:29', '00:48', '00:41', '00:55', '01:18', '', '01:38', '00:51', '01:16', '00:49', '', '01:02', '01:13', '01:16', '01:01', '01:05', '00:56', '00:50', '01:18', '00:07', '00:56', '00:15', '00:43', '00:39', '00:54', '00:50', '', '00:41', '00:45', '00:53', '00:44', '00:45', '00:49', '00:46', '00:56', '00:50', '00:48'],
        'titulo': ['Hoy quiero compartir con ustedes el increíble logro de foto_sintesiss_ Juan Camilo Quintero, quien logró captar una especie única de Colombia, escondida en lo profundo de nuestro páramo A pesar de la lluvia, la neblina y todo lo que hace difícil grabar allá arriba, él aprovechó cada instante. Y gracias a ese amor por la naturaleza, hoy podemos disfrutar de unas imágenes que de verdad nos recuerdan lo maravilloso que es nuestro país. Más que reaccionar, quiero que juntos celebremos este logro y que ustedes también puedan ver la belleza que él logró registrar en un momento tan especial. . . . #barbuditoparamuno #oxypogonguerinii #colibri #frailejon #paramocolombiano #paramo #medioambiente #clima #naturaleza #fauna #colombia', 'Una peli que te volará la mente y te hará pensar diferente: La Llegada. Una historia profunda sobre comunicación, tiempo y humanidad. Imperdible. #peliculasrecomendadas #peliculas #películas #scifi #scifi🎬 #LaLlegada #Arrival #cine #pelis', 'El Cambio Climático y la Geoingeniería. ¿son lo mismo? . . . . #cambioclimatico #geoingegneria #sabiasque #diferencias #calentamiento', 'Ya tienes a tu pareja perfecta? para ti qué se debería tener en cuenta al momento de entablar una relación sentimental? . . . . . #parejas #amor #ia #cachorros #relacionestoxicas', 'La transición energética y los centros de datos, una pieza central en el mundo digital. Que involucra? . . . . #tecnologia #transition #transicionenergetica #cambioclimatico #energia', 'lluvias históricas ponen en riesgo Cundinamarca y Antioquía. cómo piensas tú qué debemos actuar? . . . #cambioclimatico #clima #lluvia #cundinamarca #colombia', 'Una tecnología que “recicla el aire” en casa. Descubre cómo. . . . . #tecnologia #casa #aerotermia #tecnologia #calefacción #calor #energia', '¿Un robot en casa? mira su impacto ambiental... hablemos de NEO The Home Robot. . . . #tecnologia #robots #robot #neothehomerobot #casa #home', '¡ALERTA! 🚨 La WMO confirma: Las inundaciones son más intensas, pero el gran desafío es que la alerta llegue a tiempo para salvar vidas. Desliza y entiende por qué fallan los sistemas. ¿Qué debe ser prioridad: tecnología o preparación local? ¡Comenta! 👇 #WMO #alerta #inundaciones #cambioclimatico #noticia', 'nuevas imágenes del cometa 3i ATLAS . . . #3iatlas #atlas #cometa #ia #alien', 'Una peli que te impulsa y te inspira: Talentos Ocultos. Te va a encantar . . . #peliculas #peli #talentosocultos #nasa', 'Ciertos cosméticos y maquillaje sin registro, pueden contener plomo real, un metal tóxico que se acumula en tu cuerpo y afecta tu salud. . . . #plomo #maquillaje #makeup #maqullajenatural #ecofriendly #crueltyfree #ecocert #vegan #wrwrd', 'Todo ese calor no desaparece… termina en el océano. . . . #clima #medioambiente #cambioclimatico #mar #oceano', 'el océano está cargando con el calor del planeta, qué piensas de todo esto? . . . #oceano #tormenta #calor #cambioclimatico #medioambiente', '¿Qué hay detrás del teflón? la pelicula Dark Waters lo revela. . . . #teflon #peliculasgratis #peliculas #pelicula #recomendaciones #recomendacionesdepeliculas #darkwaters', 'Lo digital también contamina. Cada archivo que guardas tiene un costo. . . . #basura #basuraelectronica #datosdigitales #internet #seguridad #medioambiente', 'Pero la ciencia habló… y la verdad fue otra. ¿Tú qué crees que era realmente? 👽✨ . . . #3iatlas #extraterrestres #aliens #nave #cometa #extraterrestres #ia', '🌞 Energía limpia sobre el agua Los paneles solares flotantes ya producen más electricidad que los tradicionales y, además, protegen los embalses del calentamiento y las algas. ¿Te imaginas ver esto en tu ciudad? 💧⚡ . . . . #panelessolares #panelsolar #energialimpa #represa #lagos #medioambiente #viraltiktok', 'El calor extremo ya no es futuro: está pasando. ¿Estamos preparados? . . . #oladecalor #cambioclimático #planeta #golpedecalor #incendiosforestales #clima #incendios', 'Cuando la tecnología se conecta con la naturaleza, nace la verdadera innovación 🌱 . . . #planeta #simulacion #googlehearth #incendios #incendiosforestales #deforestacion #clima #medioambiente #inteligenciaartificial #raymond #IA', 'La tormenta Raymond y el fenómeno meteorológico"DANA" nos recuerdan que el cambio climático no da tregua. . . . #raymond #DANA #cambioclimatico #medioambiente #clima #españa #mexico #tormenta #tormentatropical', 'Innovar no debería costarle tanto al planeta 🌱 ¿Tú qué piensas? . . #sora #sora2 #openai #ia #IA #openAI #stephenhawking #co2', 'Si el cambio empieza en lo cercano, ¿qué eliges hoy? . . . #comida #mercadocampesino #mercadolocal #organico #organic #colombia #campo #consumoconsciente', '¿comprar o reparar, qué opinas del iPhone 17, o de estas versiones? . . #iphone17 #iphone17promax #cambioclimatico #medioambiente #plastico #planetearth #consumoconsciente #consumismo', 'Las tormentas no sorprendieron a nadie. Lo que sorprende es que sigamos actuando como si no tuvieran nada que ver con nosotros. . . #cambioclimatico #medioambiente #plastico #planetearth #earthsong', 'Estamos rodeados de basura aprovechable, pero lo que más sobra no es plástico… es indiferencia. 👉🏼 Dale play y entiende por qué separar un envase sí importa 🌱 . . #cambioclimatico #medioambiente #basura #plastic #plastico', 'El 90% de la basura podría aprovecharse… pero la indiferencia pesa más que el plástico. La economía circular y las leyes existen, lo que falta es decisión. 👉 Mira el reel y descubre cómo cada botella y cada bolsa sí hacen la diferencia. . . #cambioclimatico #medioambiente #basura #plastic #plastico', 'La ciencia ya nos avisó, podríamos vivir el año más cálido de la historia muy pronto. No es una amenaza, es una oportunidad para actuar. Informarnos también es cuidarnos. . . #cambioclimatico #medioambiente #planetearth #co2 #planetatierra #deforestacion #basura', 'Mientras algunos países convirtieron su basura en energía y progreso, otros aún la dejan acumular. ♻️ Alemania recicla el 65%, Japón llega al 80% y Suecia casi no tiene vertederos. No es magia, es decisión colectiva. 🌱 . . #basura #cambioclimatico #medioambiente #planetearth #co2 #planetatierra #talar', 'Hoy te invito a un pequeño gran desafío, vivir 24 horas sin plásticos de un solo uso 🍃 Di no a las bolsas, botellas y pitillos desechables, y sí a los termos, las bolsas de tela y los envases reutilizables. . . . #reciclaje #plastic #termo #plastico #totebag', 'Basura infinita? ♻️ Cada año generamos más de 2 mil millones de toneladas de basura… y para 2050 será 70% más si no cambiamos. 🌍 ¿Nuestro legado? ¿Montañas de basura o un planeta limpio? 🌱 . . #basura #cambioclimatico #medioambiente #co2 #planetearth #planetatierra', 'La selva se está quedando sin refugio. Cuando cae un árbol, no solo desaparece un paisaje: el jaguar pierde territorio y el guacamayo su aire. Mira el video completo y entiende lo que está en juego. . . #amazonia #jaguar #guacamayo #tala #talar #deforestacion', 'La Amazonía está viviendo un momento decisivo. 🌿 Cada árbol que se pierde afecta el clima, los animales y a quienes vivimos lejos de ella. Pero también hay historias de esperanza: comunidades que protegen, acuerdos que funcionan y acciones que inspiran. 💚 Mira el video y cuéntame ¿Qué crees que todavía podemos salvar? . . #cambioclimatico #medioambiente #amazonia #amazonas #deforestacion #ganaderia', '3 mitos con datos reales: ya está afectando nuestra salud, el agua, los cultivos y la forma en que vivimos. 🤔 ¿Qué otro mito te gustaría que desmontemos? . . #cambioclimatico #medioambiente #co2 #mito #mitos #olasdecalor #seguridadalimentaria #reciclaje #recicla', 'El costo oculto de desperdiciar comida. El planeta paga un precio altísimo por el desperdicio de alimentos. Hambre, desigualdad y contaminación… pero también soluciones. Mira el video completo en mi canal de Youtube y Facebook . . #cambioclimatico #toogoodtogo #medioambiente#efectoinvernadero #comedyfilms #foodwaste #muckbang #hambruna', '¿Cómo nuestras acciones diarias, como el transporte y nuestra huella digital, impactan el cambio climático? 🚗💨 ¡Es momento de probar alternativas más verdes como la bici o caminar! 🚴‍♀️ #co2 #climatechange #medioambiente #movilidadsostenible #cambioclimatico', '☀️ Geoingeniería solar, ¿último salvavidas contra el cambio climático o la caja de Pandora más peligrosa de la humanidad? #cambioclimatico🌏 #medioambiente #geoingegneria #clima #sol', 'Corrientes Oceánicas El océano nos está enviando una señal, las corrientes del Atlántico podrían colapsar. Más frío en Europa, más sequías y tormentas en América y África. ¿Tú qué opinas? . . #oceano #oceanoatlantico🌊 #oceanoatlantico #cambioclimatico #medioambiente #noticiastiktok #noticia #capsulainformativa', '🧠📲 Un recorrido directo sobre cómo los algoritmos de redes sociales capturan tu atención, moldean opiniones y profundizan la polarización. ⚖️ Con un llamado claro a proteger los neuroderechos, exigir transparencia y recuperar el libre albedrío. 🎥 Video completo 👉 https://youtu.be/G28n0plg8So #Neuroderechos #Algoritmos #LibreAlbedrío #Desinformación #CámarasDeEco #EducaciónDigital #TransparenciaAlgorítmica #PrivacidadDeDatos #DemocraciaDigital #BienestarDigital #IA #CiudadaníaDigital', 'El científico que más dañó al planeta… y el que lo detuvo.'],
        'fecha_publicacion': ['03/12/2025', '28/11/2025', '27/11/2025', '26/11/2025', '25/11/2025', '24/11/2025', '21/11/2025', '19/11/2025', '18/11/2025', '17/11/2025', '15/11/2025', '14/11/2025', '12/11/2025', '10/11/2025', '08/11/2025', '06/11/2025', '04/11/2025', '01/11/2025', '29/10/2025', '28/10/2025', '27/10/2025', '25/10/2025', '23/10/2025', '17/10/2025', '16/10/2025', '15/10/2025', '14/10/2025', '10/10/2025', '09/10/2025', '08/10/2025', '07/10/2025', '04/10/2025', '01/10/2025', '27/09/2025', '23/09/2025', '19/09/2025', '16/09/2025', '12/09/2025', '10/09/2025', '05/09/2025'],
        'privacidad': ['Todo el mundo'] * 40,
        'visualizaciones': [127, 5669, 111, 179, 121, 165, 6511, 129, 1143, 5232, 1725, 276, 1437, 1293, 24000, 197, 38000, 235, 119, 21000, 12000, 2358, 192, 11000, 902, 617, 609, 599, 8788, 130, 128, 2856, 341, 274, 1204, 946, 7753, 681, 1273, 73000],
        'me_gusta': [19, 211, 3, 12, 3, 10, 121, 3, 8, 171, 83, 10, 35, 22, 1643, 11, 1894, 15, 2, 1171, 424, 135, 8, 345, 48, 43, 43, 35, 42, 2, 2, 266, 19, 12, 35, 35, 494, 42, 92, 1458],
        'comentarios': [2, 5, 0, 0, 0, 1, 1, 0, 0, 4, 3, 0, 4, 1, 22, 1, 16, 0, 0, 6, 2, 1, 0, 2, 2, 2, 1, 1, 2, 0, 0, 5, 3, 1, 1, 0, 4, 2, 0, 9]
    })
    
    for df in [youtobe_data, tiktok_data]:
        df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'], dayfirst=True, errors='coerce')
        hoy = pd.Timestamp.now()
        df['dias_desde_publicacion'] = (hoy - df['fecha_publicacion']).dt.days
        df['dias_desde_publicacion'] = df['dias_desde_publicacion'].apply(lambda x: max(x, 1))
        df['rendimiento_por_dia'] = df['visualizaciones'] / df['dias_desde_publicacion']
    
    return youtobe_data, tiktok_data

youtobe_df, tiktok_df = cargar_datos()

st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        font-size: 18px;
        font-weight: bold;
        padding: 20px;
        border-radius: 15px;
        border: none;
        transition: all 0.3s;
        margin: 5px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 10px 0;
        border: 2px solid rgba(255,255,255,0.1);
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 16px;
        opacity: 0.9;
    }
    .header {
        background: linear-gradient(90deg, #1E3A8A, #3B82F6);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .data-table {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .tab-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .css-1d391kg {padding: 2rem 1rem;}
    h1, h2, h3 {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        background-color: #f0f2f6;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3B82F6;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1>📊 DASHBOARD DE REDES SOCIALES</h1><p>Análisis de rendimiento de contenido en YouTube y TikTok</p></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    youtube_btn = st.button("🎬 YOUTUBE ANALYTICS", key="youtube", use_container_width=True)
with col2:
    tiktok_btn = st.button("📱 TIKTOK ANALYTICS", key="tiktok", use_container_width=True)
with col3:
    dashboard_btn = st.button("📈 DASHBOARD COMPARATIVO", key="dashboard", use_container_width=True)

if youtube_btn or (not youtube_btn and not tiktok_btn and not dashboard_btn):
    st.markdown('<h2>📊 ANÁLISIS DE YOUTUBE</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">TOTAL VIDEOS</div>
                <div class="metric-value">{len(youtobe_df)}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">VISUALIZACIONES TOTALES</div>
                <div class="metric-value">{youtobe_df['visualizaciones'].sum():,}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        rendimiento_promedio = youtobe_df['rendimiento_por_dia'].mean()
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">RENDIMIENTO/DÍA</div>
                <div class="metric-value">{rendimiento_promedio:.1f}</div>
                <div class="metric-label">visualizaciones por día</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">ENGAGEMENT RATE</div>
                <div class="metric-value">{((youtobe_df['me_gusta'].sum() + youtobe_df['comentarios'].sum()) / youtobe_df['visualizaciones'].sum() * 100):.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 GRÁFICAS", "📊 MÉTRICAS DETALLADAS", "🏆 TOP CONTENIDO"])
    
    with tab1:
        fig = make_subplots(rows=2, cols=2, 
                           subplot_titles=('📈 Visualizaciones por Fecha', '❤️ Me Gusta vs Visualizaciones', 
                                         '📊 Distribución de Visualizaciones', '🏅 Top 5 Videos Más Vistos'),
                           specs=[[{'secondary_y': True}, {}], [{}, {}]])
        
        fig.add_trace(go.Scatter(x=youtobe_df['fecha_publicacion'], y=youtobe_df['visualizaciones'], 
                               mode='lines+markers', name='Visualizaciones', line=dict(color='#FF0000', width=3)),
                     row=1, col=1)
        fig.add_trace(go.Scatter(x=youtobe_df['fecha_publicacion'], y=youtobe_df['me_gusta'], 
                               mode='lines+markers', name='Me Gusta', line=dict(color='#FF6B35', width=2)),
                     row=1, col=1, secondary_y=True)
        
        fig.add_trace(go.Scatter(x=youtobe_df['visualizaciones'], y=youtobe_df['me_gusta'], 
                               mode='markers', marker=dict(size=12, color='#00C851', opacity=0.7),
                               text=youtobe_df['titulo'].str[:50], name='Relación'),
                     row=1, col=2)
        
        fig.add_trace(go.Histogram(x=youtobe_df['visualizaciones'], nbinsx=20, 
                                  name='Distribución', marker_color='#9C27B0', opacity=0.7),
                     row=2, col=1)
        
        top_videos = youtobe_df.nlargest(5, 'visualizaciones')
        fig.add_trace(go.Bar(x=top_videos['titulo'].str[:30] + '...', 
                            y=top_videos['visualizaciones'], 
                            name='Top Videos', 
                            marker_color=['#FF5252', '#FF4081', '#E040FB', '#7C4DFF', '#536DFE']),
                     row=2, col=2)
        
        fig.update_layout(height=700, showlegend=True, template='plotly_white',
                         plot_bgcolor='rgba(240,242,246,0.8)')
        fig.update_xaxes(title_text="Fecha", row=1, col=1)
        fig.update_yaxes(title_text="Visualizaciones", row=1, col=1)
        fig.update_yaxes(title_text="Me Gusta", secondary_y=True, row=1, col=1)
        fig.update_xaxes(title_text="Visualizaciones", row=1, col=2)
        fig.update_yaxes(title_text="Me Gusta", row=1, col=2)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📅 Rendimiento por Días desde Publicación")
            rendimiento_dias = youtobe_df.groupby('dias_desde_publicacion')['rendimiento_por_dia'].mean().reset_index()
            fig_dias = go.Figure(data=go.Scatter(x=rendimiento_dias['dias_desde_publicacion'], 
                                                y=rendimiento_dias['rendimiento_por_dia'],
                                                mode='lines+markers',
                                                line=dict(color='#00BCD4', width=3),
                                                marker=dict(size=10)))
            fig_dias.update_layout(title="Rendimiento vs Días desde Publicación",
                                  xaxis_title="Días desde Publicación",
                                  yaxis_title="Rendimiento por Día (visualizaciones/día)",
                                  template='plotly_white')
            st.plotly_chart(fig_dias, use_container_width=True)
        
        with col2:
            st.markdown("### 🔥 Top 10 Videos por Rendimiento/Día")
            top_rendimiento = youtobe_df.nlargest(10, 'rendimiento_por_dia')[['titulo', 'rendimiento_por_dia', 'dias_desde_publicacion', 'visualizaciones']]
            fig_top = go.Figure(data=[go.Bar(x=top_rendimiento['titulo'].str[:30] + '...',
                                            y=top_rendimiento['rendimiento_por_dia'],
                                            text=top_rendimiento['rendimiento_por_dia'].round(1),
                                            textposition='auto',
                                            marker_color='#4CAF50')])
            fig_top.update_layout(title="Top 10 Videos por Rendimiento Diario",
                                 xaxis_title="Video",
                                 yaxis_title="Rendimiento por Día",
                                 xaxis_tickangle=-45,
                                 template='plotly_white')
            st.plotly_chart(fig_top, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🥇 Top Videos por Visualizaciones")
            top_visualizaciones = youtobe_df.nlargest(10, 'visualizaciones')[['titulo', 'visualizaciones', 'me_gusta', 'comentarios', 'rendimiento_por_dia']]
            st.dataframe(top_visualizaciones.style.background_gradient(subset=['visualizaciones'], cmap='Reds'), height=400)
        
        with col2:
            st.markdown("### 📈 Métricas de Rendimiento")
            st.metric("Video con Mayor Rendimiento/Día", 
                     f"{youtobe_df.loc[youtobe_df['rendimiento_por_dia'].idxmax(), 'rendimiento_por_dia']:.1f}",
                     delta=f"{youtobe_df['rendimiento_por_dia'].max() - youtobe_df['rendimiento_por_dia'].mean():.1f}")
            st.metric("Video Más Reciente", 
                     youtobe_df.loc[youtobe_df['fecha_publicacion'].idxmax(), 'titulo'][:50] + "...")
            st.metric("Visualizaciones Promedio por Video", f"{youtobe_df['visualizaciones'].mean():.0f}")
    
    with st.expander("📋 VER TODOS LOS DATOS DE YOUTUBE", expanded=False):
        st.dataframe(youtobe_df, use_container_width=True)

elif tiktok_btn:
    st.markdown('<h2>📊 ANÁLISIS DE TIKTOK</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">TOTAL VIDEOS</div>
                <div class="metric-value">{len(tiktok_df)}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">VISUALIZACIONES TOTALES</div>
                <div class="metric-value">{tiktok_df['visualizaciones'].sum():,}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        rendimiento_promedio = tiktok_df['rendimiento_por_dia'].mean()
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">RENDIMIENTO/DÍA</div>
                <div class="metric-value">{rendimiento_promedio:.1f}</div>
                <div class="metric-label">visualizaciones por día</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">ENGAGEMENT RATE</div>
                <div class="metric-value">{((tiktok_df['me_gusta'].sum() + tiktok_df['comentarios'].sum()) / tiktok_df['visualizaciones'].sum() * 100):.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 GRÁFICAS", "🔥 MÉTRICAS TIKTOK", "🏆 TOP VIRALES"])
    
    with tab1:
        fig = make_subplots(rows=2, cols=2, 
                           subplot_titles=('📈 Engagement por Fecha', '❤️ Visualizaciones vs Me Gusta', 
                                         '🎭 Heatmap de Interacción', '🏅 Top 5 Videos TikTok'),
                           specs=[[{'secondary_y': True}, {}], [{}, {}]])
        
        fig.add_trace(go.Scatter(x=tiktok_df['fecha_publicacion'], y=tiktok_df['visualizaciones'], 
                               mode='lines+markers', name='Visualizaciones', line=dict(color='#00F5FF', width=3)),
                     row=1, col=1)
        fig.add_trace(go.Scatter(x=tiktok_df['fecha_publicacion'], y=tiktok_df['me_gusta'], 
                               mode='lines+markers', name='Me Gusta', line=dict(color='#FF00FF', width=2)),
                     row=1, col=1, secondary_y=True)
        
        fig.add_trace(go.Scatter(x=tiktok_df['visualizaciones'], y=tiktok_df['me_gusta'], 
                               mode='markers', 
                               marker=dict(size=tiktok_df['comentarios']*5 + 10, 
                                         color=tiktok_df['comentarios'], 
                                         colorscale='Viridis',
                                         showscale=True,
                                         colorbar=dict(title="Comentarios")),
                               text=tiktok_df['titulo'].str[:50],
                               name='Engagement'),
                     row=1, col=2)
        
        engagement = tiktok_df[['visualizaciones', 'me_gusta', 'comentarios']].corr()
        fig.add_trace(go.Heatmap(z=engagement.values, 
                                x=engagement.columns, 
                                y=engagement.columns, 
                                colorscale='RdBu',
                                text=engagement.values.round(2),
                                texttemplate='%{text}',
                                textfont={"size": 12}),
                     row=2, col=1)
        
        top_tiktok = tiktok_df.nlargest(5, 'visualizaciones')
        fig.add_trace(go.Bar(x=top_tiktok['titulo'].str[:30] + '...', 
                            y=top_tiktok['visualizaciones'], 
                            name='Top Videos',
                            marker_color=['#00E5FF', '#18FFFF', '#64FFDA', '#69F0AE', '#B2FF59']),
                     row=2, col=2)
        
        fig.update_layout(height=700, showlegend=True, template='plotly_dark',
                         plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(title_text="Fecha", row=1, col=1)
        fig.update_yaxes(title_text="Visualizaciones", row=1, col=1)
        fig.update_yaxes(title_text="Me Gusta", secondary_y=True, row=1, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📊 Rendimiento por Días desde Publicación")
            rendimiento_dias = tiktok_df.groupby('dias_desde_publicacion')['rendimiento_por_dia'].mean().reset_index()
            fig_dias = go.Figure(data=go.Scatter(x=rendimiento_dias['dias_desde_publicacion'], 
                                                y=rendimiento_dias['rendimiento_por_dia'],
                                                mode='lines+markers',
                                                line=dict(color='#FF4081', width=3),
                                                marker=dict(size=10, symbol='diamond')))
            fig_dias.update_layout(title="Rendimiento vs Días desde Publicación",
                                  xaxis_title="Días desde Publicación",
                                  yaxis_title="Rendimiento por Día",
                                  template='plotly_white')
            st.plotly_chart(fig_dias, use_container_width=True)
        
        with col2:
            st.markdown("### 🚀 Top 10 Videos por Rendimiento/Día")
            top_rendimiento = tiktok_df.nlargest(10, 'rendimiento_por_dia')[['titulo', 'rendimiento_por_dia', 'dias_desde_publicacion', 'visualizaciones']]
            fig_top = go.Figure(data=[go.Bar(x=top_rendimiento['titulo'].str[:30] + '...',
                                            y=top_rendimiento['rendimiento_por_dia'],
                                            text=top_rendimiento['rendimiento_por_dia'].round(1),
                                            textposition='auto',
                                            marker_color='linear-gradient(90deg, #FF4081, #F50057)')])
            fig_top.update_layout(title="Top 10 Videos por Rendimiento Diario",
                                 xaxis_title="Video",
                                 yaxis_title="Rendimiento por Día",
                                 xaxis_tickangle=-45,
                                 template='plotly_white')
            st.plotly_chart(fig_top, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🥇 Top Videos por Visualizaciones")
            top_visualizaciones = tiktok_df.nlargest(10, 'visualizaciones')[['titulo', 'visualizaciones', 'me_gusta', 'comentarios', 'rendimiento_por_dia']]
            st.dataframe(top_visualizaciones.style.background_gradient(subset=['visualizaciones'], cmap='Blues'), height=400)
        
        with col2:
            st.markdown("### 📈 Métricas de Rendimiento TikTok")
            st.metric("Video con Mayor Rendimiento/Día", 
                     f"{tiktok_df.loc[tiktok_df['rendimiento_por_dia'].idxmax(), 'rendimiento_por_dia']:.1f}",
                     delta=f"{tiktok_df['rendimiento_por_dia'].max() - tiktok_df['rendimiento_por_dia'].mean():.1f}")
            st.metric("Video Más Viral", 
                     tiktok_df.loc[tiktok_df['visualizaciones'].idxmax(), 'titulo'][:50] + "...")
            st.metric("Tasa de Engagement Promedio", f"{tiktok_df['me_gusta'].mean() / tiktok_df['visualizaciones'].mean() * 100:.2f}%")
    
    with st.expander("📋 VER TODOS LOS DATOS DE TIKTOK", expanded=False):
        st.dataframe(tiktok_df, use_container_width=True)

elif dashboard_btn:
    st.markdown('<h2>📈 DASHBOARD COMPARATIVO</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">VIDEOS YOUTUBE</div>
                <div class="metric-value">{len(youtobe_df)}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">VIDEOS TIKTOK</div>
                <div class="metric-value">{len(tiktok_df)}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">TOTAL VISUALIZACIONES</div>
                <div class="metric-value">{youtobe_df['visualizaciones'].sum() + tiktok_df['visualizaciones'].sum():,}</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        rendimiento_total = (youtobe_df['rendimiento_por_dia'].mean() + tiktok_df['rendimiento_por_dia'].mean()) / 2
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">RENDIMIENTO PROMEDIO/DÍA</div>
                <div class="metric-value">{rendimiento_total:.1f}</div>
                <div class="metric-label">ambas plataformas</div>
            </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 COMPARATIVA GRÁFICA", "📈 MÉTRICAS COMPARATIVAS", "🏆 TOP GLOBAL"])
    
    with tab1:
        fig = make_subplots(rows=2, cols=2, 
                           subplot_titles=('📊 Comparativa Visualizaciones', '❤️ Comparativa Me Gusta', 
                                         '📈 Distribución Engagement', '🚀 Evolución Combinada'),
                           specs=[[{}, {}], [{}, {}]])
        
        fig.add_trace(go.Bar(x=['YouTube', 'TikTok'], 
                            y=[youtobe_df['visualizaciones'].mean(), tiktok_df['visualizaciones'].mean()], 
                            name='Promedio Visualizaciones', 
                            marker_color=['#FF0000', '#00F5FF'],
                            text=[f"{youtobe_df['visualizaciones'].mean():.0f}", f"{tiktok_df['visualizaciones'].mean():.0f}"],
                            textposition='auto'),
                     row=1, col=1)
        
        fig.add_trace(go.Bar(x=['YouTube', 'TikTok'], 
                            y=[youtobe_df['me_gusta'].mean(), tiktok_df['me_gusta'].mean()], 
                            name='Promedio Me Gusta', 
                            marker_color=['#FF6B35', '#FF00FF'],
                            text=[f"{youtobe_df['me_gusta'].mean():.0f}", f"{tiktok_df['me_gusta'].mean():.0f}"],
                            textposition='auto'),
                     row=1, col=2)
        
        youtube_engagement = youtobe_df['me_gusta'].sum() + youtobe_df['comentarios'].sum()
        tiktok_engagement = tiktok_df['me_gusta'].sum() + tiktok_df['comentarios'].sum()
        fig.add_trace(go.Pie(labels=['YouTube', 'TikTok'], 
                            values=[youtube_engagement, tiktok_engagement], 
                            hole=0.4,
                            marker=dict(colors=['#FF0000', '#00F5FF']),
                            textinfo='label+percent'),
                     row=2, col=1)
        
        fig.add_trace(go.Scatter(x=youtobe_df['fecha_publicacion'], 
                                y=youtobe_df['rendimiento_por_dia'], 
                                mode='lines', 
                                name='YouTube', 
                                line=dict(color='#FF0000', width=3)),
                     row=2, col=2)
        fig.add_trace(go.Scatter(x=tiktok_df['fecha_publicacion'], 
                                y=tiktok_df['rendimiento_por_dia'], 
                                mode='lines', 
                                name='TikTok', 
                                line=dict(color='#00F5FF', width=3)),
                     row=2, col=2)
        
        fig.update_layout(height=700, showlegend=True, template='plotly_white')
        fig.update_yaxes(title_text="Promedio", row=1, col=1)
        fig.update_yaxes(title_text="Promedio", row=1, col=2)
        fig.update_yaxes(title_text="Rendimiento por Día", row=2, col=2)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Métricas Comparativas")
            comparativa_data = pd.DataFrame({
                'Métrica': ['Total Videos', 'Total Visualizaciones', 'Promedio Visualizaciones', 
                          'Promedio Me Gusta', 'Promedio Comentarios', 'Rendimiento/Día'],
                'YouTube': [len(youtobe_df), youtobe_df['visualizaciones'].sum(), 
                          youtobe_df['visualizaciones'].mean(), youtobe_df['me_gusta'].mean(),
                          youtobe_df['comentarios'].mean(), youtobe_df['rendimiento_por_dia'].mean()],
                'TikTok': [len(tiktok_df), tiktok_df['visualizaciones'].sum(), 
                          tiktok_df['visualizaciones'].mean(), tiktok_df['me_gusta'].mean(),
                          tiktok_df['comentarios'].mean(), tiktok_df['rendimiento_por_dia'].mean()]
            })
            
            st.dataframe(comparativa_data.style.format({
                'YouTube': '{:,.1f}',
                'TikTok': '{:,.1f}'
            }).background_gradient(subset=['YouTube', 'TikTok'], cmap='YlOrRd'))
        
        with col2:
            st.markdown("### 📈 Análisis de Rendimiento")
            
            mejor_rendimiento_youtube = youtobe_df.loc[youtobe_df['rendimiento_por_dia'].idxmax()]
            mejor_rendimiento_tiktok = tiktok_df.loc[tiktok_df['rendimiento_por_dia'].idxmax()]
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("🎬 Mejor YouTube", 
                         f"{mejor_rendimiento_youtube['rendimiento_por_dia']:.1f}",
                         delta="rendimiento/día")
                st.caption(f"Video: {mejor_rendimiento_youtube['titulo'][:40]}...")
            
            with col_b:
                st.metric("📱 Mejor TikTok", 
                         f"{mejor_rendimiento_tiktok['rendimiento_por_dia']:.1f}",
                         delta="rendimiento/día")
                st.caption(f"Video: {mejor_rendimiento_tiktok['titulo'][:40]}...")
            
            st.markdown("---")
            
            total_visualizaciones = youtobe_df['visualizaciones'].sum() + tiktok_df['visualizaciones'].sum()
            youtube_percent = (youtobe_df['visualizaciones'].sum() / total_visualizaciones) * 100
            tiktok_percent = (tiktok_df['visualizaciones'].sum() / total_visualizaciones) * 100
            
            st.markdown(f"### 📊 Distribución de Visualizaciones")
            st.markdown(f"**YouTube:** {youtube_percent:.1f}% ({youtobe_df['visualizaciones'].sum():,})")
            st.progress(youtube_percent / 100)
            st.markdown(f"**TikTok:** {tiktok_percent:.1f}% ({tiktok_df['visualizaciones'].sum():,})")
            st.progress(tiktok_percent / 100)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🥇 Top 5 YouTube")
            top_youtube = youtobe_df.nlargest(5, 'visualizaciones')[['titulo', 'visualizaciones', 'me_gusta', 'comentarios', 'rendimiento_por_dia']]
            for i, row in top_youtube.iterrows():
                with st.container():
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #FFE0E0, #FFFFFF); padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #FF0000;">
                            <strong>#{top_youtube.index.get_loc(i)+1} {row['titulo'][:50]}...</strong><br>
                            👁️ {row['visualizaciones']:,} | ❤️ {row['me_gusta']} | 💬 {row['comentarios']}<br>
                            ⚡ Rendimiento/día: {row['rendimiento_por_dia']:.1f}
                        </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🥇 Top 5 TikTok")
            top_tiktok = tiktok_df.nlargest(5, 'visualizaciones')[['titulo', 'visualizaciones', 'me_gusta', 'comentarios', 'rendimiento_por_dia']]
            for i, row in top_tiktok.iterrows():
                with st.container():
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #E0F7FF, #FFFFFF); padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #00F5FF;">
                            <strong>#{top_tiktok.index.get_loc(i)+1} {row['titulo'][:50]}...</strong><br>
                            👁️ {row['visualizaciones']:,} | ❤️ {row['me_gusta']} | 💬 {row['comentarios']}<br>
                            ⚡ Rendimiento/día: {row['rendimiento_por_dia']:.1f}
                        </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 🏆 Video con Mayor Rendimiento Global")
        max_rendimiento_global = max(youtobe_df['rendimiento_por_dia'].max(), tiktok_df['rendimiento_por_dia'].max())
        
        if youtobe_df['rendimiento_por_dia'].max() > tiktok_df['rendimiento_por_dia'].max():
            mejor_video = youtobe_df.loc[youtobe_df['rendimiento_por_dia'].idxmax()]
            plataforma = "🎬 YouTube"
            color = "#FF0000"
        else:
            mejor_video = tiktok_df.loc[tiktok_df['rendimiento_por_dia'].idxmax()]
            plataforma = "📱 TikTok"
            color = "#00F5FF"
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}20, #FFFFFF); padding: 25px; border-radius: 15px; margin: 20px 0; border: 3px solid {color}; text-align: center;">
                <h3>🏆 CAMPEÓN DE RENDIMIENTO</h3>
                <h4>{plataforma}</h4>
                <p><strong>{mejor_video['titulo'][:100]}...</strong></p>
                <div style="display: flex; justify-content: center; gap: 30px; margin: 20px 0;">
                    <div>
                        <div style="font-size: 24px; font-weight: bold; color: {color};">{mejor_video['rendimiento_por_dia']:.1f}</div>
                        <div>Rendimiento/día</div>
                    </div>
                    <div>
                        <div style="font-size: 24px; font-weight: bold; color: {color};">{mejor_video['visualizaciones']:,}</div>
                        <div>Visualizaciones</div>
                    </div>
                    <div>
                        <div style="font-size: 24px; font-weight: bold; color: {color};">{mejor_video['me_gusta']}</div>
                        <div>Me Gusta</div>
                    </div>
                </div>
                <p>Publicado hace {mejor_video['dias_desde_publicacion']} días</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666; padding: 20px;'>📊 Dashboard de Análisis de Redes Sociales | Actualizado automáticamente</div>", unsafe_allow_html=True)
