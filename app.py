import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Social Media Dashboard", layout="wide", page_icon="📊")

@st.cache_data
def cargar_datos():
    youtobe_data = pd.DataFrame({
        'duracion_video': ['00:45:00', '03:39:00', '03:58:00', '00:04:53', '00:05:36', '00:00:45', '00:01:30', '00:00:49', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42', '00:00:42'],
        'titulo': ['Amazonía al borde: el bosque que decide el futuro del planeta.', 'El costo oculto de botar comida', '¿Salvar el planeta o arriesgarlo todo? - GEOINGENIERIA SOLAR', 'Todavía decides tú Cómo las redes sociales nos manipulan en silencio.', 'El científico que más dañó al planeta... y el científico que lo detuvo.', 'Especie única en Colombia el colibrí barbudito paramuno.', 'La Llegada.', 'La transición energética y los centros de datos, qué involucra? #energialimpa #datos #tecnología', 'Lluvias históricas ponen en riesgo Cundinamarca y Antioquía. #cambioclimático #lluvia #clima', 'Una tecnología que "recicla el aire" en casa. Descubre cómo. #aerotermia #energia #energialimpa', '¿Un robot en casa? mira su impacto ambiental... hablemos de NEO The Home Robot #robot #robots', 'nuevas imágenes del cometa 3i ATLAS #3iatlas #aliens #extraterrestre #cometa #nasa', 'Una peli que te impulsa y te inspira,Talentos Ocultos. Te va a encantar #talentosocultos #peliculas', 'Ciertos cosméticos, pueden contener plomo real, un metal tóxico que afecta tu salud. #makeup', 'Todo ese calor no desaparece… termina en el océano. #clima', '¿Qué hay detrás del teflón? la pelicula Dark Waters lo revela.', 'Lo digital también contamina. Cada archivo que guardas tiene un costo #cambioclimático #basura', 'Pero la ciencia habló… y la verdad fue otra. ¿Tú qué crees que era realmente? 👽✨ #3iatlas #cometa', 'energía limpia sobre el agua, paneles solares flotantes! #panelessolares #energiasolar', 'El calor extremo ya no es futuro, está pasando. ¿Estamos preparados? #oladecalor #cambioclimático', 'Cuando la tecnología se conecta con la naturaleza 🌱 #ia #inteligenciaartificial', 'La tormenta Raymond y la "DANA" nos recuerdan que el cambio climático no da tregua. #clima', 'Innovar no debería costarle tanto al planeta 🌱 ¿Tú qué piensas? #openai #sora #sora2 #ia', 'Si el cambio empieza en lo cercano, ¿qué eliges hoy?   #cambioclimático #mercadolocal #organico', '¿comprar o reparar, qué opinas del iPhone 17, o de estas versiones? #iphone #iphone17 #consumismo', 'Sorprende que sigamos actuando como si no tuviera nada que ver con nosotros. #medioambiente #earth', 'Estamos rodeados de basura aprovechable, y lo que más sobra no es plástico, es indiferencia. #basura', '¿El problema es falta de educación o falta de interés? #cambioclimático #naturaleza #basura', 'No es una amenaza, es una oportunidad para actuar. #cambioclimático #calentamientoglobal', 'Mientras algunos países convirtieron su basura, otros aún la dejan acumular🌱 #naturaleza #sabiasque', 'Basura infinita? #cambioclimático #naturaleza #cambioclimático #co2 #ciencia', 'La selva se está quedando sin refugio. Cuando cae un árbol, no solo desaparece un paisaje.', 'La selva se está quedando sin refugio. Cuando cae un árbol, no solo desaparece un paisaje.', 'La Amazonía al borde ¿Qué crees que todavía podemos salvar?', 'Mitos del Cambio Climático. tu que opinas? 🤔', 'El costo oculto de desperdiciar comida #cambioclimático #efectoinvernadero #desperdício #comedyfilms', '¡Es momento de probar alternativas como la bici o caminar! 🚴‍♀️ #movilidadsostenible #co2', 'bloquear el sol para enfriar la tierra? #cambioclimático #medioambiente #climatechange #clima', 'Las corrientes Oceánicas podrían colapsar antes del 2055 #oceanoatlantico  #oceano #medioambiente', 'El científico que más dañó al planeta… y el científico que lo detuvo', 'CÁPSULA informativa de la semana, cuéntenme que opinas! #noticias #planetatierra #tecnología', 'qué piensas de las medidas que se están tomando, que harías tú? #noticias #santamartacolombia', '¡Hola, Soy Eva!'],
        'fecha_publicacion': ['01/10/2025', '23/09/2025', '16/09/2025', '08/09/2025', '29/08/2025', '03/12/2025', '26/11/2025', '25/11/2025', '24/11/2025', '21/11/2025', '19/11/2025', '17/11/2025', '15/11/2025', '14/11/2025', '12/11/2025', '08/11/2025', '06/11/2025', '04/11/2025', '04/11/2025', '30/10/2025', '29/10/2025', '27/10/2025', '25/10/2025', '23/10/2025', '17/10/2025', '16/10/2025', '15/10/2025', '14/10/2025', '10/10/2025', '09/10/2025', '07/10/2025', '04/10/2025', '03/10/2025', '02/10/2025', '27/09/2025', '24/09/2025', '19/09/2025', '16/09/2025', '13/09/2025', '06/09/2025', '25/08/2025', '23/08/2025', '23/08/2025'],
        'privacidad': ['Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Publicado', 'Creado para niños'],
        'visualizaciones': [18, 22, 8, 50, 298, 37, 123, 1395, 1130, 67, 104, 2362, 103, 1373, 98, 236, 152, 1251, 57, 343, 2589, 135, 197, 274, 1476, 270, 58, 1310, 73, 567, 413, 497, 398, 1722, 142, 22651, 206, 479, 986, 2287, 87, 640, 424],
        'me_gusta': [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        'comentarios': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    })

    tiktok_data = pd.DataFrame({
        'duracion_video': ['00:44', '01:33', '', '01:29', '00:48', '00:41', '00:55', '01:18', '', '01:38', '00:51', '01:16', '00:49', '', '01:02', '01:13', '01:16', '01:01', '01:05', '00:56', '00:50', '01:18', '00:07', '00:56', '00:15', '00:43', '00:39', '00:54', '00:50', '', '00:41', '00:45', '00:53', '00:44', '00:45', '00:49', '00:46', '00:56', '00:50', '00:48'],
        'titulo': ['Hoy quiero compartir con ustedes el increíble logro de foto_sintesiss_ Juan Camilo Quintero, quien logró captar una especie única de Colombia, escondida en lo profundo de nuestro páramo A pesar de la lluvia, la neblina y todo lo que hace difícil grabar allá arriba, él aprovechó cada instante. Y gracias a ese amor por la naturaleza, hoy podemos disfrutar de unas imágenes que de verdad nos recuerdan lo maravilloso que es nuestro país. Más que reaccionar, quiero que juntos celebremos este logro y que ustedes también puedan ver la belleza que él logró registrar en un momento tan especial. . . . #barbuditoparamuno #oxypogonguerinii #colibri #frailejon #paramocolombiano #paramo #medioambiente #clima #naturaleza #fauna #colombia', 'Una peli que te volará la mente y te hará pensar diferente: La Llegada. Una historia profunda sobre comunicación, tiempo y humanidad. Imperdible. #peliculasrecomendadas #peliculas #películas #scifi #scifi🎬 #LaLlegada #Arrival #cine #pelis', 'El Cambio Climático y la Geoingeniería. ¿son lo mismo? . . . . #cambioclimatico #geoingegneria #sabiasque #diferencias #calentamiento', 'Ya tienes a tu pareja perfecta? para ti qué se debería tener en cuenta al momento de entablar una relación sentimental? . . . . . #parejas #amor #ia #cachorros #relacionestoxicas', 'La transición energética y los centros de datos, una pieza central en el mundo digital. Que involucra? . . . . #tecnologia #transition #transicionenergetica #cambioclimatico #energia', 'lluvias históricas ponen en riesgo Cundinamarca y Antioquía. cómo piensas tú qué debemos actuar? . . . #cambioclimatico #clima #lluvia #cundinamarca #colombia', 'Una tecnología que "recicla el aire" en casa. Descubre cómo. . . . . #tecnologia #casa #aerotermia #tecnologia #calefacción #calor #energia', '¿Un robot en casa? mira su impacto ambiental... hablemos de NEO The Home Robot. . . . #tecnologia #robots #robot #neothehomerobot #casa #home', '¡ALERTA! 🚨 La WMO confirma: Las inundaciones son más intensas, pero el gran desafío es que la alerta llegue a tiempo para salvar vidas. Desliza y entiende por qué fallan los sistemas. ¿Qué debe ser prioridad: tecnología o preparación local? ¡Comenta! 👇 #WMO #alerta #inundaciones #cambioclimatico #noticia', 'nuevas imágenes del cometa 3i ATLAS . . . #3iatlas #atlas #cometa #ia #alien', 'Una peli que te impulsa y te inspira: Talentos Ocultos. Te va a encantar . . . #peliculas #peli #talentosocultos #nasa', 'Ciertos cosméticos y maquillaje sin registro, pueden contener plomo real, un metal tóxico que se acumula en tu cuerpo y afecta tu salud. . . . #plomo #maquillaje #makeup #maqullajenatural #ecofriendly #crueltyfree #ecocert #vegan #wrwrd', 'Todo ese calor no desaparece… termina en el océano. . . . #clima #medioambiente #cambioclimatico #mar #oceano', 'el océano está cargando con el calor del planeta, qué piensas de todo esto? . . . #oceano #tormenta #calor #cambioclimatico #medioambiente', '¿Qué hay detrás del teflón? la pelicula Dark Waters lo revela. . . . #teflon #peliculasgratis #peliculas #pelicula #recomendaciones #recomendacionesdepeliculas #darkwaters', 'Lo digital también contamina. Cada archivo que guardas tiene un costo. . . . #basura #basuraelectronica #datosdigitales #internet #seguridad #medioambiente', 'Pero la ciencia habló… y la verdad fue otra. ¿Tú qué crees que era realmente? 👽✨ . . . #3iatlas #extraterrestres #aliens #nave #cometa #extraterrestres #ia', '🌞 Energía limpia sobre el agua Los paneles solares flotantes ya producen más electricidad que los tradicionales y, además, protegen los embalses del calentamiento y las algas. ¿Te imaginas ver esto en tu ciudad? 💧⚡ . . . . #panelessolares #panelsolar #energialimpa #represa #lagos #medioambiente #viraltiktok', 'El calor extremo ya no es futuro: está pasando. ¿Estamos preparados? . . . #oladecalor #cambioclimático #planeta #golpedecalor #incendiosforestales #clima #incendios', 'Cuando la tecnología se conecta con la naturaleza, nace la verdadera innovación 🌱 . . . #planeta #simulacion #googlehearth #incendios #incendiosforestales #deforestacion #clima #medioambiente #inteligenciaartificial #raymond #IA', 'La tormenta Raymond y el fenómeno meteorológico"DANA" nos recuerdan que el cambio climático no da tregua. . . . #raymond #DANA #cambioclimatico #medioambiente #clima #españa #mexico #tormenta #tormentatropical', 'Innovar no debería costarle tanto al planeta 🌱 ¿Tú qué piensas? . . #sora #sora2 #openai #ia #IA #openAI #stephenhawking #co2', 'Si el cambio empieza en lo cercano, ¿qué eliges hoy? . . . #comida #mercadocampesino #mercadolocal #organico #organic #colombia #campo #consumoconsciente', '¿comprar o reparar, qué opinas del iPhone 17, o de estas versiones? . . #iphone17 #iphone17promax #cambioclimatico #medioambiente #plastico #planetearth #consumoconsciente #consumismo', 'Las tormentas no sorprendieron a nadie. Lo que sorprende es que sigamos actuando como si no tuvieran nada que ver con nosotros. . . #cambioclimatico #medioambiente #plastico #planetearth #earthsong', 'Estamos rodeados de basura aprovechable, pero lo que más sobra no es plástico… es indiferencia. 👉🏼 Dale play y entiende por qué separar un envase sí importa 🌱 . . #cambioclimatico #medioambiente #basura #plastic #plastico', 'El 90% de la basura podría aprovecharse… pero la indiferencia pesa más que el plástico. La economía circular y las leyes existen, lo que falta es decisión. 👉 Mira el reel y descubre cómo cada botella y cada bolsa sí hacen la diferencia. . . #cambioclimatico #medioambiente #basura #plastic #plastico', 'La ciencia ya nos avisó, podríamos vivir el año más cálido de la historia muy pronto. No es una amenaza, es una oportunidad para actuar. Informarnos también es cuidarnos. . . #cambioclimatico #medioambiente #planetearth #co2 #planetatierra #deforestacion #basura', 'Mientras algunos países convirtieron su basura en energía y progreso, otros aún la dejan acumular. ♻️ Alemania recicla el 65%, Japón llega al 80% y Suecia casi no tiene vertederos. No es magia, es decisión colectiva. 🌱 . . #basura #cambioclimatico #medioambiente #planetearth #co2 #planetatierra #talar', 'Hoy te invito a un pequeño gran desafío, vivir 24 horas sin plásticos de un solo uso 🍃 Di no a las bolsas, botellas y pitillos desechables, y sí a los termos, las bolsas de tela y los envases reutilizables. . . . #reciclaje #plastic #termo #plastico #totebag', 'Basura infinita? ♻️ Cada año generamos más de 2 mil millones de toneladas de basura… y para 2050 será 70% más si no cambiamos. 🌍 ¿Nuestro legado? ¿Montañas de basura o un planeta limpio? 🌱 . . #basura #cambioclimatico #medioambiente #co2 #planetearth #planetatierra', 'La selva se está quedando sin refugio. Cuando cae un árbol, no solo desaparece un paisaje: el jaguar pierde territorio y el guacamayo su aire. Mira el video completo y entiende lo que está en juego. . . #amazonia #jaguar #guacamayo #tala #talar #deforestacion', 'La Amazonía está viviendo un momento decisivo. 🌿 Cada árbol que se pierde afecta el clima, los animales y a quienes vivimos lejos de ella. Pero también hay historias de esperanza: comunidades que protegen, acuerdos que funcionan y acciones que inspiran. 💚 Mira el video y cuéntame ¿Qué crees que todavía podemos salvar? . . #cambioclimatico #medioambiente #amazonia #amazonas #deforestacion #ganaderia', '3 mitos con datos reales: ya está afectando nuestra salud, el agua, los cultivos y la forma en que vivimos. 🤔 ¿Qué otro mito te gustaría que desmontemos? . . #cambioclimatico #medioambiente #co2 #mito #mitos #olasdecalor #seguridadalimentaria #reciclaje #recicla', 'El costo oculto de desperdiciar comida. El planeta paga un precio altísimo por el desperdicio de alimentos. Hambre, desigualdad y contaminación… pero también soluciones. Mira el video completo en mi canal de Youtube y Facebook . . #cambioclimatico #toogoodtogo #medioambiente#efectoinvernadero #comedyfilms #foodwaste #muckbang #hambruna', '¿Cómo nuestras acciones diarias, como el transporte y nuestra huella digital, impactan el cambio climático? 🚗💨 ¡Es momento de probar alternativas más verdes como la bici o caminar! 🚴‍♀️ #co2 #climatechange #medioambiente #movilidadsostenible #cambioclimatico', '☀️ Geoingeniería solar, ¿último salvavidas contra el cambio climático o la caja de Pandora más peligrosa de la humanidad? #cambioclimatico🌏 #medioambiente #geoingegneria #clima #sol', 'Corrientes Oceánicas El océano nos está enviando una señal, las corrientes del Atlántico podrían colapsar. Más frío en Europa, más sequías y tormentas en América y África. ¿Tú qué opinas? . . #oceano #oceanoatlantico🌊 #oceanoatlantico #cambioclimatico #medioambiente #noticiastiktok #noticia #capsulainformativa', '🧠📲 Un recorrido directo sobre cómo los algoritmos de redes sociales capturan tu atención, moldean opiniones y profundizan la polarización. ⚖️ Con un llamado claro a proteger los neuroderechos, exigir transparencia y recuperar el libre albedrío. 🎥 Video completo 👉 https://youtu.be/G28n0plg8So #Neuroderechos #Algoritmos #LibreAlbedrío #Desinformación #CámarasDeEco #EducaciónDigital #TransparenciaAlgorítmica #PrivacidadDeDatos #DemocraciaDigital #BienestarDigital #IA #CiudadaníaDigital', 'El científico que más dañó al planeta… y el que lo detuvo.'],
        'fecha_publicacion': ['03/12/2025', '28/11/2025', '27/11/2025', '26/11/2025', '25/11/2025', '24/11/2025', '21/11/2025', '19/11/2025', '18/11/2025', '17/11/2025', '15/11/2025', '14/11/2025', '12/11/2025', '10/11/2025', '08/11/2025', '06/11/2025', '04/11/2025', '01/11/2025', '29/10/2025', '28/10/2025', '27/10/2025', '25/10/2025', '23/10/2025', '17/10/2025', '16/10/2025', '15/10/2025', '14/10/2025', '10/10/2025', '09/10/2025', '08/10/2025', '07/10/2025', '04/10/2025', '01/10/2025', '27/09/2025', '23/09/2025', '19/09/2025', '16/09/2025', '12/09/2025', '10/09/2025', '05/09/2025'],
        'privacidad': ['Todo el mundo'] * 40,
        'visualizaciones': [127, 5669, 111, 179, 121, 165, 6511, 129, 1143, 5232, 1725, 276, 1437, 1293, 24000, 197, 38000, 235, 119, 21000, 12000, 2358, 192, 11000, 902, 617, 609, 599, 8788, 130, 128, 2856, 341, 274, 1204, 946, 7753, 681, 1273, 73000],
        'me_gusta': [19, 211, 3, 12, 3, 10, 121, 3, 8, 171, 83, 10, 35, 22, 1643, 11, 1894, 15, 2, 1171, 424, 135, 8, 345, 48, 43, 43, 35, 42, 2, 2, 266, 19, 12, 35, 35, 494, 42, 92, 1458],
        'comentarios': [2, 5, 0, 0, 0, 1, 1, 0, 0, 4, 3, 0, 4, 1, 22, 1, 16, 0, 0, 6, 2, 1, 0, 2, 2, 2, 1, 1, 2, 0, 0, 5, 3, 1, 1, 0, 4, 2, 0, 9]
    })
    
    for df_data in [youtobe_data, tiktok_data]:
        df_data['fecha_publicacion'] = pd.to_datetime(df_data['fecha_publicacion'], dayfirst=True, errors='coerce')
        hoy = pd.Timestamp.now()
        df_data['dias_desde_publicacion'] = (hoy - df_data['fecha_publicacion']).dt.days
        df_data['dias_desde_publicacion'] = df_data['dias_desde_publicacion'].apply(lambda x: max(x, 1))
        df_data['rendimiento_por_dia'] = df_data['visualizaciones'] / df_data['dias_desde_publicacion']
    
    return youtobe_data, tiktok_data

youtobe_df, tiktok_df = cargar_datos()

st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 0;
    }
    
    /* Sidebar styling - AZUL como la imagen */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        padding-top: 2rem;
    }
    
    /* Social media buttons */
    .social-btn {
        display: flex;
        align-items: center;
        padding: 15px 20px;
        margin: 8px 0;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        text-align: left;
    }
    
    .social-btn:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
    }
    
    .social-btn.active {
        background: rgba(59, 130, 246, 0.3);
        border-color: #3B82F6;
    }
    
    .social-icon {
        margin-right: 12px;
        font-size: 20px;
    }
    
    /* Metrics cards */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
        transition: transform 0.3s;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #1f2937;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 14px;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-trend {
        font-size: 14px;
        display: flex;
        align-items: center;
        margin-top: 5px;
    }
    
    .trend-up {
        color: #10b981;
    }
    
    .trend-down {
        color: #ef4444;
    }
    
    /* Status indicators */
    .status-connected {
        color: #10b981;
        font-weight: 600;
    }
    
    .status-disconnected {
        color: #ef4444;
        font-weight: 600;
    }
    
    /* Header */
    .dashboard-header {
        background: linear-gradient(90deg, #3B82F6 0%, #1D4ED8 100%);
        border-radius: 20px;
        padding: 30px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8fafc;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        background: transparent;
        color: #64748b;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #3B82F6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Performance chart container */
    .performance-chart {
        background: white;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin: 20px 0;
        border: 1px solid #e5e7eb;
    }
    
    /* Data table */
    .data-table-container {
        background: white;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin: 20px 0;
        border: 1px solid #e5e7eb;
    }
    
    /* Platform-specific colors */
    .youtube-color {
        color: #FF0000;
    }
    
    .tiktok-color {
        color: #000000;
    }
    
    .facebook-color {
        color: #1877F2;
    }
    
    .twitter-color {
        color: #1DA1F2;
    }
    
    .instagram-color {
        color: #E4405F;
    }
    
    .linkedin-color {
        color: #0A66C2;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a1a1a1;
    }
    
    /* Sidebar titles */
    .sidebar-title {
        color: white !important;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
        margin-top: 25px;
    }
    
    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 5px;
    }
    
    /* Status containers */
    .status-container {
        background: rgba(255, 255, 255, 0.1);
        padding: 12px 15px;
        border-radius: 10px;
        margin-bottom: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 40px; padding: 0 10px;">
            <h2 style="color: white; margin-bottom: 5px; font-size: 24px;">📊 DASHBOARD</h2>
            <p style="color: #94a3b8; font-size: 14px; margin: 0;">Social Media Analytics</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-title">🔗 Panel Professional</p>', unsafe_allow_html=True)
    
    facebook_selected = st.button("📘 Facebook", key="facebook_btn", use_container_width=True)
    twitter_selected = st.button("🐦 Twitter", key="twitter_btn", use_container_width=True)
    instagram_selected = st.button("📷 Instagram", key="instagram_btn", use_container_width=True)
    linkedin_selected = st.button("💼 LinkedIn", key="linkedin_btn", use_container_width=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-title">🎬 Video Platforms</p>', unsafe_allow_html=True)
    
    youtube_selected = st.button("▶️ YouTube", key="youtube_btn", use_container_width=True)
    tiktok_selected = st.button("🎵 TikTok", key="tiktok_btn", use_container_width=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-title">📈 Status</p>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="status-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #e2e8f0;">Facebook</span>
                <span class="status-disconnected">No conectado</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="status-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #e2e8f0;">Twitter</span>
                <span class="status-disconnected">No conectado</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="status-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #e2e8f0;">Instagram</span>
                <span class="status-disconnected">No conectado</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="status-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #e2e8f0;">LinkedIn</span>
                <span class="status-disconnected">No conectado</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="status-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #e2e8f0;">TikTok</span>
                <span class="status-disconnected">Cancelado</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="dashboard-header">
        <h1 style="margin: 0; font-size: 36px;">📊 SOCIAL MEDIA DASHBOARD</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 16px;">Professional Analytics & Performance Monitoring</p>
    </div>
""", unsafe_allow_html=True)

if youtube_selected:
    selected_platform = "YouTube"
    df = youtobe_df
    platform_color = "#FF0000"
    platform_name = "YouTube"
    icon = "▶️"
elif tiktok_selected:
    selected_platform = "TikTok"
    df = tiktok_df
    platform_color = "#000000"
    platform_name = "TikTok"
    icon = "🎵"
elif facebook_selected:
    selected_platform = "Facebook"
    df = youtobe_df
    platform_color = "#1877F2"
    platform_name = "Facebook"
    icon = "📘"
elif twitter_selected:
    selected_platform = "Twitter"
    df = youtobe_df
    platform_color = "#1DA1F2"
    platform_name = "Twitter"
    icon = "🐦"
elif instagram_selected:
    selected_platform = "Instagram"
    df = youtobe_df
    platform_color = "#E4405F"
    platform_name = "Instagram"
    icon = "📷"
elif linkedin_selected:
    selected_platform = "LinkedIn"
    df = youtobe_df
    platform_color = "#0A66C2"
    platform_name = "LinkedIn"
    icon = "💼"
else:
    selected_platform = "YouTube"
    df = youtobe_df
    platform_color = "#FF0000"
    platform_name = "YouTube"
    icon = "▶️"

st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 30px;">
        <div style="font-size: 28px; margin-right: 15px; color: {platform_color};">{icon}</div>
        <h2 style="margin: 0; color: {platform_color};">{platform_name} ANALYTICS</h2>
        <div style="margin-left: auto; background: {platform_color}10; color: {platform_color}; padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 600;">
            {len(df)} Videos
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_videos = len(df)
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL VIDEOS</div>
            <div class="metric-value">{total_videos}</div>
            <div class="metric-trend trend-up">
                <span>Active content</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    total_views = df['visualizaciones'].sum()
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL VIEWS</div>
            <div class="metric-value">{total_views:,}</div>
            <div class="metric-trend trend-up">
                <span>All time</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    avg_daily_perf = df['rendimiento_por_dia'].mean()
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">AVG DAILY PERFORMANCE</div>
            <div class="metric-value">{avg_daily_perf:.1f}</div>
            <div class="metric-trend trend-up">
                <span>Views per day</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    if df['visualizaciones'].sum() > 0:
        engagement_rate = ((df['me_gusta'].sum() + df['comentarios'].sum()) / df['visualizaciones'].sum() * 100)
    else:
        engagement_rate = 0
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ENGAGEMENT RATE</div>
            <div class="metric-value">{engagement_rate:.2f}%</div>
            <div class="metric-trend trend-up">
                <span>Likes & Comments</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="performance-chart">
        <h3 style="margin-top: 0; margin-bottom: 25px; color: #1f2937;">📈 PERFORMANCE OVER TIME</h3>
        <p style="color: #6b7280; margin-bottom: 20px; font-size: 14px;">Daily Performance Trends</p>
""", unsafe_allow_html=True)

try:
    dates = pd.date_range(start=datetime(2025, 10, 1), end=datetime(2025, 11, 30), freq='D')
    
    if selected_platform in ["YouTube", "TikTok"]:
        if selected_platform == "YouTube":
            views_by_date = youtobe_df.groupby('fecha_publicacion')['visualizaciones'].sum()
        else:
            views_by_date = tiktok_df.groupby('fecha_publicacion')['visualizaciones'].sum()
        
        views_data = []
        for date in dates:
            if date in views_by_date.index:
                views_data.append(views_by_date[date])
            else:
                views_data.append(0)
    else:
        views_data = [0] * len(dates)
    
    fig = make_subplots(rows=1, cols=2, 
                       subplot_titles=('Daily Views Trend', 'Engagement Metrics'),
                       specs=[[{'type': 'scatter'}, {'type': 'bar'}]])
    
    fig.add_trace(go.Scatter(x=dates, y=views_data, mode='lines', name='Views',
                            line=dict(color=platform_color, width=3)),
                  row=1, col=1)
    
    dates_ticks = ['Oct 7', 'Oct 14', 'Oct 21', 'Oct 28', 'Nov 4', 'Nov 11', 'Nov 18', 'Nov 25']
    tick_positions = [datetime(2025, 10, 7), datetime(2025, 10, 14), datetime(2025, 10, 21), 
                      datetime(2025, 10, 28), datetime(2025, 11, 4), datetime(2025, 11, 11),
                      datetime(2025, 11, 18), datetime(2025, 11, 25)]
    
    fig.add_trace(go.Bar(x=['Likes', 'Comments', 'Engagement'], 
                        y=[df['me_gusta'].sum(), df['comentarios'].sum(), engagement_rate],
                        marker_color=[platform_color, '#6b7280', '#10b981'],
                        name='Engagement'),
                  row=1, col=2)
    
    fig.update_layout(height=400, showlegend=False, template='plotly_white',
                     plot_bgcolor='white', paper_bgcolor='white',
                     margin=dict(l=20, r=20, t=40, b=20))
    
    fig.update_xaxes(title_text="Date", row=1, col=1, ticktext=dates_ticks, tickvals=tick_positions)
    fig.update_yaxes(title_text="Views", row=1, col=1)
    fig.update_xaxes(title_text="Metrics", row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
except Exception as e:
    st.warning(f"Error al generar gráfica: {str(e)}")
    st.info("Mostrando datos en formato alternativo...")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class="data-table-container">
        <h3 style="margin-top: 0; margin-bottom: 25px; color: #1f2937;">📊 CONTENT PERFORMANCE DATA</h3>
""", unsafe_allow_html=True)

if selected_platform in ["YouTube", "TikTok"]:
    top_videos = df.nlargest(10, 'visualizaciones')[['titulo', 'fecha_publicacion', 'visualizaciones', 'me_gusta', 'comentarios', 'rendimiento_por_dia']]
    top_videos['fecha_publicacion'] = top_videos['fecha_publicacion'].dt.strftime('%Y-%m-%d')
    top_videos = top_videos.rename(columns={
        'titulo': 'Title',
        'fecha_publicacion': 'Publish Date',
        'visualizaciones': 'Views',
        'me_gusta': 'Likes',
        'comentarios': 'Comments',
        'rendimiento_por_dia': 'Daily Perf.'
    })
    
    st.dataframe(top_videos.style.format({
        'Views': '{:,}',
        'Daily Perf.': '{:.1f}'
    }).background_gradient(subset=['Views', 'Daily Perf.'], cmap='Reds' if selected_platform == "YouTube" else 'Blues'), 
    height=400, use_container_width=True)
else:
    st.info(f"🔒 {platform_name} analytics require platform connection")
    st.markdown("""
        <div style="text-align: center; padding: 40px; background: #f8fafc; border-radius: 10px;">
            <div style="font-size: 48px; margin-bottom: 20px; color: #cbd5e1;">{icon}</div>
            <h3 style="color: #64748b;">Connect to {platform_name}</h3>
            <p style="color: #94a3b8;">Grant permissions to access your public profile and posts.</p>
            <div style="display: flex; gap: 10px; justify-content: center; margin-top: 20px;">
                <button style="background: #ef4444; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer;">Cancel</button>
                <button style="background: {platform_color}; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer;">Connect</button>
            </div>
        </div>
    """.format(icon=icon, platform_name=platform_name, platform_color=platform_color), unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

col_analysis1, col_analysis2 = st.columns(2)

with col_analysis1:
    st.markdown("""
        <div class="performance-chart" style="height: 100%;">
            <h3 style="margin-top: 0; margin-bottom: 20px; color: #1f2937;">📊 PERFORMANCE ANALYTICS</h3>
    """, unsafe_allow_html=True)
    
    if selected_platform in ["YouTube", "TikTok"]:
        high_perf = len(df[df['rendimiento_por_dia'] > df['rendimiento_por_dia'].quantile(0.75)])
        medium_perf = len(df[(df['rendimiento_por_dia'] >= df['rendimiento_por_dia'].quantile(0.25)) & 
                            (df['rendimiento_por_dia'] <= df['rendimiento_por_dia'].quantile(0.75))])
        low_perf = len(df[df['rendimiento_por_dia'] < df['rendimiento_por_dia'].quantile(0.25)])
        
        fig_pie = go.Figure(data=[go.Pie(labels=['High Performers', 'Medium', 'Low'],
                                        values=[high_perf, medium_perf, low_perf],
                                        hole=0.4,
                                        marker=dict(colors=['#10b981', '#3B82F6', '#6b7280']))])
        
        fig_pie.update_layout(height=300, showlegend=True, template='plotly_white',
                             margin=dict(l=20, r=20, t=30, b=20))
        
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Performance data requires platform connection")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_analysis2:
    st.markdown("""
        <div class="performance-chart" style="height: 100%;">
            <h3 style="margin-top: 0; margin-bottom: 20px; color: #1f2937;">📈 KEY METRICS</h3>
    """, unsafe_allow_html=True)
    
    if selected_platform in ["YouTube", "TikTok"]:
        metrics_data = {
            'Metric': ['Avg. Views/Video', 'Avg. Likes/Video', 'Avg. Comments/Video', 
                      'Max Daily Performance', 'Content Age (days)', 'Engagement Rate'],
            'Value': [f"{df['visualizaciones'].mean():.0f}", 
                     f"{df['me_gusta'].mean():.1f}", 
                     f"{df['comentarios'].mean():.1f}",
                     f"{df['rendimiento_por_dia'].max():.1f}",
                     f"{df['dias_desde_publicacion'].mean():.0f}",
                     f"{engagement_rate:.2f}%"]
        }
        
        for i, (metric, value) in enumerate(zip(metrics_data['Metric'], metrics_data['Value'])):
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; 
                           padding: 12px 0; border-bottom: {'1px solid #e5e7eb' if i < len(metrics_data['Metric'])-1 else 'none'};">
                    <span style="color: #4b5563; font-size: 14px;">{metric}</span>
                    <span style="font-weight: 600; color: #1f2937; font-size: 16px;">{value}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Connect to view platform metrics")
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 14px; padding: 30px; border-top: 1px solid #e5e7eb; margin-top: 40px;">
        Social Media Dashboard v2.0 • Data updated in real-time • {selected_platform} Analytics
    </div>
""".format(selected_platform=selected_platform), unsafe_allow_html=True)
