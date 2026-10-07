from flask import Flask, render_template_string, abort, request
from datetime import datetime

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 31536000

BRAND = {
    "name": "BRUGAFI",
    "tagline": "Scent a Beautiful Life",
    "domain": "brugafi.homes",
    "email": "hola@brugafi.homes",
}

COLLECTIONS = [{'slug': 'exclusiva',
  'title': 'Colección Exclusiva',
  'image': 'img/colecciones/exclusiva.webp',
  'items': [{'name': 'Haven',
             'profile': 'Neutro',
             'notes': 'Algodón, pera, lirio, almizcle, vainilla',
             'inspiration': 'Clásicos aromas de suavizantes americanos'},
            {'name': 'Pure',
             'profile': 'Neutro',
             'notes': 'Hierbas, naranja, almizcle, madera',
             'inspiration': 'Aroma limpio de jabón en barra'},
            {'name': 'Iris',
             'profile': 'Neutro',
             'notes': 'Ylang ylang, violeta, tomillo, musgo',
             'inspiration': 'Neutro'},
            {'name': 'calm',
             'profile': 'Herbal - Dulce',
             'notes': 'Lavanda, leche, miel',
             'inspiration': 'Herbal - Dulce'},
            {'name': 'Napa',
             'profile': 'Neutro',
             'notes': 'Cuero nuevo, cedro seco, hojas de violeta, cardamomo',
             'inspiration': 'Neutro'},
            {'name': 'Satin', 'profile': 'Neutro', 'notes': 'Sándalo blanco', 'inspiration': 'Neutro'}]},
 {'slug': 'hoteles',
  'title': 'Colección Hoteles',
  'image': 'img/colecciones/hoteles.webp',
  'items': [{'name': 'Royal',
             'profile': 'Neutro / Floral',
             'notes': 'Orquídea, flores blancas, sándalo, incienso',
             'inspiration': 'Ritz Carlton'},
            {'name': 'Jungle',
             'profile': 'Cítrico',
             'notes': 'Lima, bambú, flor de loto, cedro, vainilla',
             'inspiration': 'Xcaret México'},
            {'name': 'Sharp',
             'profile': 'Neutro',
             'notes': 'Higo, almendra, ámbar, cedro, almizcle',
             'inspiration': 'Four Seasons'},
            {'name': 'Bloom',
             'profile': 'Cítrico - Floral',
             'notes': 'Lemongrass, almizcle, flores frescas, citrus',
             'inspiration': 'Rosewood México'},
            {'name': 'Cliff',
             'profile': 'Cítrico - Amaderado',
             'notes': 'Vetiver, naranja amarga, toronja roja',
             'inspiration': 'Cap Rocat, Mallorca'},
            {'name': 'Lagoon',
             'profile': 'Floral - Ambarado',
             'notes': 'Almizcle, tonka, ámbar gris, toronja, cassis, rosa, azahar',
             'inspiration': 'The Westin Maui Resort & Spa'},
            {'name': 'Breeze',
             'profile': 'Aromático - Fresco',
             'notes': 'Menta, lavanda, eucalipto, toques cítricos',
             'inspiration': 'Live Aqua Beach Resort Cancún'},
            {'name': 'Vogue',
             'profile': 'Frutal - Floral',
             'notes': 'Manzana, frambuesa, pomelo, cedro blanco, mezclas florales',
             'inspiration': 'Marriott Hotels'},
            {'name': 'Gold',
             'profile': 'Floral - Almizclado',
             'notes': 'Lirio, jazmín, melón verde, anís, almizcle',
             'inspiration': 'Wynn Las Vegas'}]},
 {'slug': 'tiendas',
  'title': 'Colección Tiendas',
  'image': 'img/colecciones/tiendas.webp',
  'items': [{'name': 'Fancy',
             'profile': 'Amaderado',
             'notes': 'Herbal, musgo, cedro, ámbar',
             'inspiration': 'Palacio de Hierro'},
            {'name': 'Dusk',
             'profile': 'Amaderado',
             'notes': 'Toronja, bergamota, pimienta rosa, clearwood, gamuza, musgo',
             'inspiration': 'Abercrombie'},
            {'name': 'Linen', 'profile': 'Neutro', 'notes': 'Té blanco, tomillo', 'inspiration': 'Zara Home'},
            {'name': 'Aero',
             'profile': 'Cítrico / Neutro',
             'notes': 'Bergamota, té blanco, limón, gamuza',
             'inspiration': 'InnovaSport'}]}]

DIFFUSERS = [
    {
        "code":"BGF45",
        "coverage":"Hasta 45 m²",
        "image":"img/difusores/difusor-45.webp",
        "stripe_url":"#",
        "description_html":"Ideal para espacios personales y acogedores como <strong>lofts, recibidores, consultorios, oficinas privadas, estudios, recámaras amplias o pequeños espacios de atención.</strong><br>Una opción discreta para mantener una presencia aromática agradable y constante."
    },
    {
        "code":"BGF70",
        "coverage":"Hasta 70 m²",
        "image":"img/difusores/difusor-70.webp",
        "stripe_url":"#",
        "description_html":"Pensado para espacios medianos como <strong>salas de estar, salas de juntas, oficinas, boutiques, showrooms y áreas de convivencia.</strong><br>Equilibrio entre cobertura y presencia para espacios donde el aroma también forma parte de la experiencia."
    },
    {
        "code":"BGF140",
        "coverage":"Hasta 140 m²",
        "image":"img/difusores/difusor-140.webp",
        "stripe_url":"#",
        "description_html":"Diseñado para espacios amplios como <strong>halls, recepciones, oficinas abiertas, showrooms, boutiques grandes, salas de espera, gimnasios boutique y áreas comerciales o de atención.</strong><br>Mayor cobertura para crear una identidad aromática perceptible desde el primer momento."
    },
]

PRODUCTS = [
    {"title":"Aceite para difusor","size":"250 ml","stripe_url":"#","image":"img/productos/aceite-250.webp","copy":"Fragancia de alta fijación para difusores profesionales. Compatible únicamente con difusores de aromas; no apto para humidificadores.","details_html":'<p><strong>Beneficios del producto</strong></p><p>Descubre el poder del Diffuser Fragance Oil BRUGAFI. Diseñado para llenar tus espacios con fragancias elegantes con alta fijación, transforma cualquier ambiente en un refugio de bienestar y sofisticación.</p><p>Fórmula de alta calidad para una experiencia aromática intensa y prolongada. Ideal para crear atmósferas relajantes, energizantes o equilibradas según el aroma seleccionado.</p><p><strong>Capacidad 250 mL</strong></p><p><strong>Modos de uso</strong></p><p>Siguiendo las indicaciones del dispositivo, vierte nuestro aceite hasta la capacidad que indique el recipiente que incluye el difusor. Disfruta de un ambiente lleno de fragancia refinada.</p><p>Ofrecemos aceite aromático formulado exclusivamente para su uso en difusores eléctricos profesionales BRUGAFI. (no apto para humidificadores).</p><p>Sin embargo, para el rendimiento del aroma influye la intensidad, duración, cobertura en m².</p><p>Cada máquina ofrece una experiencia aromática distinta según su tecnología, potencia de bruma y rango de cobertura. <strong>Ajusta la intensidad a tu gusto y disfruta BRUGAFI de la forma que mejor se adapte a tu espacio.</strong></p><p>Además, la duración del aceite también dependerá del modo de programación. A mayor intensidad de bruma, mayor consumo de producto.</p><p><strong>Ejemplo de uso recomendado:</strong><br>Configuración de 10 segundos de difusión cada 5 minutos durante 8 horas al día. Con esta configuración, nuestro envase de 250 ml puede durar aproximadamente 1.5 meses.</p><p><strong>Cuidados y precauciones</strong></p><p>No aplicar en piel o mascotas. No mezcles con otros productos. Guarda en lugar fresco, seco y fuera del alcance de niños y animales.</p><ul><li>Fragancias de alta fijación</li><li>Libres de Ftalatos y Parabenos</li><li>Envíos a todo México</li></ul>'},
    {"title":"Perfume para telas","size":"150 ml · 350 ml","stripe_url":"#","image":"img/productos/perfume-telas.webp","copy":"Aromas frescos y duraderos para ropa y textiles. No deja residuos y está pensado para acompañar el cuidado de tus prendas.","details_html":'<p>Nuestro <strong>Perfume para Telas</strong> está formulado para <strong>aromatizar fibras y superficies textiles</strong> (sábanas, edredones, cojines, toallas, cortinas, tapicería, etc.).</p><p><strong>No es un aromatizante ambiental.</strong> Su función principal es perfumar la <strong>tela</strong>, como su nombre lo indica, y no perfumar el aire de una habitación de forma continua.</p><p><strong>¿Qué sí hace?</strong></p><ul><li>Deja un <strong>aroma limpio y duradero</strong> sobre textiles.</li><li>Aporta sensación de <strong>frescura</strong> a su ropa de cama y a las telas de uso diario.</li><li>No mancha ni decolora las telas, seca rápidamente.</li></ul><p><em>Realice siempre una <strong>prueba en zona poco visible</strong> antes del primer uso.</em></p><p><strong>¿Qué no hace?</strong></p><ul><li>No está diseñado para <strong>difundir fragancia en el ambiente</strong> ni sustituye un sistema de aromatización de espacios.</li></ul><p><strong>Uso recomendado</strong></p><ol><li><strong>Rocíe a 20–30 cm</strong> de distancia sobre la tela.</li><li>Deje <strong>secar al aire</strong> antes de usar o sentarse.</li></ol><p><strong>¿Desea aromatizar su hogar?</strong></p><p>Para perfumar el <strong>ambiente</strong> de forma uniforme y constante, le recomendamos nuestro <strong>Aceite para Difusor Eléctrico de Aromas</strong> (uso exclusivo en máquinas difusoras profesionales BRUGAFI). Este producto trabaja con su equipo para dispersar la fragancia en el aire y mantener el aroma del espacio.</p><ul><li><strong>Opción adecuada para ambientes:</strong> <em>Aceite para Difusor Eléctrico de Aromas</em> (no usar en humidificadores).</li><li><strong>Opción adecuada para textiles:</strong> <em>Perfume para Telas</em>.</li></ul><p><strong>Beneficios del producto</strong></p><p><strong>Modos de uso</strong></p><p><strong>Cuidados y precauciones</strong></p><ul><li>Fragancias de alta fijación</li><li>Libres de Ftalatos y Parabenos</li><li>Envíos a todo México</li></ul>'},
    {"title":"Difusor de varillas","size":"100 ml","stripe_url":"#","image":"img/productos/difusor-varillas.webp","copy":"Fragancia continua, sutil y elegante para baños, espacios pequeños, hogar, oficina y negocio.","details_html":"<p>Los difusores de varitas o Reed diffuser proporcionan una fragancia continua y sutil sin necesidad de fuego, lo que los hace seguros para usar en cualquier ambiente. Son fáciles de usar y requieren poco mantenimiento: simplemente necesitas girar las varitas de vez en cuando para intensificar el aroma. Además, vienen en una variedad de fragancias y diseños decorativos, lo que los convierte en un elemento estético en la decoración del hogar. Al ser duraderos, ofrecen una experiencia aromática prolongada y pueden contribuir a crear un ambiente relajante y acogedor.</p><p><strong>Presentación 100 mL</strong></p><p><strong>Beneficios</strong></p><ul><li>Ideal para <strong>baños</strong>: fragancia constante y agradable.</li><li><strong>Diseño neutro y elegante</strong>: combina con cualquier decoración.</li><li><strong>Aroma continuo 24/7</strong> sin electricidad ni flama.</li><li>Excelente opción para <strong>hogar, oficinas y negocios</strong>.</li><li>Aporta sensación de <strong>limpieza, frescura y armonía</strong>.</li></ul><p><strong>Modo de uso</strong><br>Inserte las varillas en el frasco, espere 24 h para saturación y voltee las varillas para reactivar el aroma. Ubique en zonas con ligera o nula circulación de aire.</p><p><strong>Precauciones</strong><br>Mantener fuera del alcance de niños y mascotas. Evitar contacto con ojos y piel. No ingerir. Mantener alejado de temperaturas altas.</p><ul><li>Fragancias de alta fijación</li><li>Libres de Ftalatos y Parabenos</li><li>Envíos a todo México</li></ul>"},
]

FAQS = [
    ("Difusor de aromas", ["Aroma uniforme y constante (sin saturar).","Programación desde el celular.","Ideal para negocios y hogar: recibidor, consultorio, boutique y oficina.","Experiencia premium: eleva la percepción del espacio."]),
    ("Aceite para difusor", ["Descubre el poder del Difusser Fragance Oil, diseñado para llenar tus espacios con fragancias elegantes con alta fijación.","Transforma cualquier ambiente en un refugio de bienestar y sofisticación.","Compatible únicamente con difusores de aromas (no apto para humidificadores).","Fórmula de alta calidad para una experiencia aromática intensa y prolongada.","Ideal para crear atmósferas relajantes, energizantes o equilibradas según el aroma seleccionado."]),
    ("Perfume para telas", ["Aromas frescos y duraderos que cuidan tu ropa y el planeta.","Nuestras fragancias no dañan los tejidos ni dejan residuos, por lo que alargan la vida de tus prendas y reducen los lavados.","Una forma sencilla y consciente de llenar tu hogar de calidez sin comprometer el cuidado.","El detalle que transforma tu rutina en una decisión inteligente."]),
    ("¿Las fragancias son libres de ftalatos y parabenos?", ["Sí. BRUGAFI comunica sus fragancias como libres de ftalatos y parabenos."]),
    ("¿Qué presentaciones manejan?", ["Aceite para difusor: 250 ml.","Perfume para telas: 150 ml y 350 ml.","Difusor de varillas: 100 ml."])
]

PRIVACY = """BRUGAFI protege los datos personales que sus clientes y visitantes proporcionen por medios digitales, formularios, procesos de compra o contacto. Los datos podrán utilizarse para identificar al cliente, procesar pedidos, coordinar entregas, atender solicitudes, dar seguimiento comercial y comunicar información relacionada con productos y servicios BRUGAFI. BRUGAFI no venderá datos personales a terceros. Cuando sea necesario para completar una operación, la información podrá compartirse únicamente con proveedores que participen en el procesamiento de pagos, logística, alojamiento tecnológico o atención al cliente, bajo las condiciones aplicables. El titular podrá solicitar acceso, rectificación, cancelación u oposición respecto de sus datos escribiendo al correo oficial de BRUGAFI. Al utilizar este sitio, el usuario reconoce haber leído este aviso de privacidad."""

TERMS = """Al utilizar brugafi.homes o realizar una compra, el usuario acepta estos términos. Las imágenes, descripciones y materiales del sitio tienen fines informativos y comerciales. Los precios, disponibilidad, presentaciones y promociones podrán cambiar antes de confirmar una compra. Una operación se considera aceptada cuando el pago ha sido confirmado. El cliente es responsable de proporcionar datos correctos de contacto y entrega. BRUGAFI podrá cancelar o reembolsar una operación cuando exista un error evidente de precio, falta de inventario, imposibilidad de entrega o una incidencia de pago. Los productos deberán utilizarse de acuerdo con su propósito: el aceite para difusor es para equipos de difusión de aromas y no para humidificadores. El uso del sitio no concede derechos sobre marcas, textos, fotografías, diseños ni otros materiales de BRUGAFI."""

LEGAL = """BRUGAFI es una marca de productos de aromatización para hogar, oficina y espacios comerciales. Las referencias sensoriales utilizadas para describir algunos aromas tienen el único propósito de ayudar al cliente a comprender su perfil olfativo. Las marcas, hoteles, tiendas o perfumes mencionados como inspiración pertenecen a sus respectivos titulares y no implican afiliación, autorización, patrocinio ni relación comercial con BRUGAFI, salvo que se indique expresamente lo contrario. Los resultados de intensidad, duración y percepción aromática pueden variar según ventilación, superficie, temperatura, configuración del difusor y características del espacio. La información del sitio no sustituye las instrucciones específicas de uso y seguridad del producto."""

SHIPPING = """ENTREGA EN TU DOMICILIO CON PAQUETERÍA\n\nTu pedido estará listo en 2 días hábiles, te llegará una notificación de pedido empacado vía correo electrónico. Posterior, se asignará una paquetería que surtirá tu paquete de 2 a 3 días hábiles dentro de la zona metropolitana.\n\nEn caso de ser envío al interior de la república tu envío demorará de 4 a 7 días hábiles, aunque puede ser menos."""

HOME = r"""
<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="preload" as="image" href="/static/img/fondos/main.webp" fetchpriority="high"><title>BRUGAFI | Home Fragrance</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--gold:#C8B273;--night:#0A0A0C;--ivory:#F5F0E7;--text:#1E1C19}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:Inter,sans-serif;color:var(--text);background:#15120f}a{text-decoration:none;color:inherit}.bg{position:fixed;inset:0;background:url('/static/img/fondos/main.webp') center center/cover no-repeat;z-index:-3}.veil{position:fixed;inset:0;background:linear-gradient(180deg,rgba(7,6,5,.04) 0%,rgba(7,6,5,.08) 42%,rgba(10,8,6,.38) 100%);z-index:-2}.container{width:min(1200px,calc(100% - 38px));margin:auto}header{position:fixed;inset:0 0 auto 0;z-index:30;background:rgba(18,15,12,.42);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,.08);}.nav{height:76px;display:flex;align-items:center;justify-content:space-between;color:#fff}.brand-lockup{display:flex;align-items:center;gap:26px}
.logo-stack{display:flex;flex-direction:column;align-items:stretch;width:max-content}
.logo{font-family:'Cormorant Garamond',serif;font-size:34px;letter-spacing:.14em;line-height:.95}
.logo-domain{font-family:'Cormorant Garamond',serif;font-size:12px;letter-spacing:.72em;line-height:1;margin-top:7px;text-align:center;padding-left:.72em;opacity:.92}
.brand-slogan{font-family:'Cormorant Garamond',serif;font-size:20px;letter-spacing:.05em;white-space:nowrap;opacity:.96}
.nav-links{display:flex;gap:18px;font-size:12px;text-transform:uppercase;letter-spacing:.09em}.hero{height:100svh;min-height:650px}.content{padding:24px 0 54px;background:linear-gradient(180deg,rgba(20,16,12,.05),rgba(20,16,12,.34))}.section{padding:66px 0}.section h2{font-family:'Cormorant Garamond',serif;color:#fff;font-size:clamp(40px,5vw,62px);margin:0 0 26px;text-shadow:0 2px 16px rgba(0,0,0,.25)}.brand-title{font-family:'Cormorant Garamond',serif;letter-spacing:.14em;font-weight:500;white-space:nowrap}.collection-grid,.diff-grid,.product-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}.collection-card{height:410px;position:relative;overflow:hidden;background-size:cover;background-position:center;display:flex;align-items:flex-end;box-shadow:0 22px 48px rgba(0,0,0,.16);border-radius:20px;border:1px solid rgba(0,0,0,.38)}.lazy-bg{background-image:none}.section{content-visibility:auto;contain-intrinsic-size:900px}.collection-card:after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.02),rgba(0,0,0,.48))}.collection-card .label{position:relative;z-index:2;color:#fff;padding:26px}.collection-card h3{font-family:'Cormorant Garamond',serif;font-size:38px;margin:0 0 4px}.collection-card small{opacity:.85}.diff-card{min-height:520px;perspective:1500px}.diff-inner{position:relative;width:100%;min-height:520px;transform-style:preserve-3d;transition:transform .75s cubic-bezier(.2,.7,.2,1)}.diff-card:hover .diff-inner,.diff-card:focus-within .diff-inner,.diff-card.is-flipped .diff-inner{transform:rotateY(180deg)}.diff-face{position:absolute;inset:0;border-radius:22px;overflow:hidden;backface-visibility:hidden;-webkit-backface-visibility:hidden;box-shadow:0 20px 44px rgba(0,0,0,.12);background-size:cover;background-position:center}.diff-front:before{content:'';position:absolute;inset:0;background:rgba(248,243,234,.83);backdrop-filter:blur(1px)}.diff-back{transform:rotateY(180deg);background-size:cover;background-position:center}.diff-info{position:relative;z-index:2;padding:28px;height:100%;display:flex;flex-direction:column}.diff-info .code{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#7c642a;font-weight:700}.diff-info h3{font-family:'Cormorant Garamond',serif;font-size:34px;margin:10px 0 8px}.diff-info p{line-height:1.7;color:#51483f}.specs{margin-top:auto}.specs div{padding:8px 0;border-bottom:1px solid rgba(0,0,0,.08);font-size:14px}
.diff-card{cursor:pointer}
.diff-back{display:flex;align-items:flex-end;justify-content:center;padding:24px}
.diff-back::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.02),rgba(0,0,0,.32));pointer-events:none}
.diff-buy-wrap{position:relative;z-index:3;width:100%;display:flex;justify-content:center}
.diff-buy-btn{display:inline-flex;align-items:center;justify-content:center;min-width:180px;padding:13px 22px;border:1px solid #C8B273;border-radius:999px;background:#0A0A0C;color:#F3E6BD;font-weight:700;text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.22)}
.diff-buy-btn:hover{background:#18130d}
.diff-buy-btn.disabled{opacity:.6;cursor:default}
.mobile-flip-hint{display:none;font-size:12px;color:#705a28;margin-top:10px;font-weight:700}
@media (hover:none),(pointer:coarse){
  .diff-card:hover .diff-inner{transform:none}
  .diff-card.is-flipped .diff-inner{transform:rotateY(180deg)}
  .mobile-flip-hint{display:block}
}

.product-card{min-height:410px;display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:10px;background:rgba(248,243,234,.18);backdrop-filter:blur(8px);border-radius:22px;padding:24px;color:#fff;box-shadow:0 18px 42px rgba(0,0,0,.10)}.product-card img,.product-summary img{width:100%;max-height:320px;object-fit:contain;filter:drop-shadow(0 18px 25px rgba(0,0,0,.18))}.product-card h3,.product-summary h3{font-family:'Cormorant Garamond',serif;font-size:31px;margin:0 0 6px}.product-card .size,.product-summary .size{font-weight:700;color:#f0d58d;margin-bottom:8px}.product-card p,.product-summary p{font-size:14px;line-height:1.65;color:#f1ece3}.expand-card{display:block}.product-summary{display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:10px;cursor:pointer;list-style:none}.product-summary::-webkit-details-marker{display:none}.expand-body{margin-top:18px;padding-top:18px;border-top:1px solid rgba(255,255,255,.16);color:#f1ece3;font-size:14px;line-height:1.72}.expand-body p{margin:0 0 12px}.expand-body ul{margin:0 0 14px;padding-left:18px}.expand-body li{margin:6px 0}.buy-wrap{margin-top:22px;padding-top:18px;border-top:1px solid rgba(255,255,255,.16)}.buy-btn{display:inline-flex;align-items:center;justify-content:center;min-width:190px;padding:13px 20px;border:1px solid #C8B273;border-radius:999px;background:#0A0A0C;color:#F3E6BD;font-weight:700;text-decoration:none;transition:transform .2s ease,background .2s ease}.buy-btn:hover{transform:translateY(-1px);background:#17130d}.buy-btn.disabled{opacity:.58;cursor:default;pointer-events:none}.quality{display:grid;grid-template-columns:1fr auto;align-items:center;gap:36px;color:#fff;padding:34px 0}.quality h2{margin-bottom:14px}.badge-wrap{width:220px;height:220px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:radial-gradient(circle,rgba(200,178,115,.15),transparent 66%);filter:drop-shadow(0 18px 26px rgba(0,0,0,.25))}.badge-wrap img{width:200px;border-radius:50%;mix-blend-mode:normal}.faq{display:grid;gap:10px}.faq details{background:rgba(248,243,234,.80);backdrop-filter:blur(10px);border-radius:14px;overflow:hidden}.faq summary{padding:18px 20px;cursor:pointer;font-weight:700;list-style:none;display:flex;justify-content:space-between}.faq summary:after{content:'+';font-size:23px;color:#8c6c24}.faq details[open] summary:after{content:'–'}.answer{padding:0 20px 18px;line-height:1.7;color:#4f473f}.answer ul{margin:0;padding-left:18px}.legal-final{padding:66px 0 28px}.legal-shell{background:rgba(8,8,8,.96);color:#f2e9d5;border:1px solid var(--gold);padding:10px;margin-top:0}.legal-inner{border:1px solid rgba(200,178,115,.45);padding:28px}.legal-brand{margin:0 0 18px;color:#cfc3aa;line-height:1.7;font-size:15px}.legal-links{display:flex;gap:20px;flex-wrap:wrap}.legal-links a{color:#e1c77f;border-bottom:1px solid rgba(225,199,127,.55);padding-bottom:3px}.footer-line{display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;margin-top:28px;padding-top:18px;border-top:1px solid rgba(225,199,127,.18);color:#eee;font-size:13px}@media(max-width:900px){.brand-slogan{display:none}.logo-domain{font-size:10px}.collection-grid,.diff-grid,.product-grid{grid-template-columns:1fr}.collection-card{height:340px}.product-card,.product-summary{grid-template-columns:1fr 1fr}.quality{grid-template-columns:1fr}.nav-links{display:none}.hero{height:100svh;min-height:560px}}@media(max-width:520px){.container{width:min(100% - 24px,1200px)}.product-card,.product-summary{grid-template-columns:1fr}.badge-wrap{width:170px;height:170px}.badge-wrap img{width:155px}}
</style></head><body><div class="bg"></div><div class="veil"></div><header><div class="container nav"><div class="brand-lockup">
      <div class="logo-stack">
        <div class="logo">BRUGAFI</div>
        <div class="logo-domain">.homes</div>
      </div>
      <div class="brand-slogan">Scent a Beautiful Life</div>
    </div>
    <div class="nav-links"><a href="#colecciones">Colecciones</a><a href="#difusores">Difusores</a><a href="#productos">Fragancias</a><a href="#faq">Preguntas</a></div></div></header><section class="hero"></section><main class="content"><div class="container">
<section class="section" id="colecciones"><h2>Colecciones <span class="brand-title">BRUGAFI</span></h2><div class="collection-grid">{% for c in collections %}<a class="collection-card" href="/coleccion/{{c.slug}}" data-bg="/static/{{c.image}}"><div class="label"><h3>{{c.title}}</h3><small>Descubre la colección</small></div></a>{% endfor %}</div></section>
<section class="section" id="difusores"><h2>Elige tu difusor</h2><div class="diff-grid">{% for d in diffusers %}<article class="diff-card" tabindex="0" role="button" aria-label="Ver imagen de {{d.code}}" onclick="toggleDiffuser(this,event)" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();toggleDiffuser(this,event)}"><div class="diff-inner"><div class="diff-face diff-front" data-bg="/static/{{d.image}}"><div class="diff-info"><span class="code">{{d.code}}</span><h3>{{d.code}} — {{d.coverage}}</h3><p>{{d.description_html|safe}}</p><div class="specs"><div><strong>Tu ambiente, desde tu celular</strong></div><div>Controla y programa tu difusor directamente desde tu celular.</div><div>Ajusta horarios e intensidad para cada momento del día.</div><div>Crea la atmósfera que quieres con solo unos toques.</div></div><div class="mobile-flip-hint">Toca para ver el difusor</div></div></div><div class="diff-face diff-back" data-bg="/static/{{d.image}}"><div class="diff-buy-wrap">{% if d.stripe_url.startswith('https://') %}<a class="diff-buy-btn" href="{{d.stripe_url}}" target="_blank" rel="noopener" onclick="event.stopPropagation()">Comprar</a>{% else %}<span class="diff-buy-btn disabled" onclick="event.stopPropagation()">Agregar liga Stripe</span>{% endif %}</div></div></div></article>{% endfor %}</div></section>
<section class="section" id="productos"><h2>Fragancias BRUGAFI</h2><div class="product-grid">{% for p in products %}<details class="product-card expand-card"><summary class="product-summary"><div><div class="size">{{p.size}}</div><h3>{{p.title}}</h3><p>{{ p['copy'] }}</p><span class="soft-link">Ver detalles</span></div><img loading="lazy" decoding="async" src="{{ p.image if p.image.startswith('data:') else '/static/' + p.image }}" alt="{{p.title}}"></summary><div class="expand-body">{{ p.details_html|safe }}<div class="buy-wrap">{% if p.stripe_url.startswith('https://') %}<a class="buy-btn" href="{{p.stripe_url}}" target="_blank" rel="noopener">Comprar</a>{% else %}<span class="buy-btn disabled">Agregar liga Stripe</span>{% endif %}</div></div></details>{% endfor %}</div></section>
<section class="section quality"><div><h2>Calidad que da tranquilidad</h2><p style="color:#f3eee5;max-width:820px;line-height:1.8"><strong>Sin ftalatos ni parabenos:</strong> reduce la exposición a ingredientes que han sido cuestionados por sus posibles efectos hormonales, especialmente con el uso frecuente. Una formulación más consciente, manteniendo la experiencia aromática premium de BRUGAFI.</p></div><div class="badge-wrap"><img loading="lazy" decoding="async" src="/static/img/marca/premium-quality.webp" alt="Premium High Quality"></div></section>
<section class="section" id="faq"><h2>Preguntas frecuentes</h2><div class="faq">{% for q,lines in faqs %}<details><summary>{{q}}</summary><div class="answer"><ul>{% for line in lines %}<li>{{line}}</li>{% endfor %}</ul></div></details>{% endfor %}</div></section>
<section class="section legal-final" id="privacidad"><div class="legal-shell"><div class="legal-inner"><p class="legal-brand">BRUGAFI · Scent a Beautiful Life</p><div class="legal-links"><a href="/aviso-privacidad">Aviso de privacidad</a><a href="/terminos">Términos del servicio</a><a href="/legal">Legal</a><a href="/politicas-envio">Políticas de envío</a></div><div class="footer-line"><span>© {{year}} BRUGAFI</span><span>{{brand.domain}}</span></div></div></div></section>
</div></main><script>
(function(){
  var nodes=document.querySelectorAll('[data-bg]');
  function apply(el){var u=el.getAttribute('data-bg');if(u){el.style.backgroundImage='url("'+u+'")';el.removeAttribute('data-bg');}}
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){apply(e.target);io.unobserve(e.target);}});},{rootMargin:'500px 0px'});
    nodes.forEach(function(el){el.classList.add('lazy-bg');io.observe(el);});
  }else{nodes.forEach(apply);}
})();
</script>
<script>
function toggleDiffuser(card,event){
  if(event && event.target.closest('.diff-buy-btn')) return;
  card.classList.toggle('is-flipped');
}
</script>
</body></html>"""

COLLECTION_PAGE = r"""
<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="preload" as="image" href="/static/img/fondos/main.webp" fetchpriority="high"><title>{{collection.title}} | BRUGAFI</title><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><style>
*{box-sizing:border-box}body{margin:0;font-family:Inter,sans-serif;color:#fff;background:#111}a{text-decoration:none;color:inherit}.bg{position:fixed;inset:0;background:url('/static/{{collection.image}}') center/cover no-repeat;z-index:-3}.shade{position:fixed;inset:0;background:rgba(8,7,6,.44);z-index:-2}.container{width:min(1160px,calc(100% - 34px));margin:auto}.top{padding:22px 0;display:flex;justify-content:space-between;align-items:center}.logo{font-family:'Cormorant Garamond',serif;font-size:32px;letter-spacing:.14em}.hero{padding:70px 0 24px}.hero h1{font-family:'Cormorant Garamond',serif;font-size:clamp(50px,7vw,84px);margin:0}.hero p{max-width:760px;line-height:1.7;color:#efe7db}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;padding:24px 0 60px}.card{padding:24px;border-radius:20px;background:rgba(248,243,234,.16);backdrop-filter:blur(7px);border:1px solid rgba(255,255,255,.12);box-shadow:0 14px 30px rgba(0,0,0,.10)}.card h3{font-family:'Cormorant Garamond',serif;font-size:34px;margin:0 0 12px}.card p{line-height:1.65;color:#f2ece4;font-size:14px}.card strong{color:#e2ca88}@media(max-width:900px){.grid{grid-template-columns:1fr}}</style></head><body><div class="bg"></div><div class="shade"></div><div class="container"><div class="top"><div class="logo">BRUGAFI</div><a href="/">← Volver</a></div><section class="hero"><h1>{{collection.title}}</h1><p>Explora los perfiles olfativos de esta colección.</p></section><section class="grid">{% for item in collection['items'] %}<article class="card"><h3>{{item.name}}</h3><p><strong>Perfil:</strong> {{item.profile}}</p><p><strong>Notas olfativas:</strong> {{item.notes}}</p><p><strong>Inspiración:</strong> {{item.inspiration}}</p></article>{% endfor %}</section></div></body></html>"""

LEGAL_PAGE = r"""
<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="preload" as="image" href="/static/img/fondos/main.webp" fetchpriority="high"><title>{{title}} | BRUGAFI</title><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"><style>*{box-sizing:border-box}body{margin:0;background:#080808;color:#eee;font-family:Inter,sans-serif}.shell{width:min(900px,calc(100% - 32px));margin:38px auto;border:1px solid #C8B273;padding:10px}.inner{border:1px solid rgba(200,178,115,.42);padding:38px}.logo{font-family:'Cormorant Garamond',serif;font-size:32px;letter-spacing:.14em;color:#e0c77e}h1{font-family:'Cormorant Garamond',serif;font-size:52px;margin:34px 0 22px}p{white-space:pre-line;line-height:1.85;color:#d9d2c6}a{color:#e0c77e;text-decoration:none}@media(max-width:600px){.inner{padding:24px}h1{font-size:40px}}</style></head><body><div class="shell"><div class="inner"><a class="logo" href="/">BRUGAFI</a><h1>{{title}}</h1><p>{{content}}</p><p><a href="/">← Regresar a brugafi.homes</a></p></div></div></body></html>"""


@app.after_request
def add_cache_headers(response):
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    return response

@app.context_processor
def globals_(): return {"year": datetime.now().year}

@app.route('/')
def home(): return render_template_string(HOME,brand=BRAND,collections=COLLECTIONS,diffusers=DIFFUSERS,products=PRODUCTS,faqs=FAQS,year=datetime.now().year)

@app.route('/coleccion/<slug>')
def collection(slug):
    c=next((x for x in COLLECTIONS if x['slug']==slug),None)
    if not c: abort(404)
    return render_template_string(COLLECTION_PAGE,collection=c)

@app.route('/aviso-privacidad')
def privacy(): return render_template_string(LEGAL_PAGE,title='Aviso de privacidad',content=PRIVACY)
@app.route('/terminos')
def terms(): return render_template_string(LEGAL_PAGE,title='Términos del servicio',content=TERMS)
@app.route('/legal')
def legal(): return render_template_string(LEGAL_PAGE,title='Legal',content=LEGAL)
@app.route('/politicas-envio')
def shipping(): return render_template_string(LEGAL_PAGE,title='Políticas de envío',content=SHIPPING)
@app.route('/health')
def health(): return 'ok',200
if __name__=='__main__': app.run(debug=True)
