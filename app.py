from flask import Flask, render_template_string, abort
from datetime import datetime

app = Flask(__name__)

BRAND = {
    "name": "BRUGAFI",
    "tagline": "Scent a Beautiful Life",
    "subtag": "Home Fragrance",
    "domain": "brugafi.homes",
    "email": "hola@brugafi.homes",  # TODO: reemplazar si usarás otro correo
    "colors": {
        "rich_gold": "#C8B273",
        "moonless_night": "#0A0A0C",
        "ivory": "#F7F3EC",
        "sand": "#EDE5D8",
        "warm_gray": "#756E63",
        "text": "#1E1C19"
    }
}

STRIPE_LINKS = {
    "diffuser_a45": "#",
    "diffuser_a70": "#",
    "diffuser_a140": "#",
    "bottle_250": "#",
    "bottle_450": "#",
    "annual_a45": "#",
    "annual_a70": "#",
    "annual_a140": "#"
}

def is_real_checkout(url: str) -> bool:
    return bool(url and url.startswith("https://"))

DIFFUSERS = [
    {
        "code": "A45",
        "title": "Difusor profesional eléctrico de aromas",
        "coverage": "Hasta 45 m²",
        "description": "Diseñado para recámaras, estudios, consultorios, oficinas privadas y espacios íntimos.",
        "features": [
            "Control desde app móvil",
            "Programación de horarios",
            "Ajuste de intensidad",
            "Difusión profesional de aceite",
            "Ideal para hogar y oficina",
            "Compatible con fragancias BRUGAFI"
        ],
        "price": "TODO REEMPLAZAR",
        "stripe_url": STRIPE_LINKS["diffuser_a45"],
        "available": is_real_checkout(STRIPE_LINKS["diffuser_a45"]),
        "image_file": "img/difusor-a45-brugafi.png"
    },
    {
        "code": "A70",
        "title": "Difusor profesional eléctrico de aromas",
        "coverage": "Hasta 70 m²",
        "description": "Pensado para áreas sociales, salas, recepciones pequeñas, oficinas y espacios de convivencia.",
        "features": [
            "Control desde app móvil",
            "Programación de horarios",
            "Ajuste de intensidad",
            "Difusión profesional de aceite",
            "Uso residencial y profesional",
            "Compatible con fragancias BRUGAFI"
        ],
        "price": "TODO REEMPLAZAR",
        "stripe_url": STRIPE_LINKS["diffuser_a70"],
        "available": is_real_checkout(STRIPE_LINKS["diffuser_a70"]),
        "image_file": "img/difusor-a70-brugafi.png"
    },
    {
        "code": "A140",
        "title": "Difusor profesional eléctrico de aromas",
        "coverage": "Hasta 140 m²",
        "description": "Para salas grandes, showrooms, boutiques, oficinas y zonas abiertas de atención.",
        "features": [
            "Control desde app móvil",
            "Programación de horarios",
            "Ajuste de intensidad",
            "Difusión profesional de aceite",
            "Mayor cobertura",
            "Compatible con fragancias BRUGAFI"
        ],
        "price": "TODO REEMPLAZAR",
        "stripe_url": STRIPE_LINKS["diffuser_a140"],
        "available": is_real_checkout(STRIPE_LINKS["diffuser_a140"]),
        "image_file": "img/difusor-a140-brugafi.png"
    }
]

BOTTLES = [
    {
        "size": "250 ml",
        "title": "Aceite para difusor",
        "description": "Aceite aromático BRUGAFI para uso en difusores profesionales.",
        "price": "TODO REEMPLAZAR",
        "stripe_url": "#",
        "available": False,
        "image_file": "img/aceite-difusor-250-brugafi.png"
    },
    {
        "size": "150 ml",
        "title": "Fragancia para textiles",
        "description": "Fragancia BRUGAFI para textiles en presentación de 150 ml.",
        "price": "TODO REEMPLAZAR",
        "stripe_url": "#",
        "available": False,
        "image_file": "img/fragancia-textil-150-brugafi.png"
    },
    {
        "size": "350 ml",
        "title": "Fragancia para textiles",
        "description": "Fragancia BRUGAFI para textiles en presentación de 350 ml.",
        "price": "TODO REEMPLAZAR",
        "stripe_url": "#",
        "available": False,
        "image_file": "img/fragancia-textil-350-brugafi.png"
    }
]

ANNUAL_PACKAGES = [
    {
        "name": "Experiencia Anual A45",
        "coverage": "Hasta 45 m²",
        "price": "TODO REEMPLAZAR",
        "stripe_url": STRIPE_LINKS["annual_a45"],
        "available": is_real_checkout(STRIPE_LINKS["annual_a45"])
    },
    {
        "name": "Experiencia Anual A70",
        "coverage": "Hasta 70 m²",
        "price": "TODO REEMPLAZAR",
        "stripe_url": STRIPE_LINKS["annual_a70"],
        "available": is_real_checkout(STRIPE_LINKS["annual_a70"])
    },
    {
        "name": "Experiencia Anual A140",
        "coverage": "Hasta 140 m²",
        "price": "TODO REEMPLAZAR",
        "stripe_url": STRIPE_LINKS["annual_a140"],
        "available": is_real_checkout(STRIPE_LINKS["annual_a140"])
    }
]

COLLECTIONS = [
    {
        "slug":"exclusiva","title": "Colección Exclusiva","cover_image":"img/colecciones/exclusiva.jpg",
        "intro": "Una selección BRUGAFI de carácter elegante, contemporáneo y personal.",
        "items": [
            {"name": "AVEL", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI.", "image_file":"img/aromas/avel.jpg", "stripe_url":"#"},
            {"name": "VAREN", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI.", "image_file":"img/aromas/varen.jpg", "stripe_url":"#"},
            {"name": "ELARA", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI.", "image_file":"img/aromas/elara.jpg", "stripe_url":"#"},
            {"name": "AMBREL", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI.", "image_file":"img/aromas/ambrel.jpg", "stripe_url":"#"},
            {"name": "LÉVAN", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI.", "image_file":"img/aromas/levan.jpg", "stripe_url":"#"},
            {"name": "NOXEN", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI.", "image_file":"img/aromas/noxen.jpg", "stripe_url":"#"},
            {"name": "ORVAN", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI.", "image_file":"img/aromas/orvan.jpg", "stripe_url":"#"},
            {"name": "ALVÉ", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI.", "image_file":"img/aromas/alve.jpg", "stripe_url":"#"},
            {"name": "SOREN", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI.", "image_file":"img/aromas/soren.jpg", "stripe_url":"#"},
        ]
    },
    {
        "slug":"hoteles","title": "Colección Hoteles","cover_image":"img/colecciones/hoteles.jpg",
        "intro": "Inspiración sensorial en grandes destinos, lobbies elegantes, spas costeros y estancias memorables.",
        "items": [
            {"name": "AUREN", "profile": "Neutro · Floral", "notes": "Orquídea, flores blancas, sándalo, incienso", "mood": "Elegancia serena, sobria y envolvente.", "image_file":"img/aromas/auren.jpg", "stripe_url":"#"},
            {"name": "VÉRIN", "profile": "Cítrico", "notes": "Green tea, algodón", "mood": "Limpieza luminosa y sofisticación ligera.", "image_file":"img/aromas/verin.jpg", "stripe_url":"#"},
            {"name": "NALÉ", "profile": "Cítrico", "notes": "Lima, bambú, flor de loto, cedro, vainilla", "mood": "Frescura verde con fondo suave y refinado.", "image_file":"img/aromas/nale.jpg", "stripe_url":"#"},
            {"name": "ORIEN", "profile": "Neutro", "notes": "Higo, almendra, ámbar, cedro, almizcle", "mood": "Calidez elegante con profundidad reconfortante.", "image_file":"img/aromas/orien.jpg", "stripe_url":"#"},
            {"name": "ZÉVOR", "profile": "Neutro", "notes": "Bergamota, rosa de damasco, orquídea, oud, ámbar, sándalo", "mood": "Lujo intenso, exótico y distinguido.", "image_file":"img/aromas/zevor.jpg", "stripe_url":"#"},
            {"name": "LUREN", "profile": "Cítrico · Floral", "notes": "Lemongrass, almizcle, flores frescas, citrus", "mood": "Vitalidad limpia y fresca.", "image_file":"img/aromas/luren.jpg", "stripe_url":"#"},
            {"name": "AVIOR", "profile": "Cítrico · Amaderado", "notes": "Vetiver, naranja amarga, toronja roja", "mood": "Energía cítrica con elegancia mediterránea.", "image_file":"img/aromas/avior.jpg", "stripe_url":"#"},
            {"name": "EIRAN", "profile": "Floral · Ambarado", "notes": "Almizcle, tonka, ámbar gris, toronja, cassis, rosa, azahar", "mood": "Sensualidad cálida y floral.", "image_file":"img/aromas/eiran.jpg", "stripe_url":"#"},
            {"name": "SAVEN", "profile": "Verde · Cítrico", "notes": "Galbano, tomillo, limón, violeta, rosa, cedro", "mood": "Frescura botánica distinguida.", "image_file":"img/aromas/saven.jpg", "stripe_url":"#"},
            {"name": "NERÉ", "profile": "Aromático · Fresco", "notes": "Menta, lavanda, eucalipto, toques cítricos", "mood": "Claridad fresca y relajante.", "image_file":"img/aromas/nere.jpg", "stripe_url":"#"},
            {"name": "VALEN", "profile": "Herbal · Fresco", "notes": "Eucalipto, menta americana, lavanda, toques cítricos", "mood": "Impulso revitalizante.", "image_file":"img/aromas/valen.jpg", "stripe_url":"#"},
            {"name": "ÉVORA", "profile": "Frutal · Floral", "notes": "Manzana, frambuesa, pomelo, cedro blanco, mezclas florales", "mood": "Carácter alegre y moderno.", "image_file":"img/aromas/evora.jpg", "stripe_url":"#"},
            {"name": "ARDEL", "profile": "Floral · Almizclado", "notes": "Lirio, jazmín, melón verde, anís, almizcle", "mood": "Suavidad pulcra y luminosa.", "image_file":"img/aromas/ardel.jpg", "stripe_url":"#"},
        ]
    },
    {
        "slug":"tiendas","title": "Colección Tiendas","cover_image":"img/colecciones/tiendas.jpg",
        "intro": "Inspiración sensorial en boutiques contemporáneas, espacios curados y ambientes sofisticados.",
        "items": [
            {"name": "VEYRA", "profile": "Amaderado", "notes": "Herbal, musgo, cedro, ámbar", "mood": "Calidez con carácter y profundidad.", "image_file":"img/aromas/veyra.jpg", "stripe_url":"#"},
            {"name": "ÉLION", "profile": "Neutro", "notes": "Té blanco, tomillo", "mood": "Limpieza sofisticada y calma contemporánea.", "image_file":"img/aromas/elion.jpg", "stripe_url":"#"}
        ]
    }
]

FAQS = [
    ("¿Qué diferencia a BRUGAFI de un aromatizante convencional?",
     "BRUGAFI utiliza difusión profesional de aceite para lograr una presencia aromática más uniforme, elegante y memorable."),
    ("¿Las fragancias contienen ftalatos o parabenos?",
     "No. Las fragancias BRUGAFI se comunican como libres de ftalatos y parabenos."),
    ("¿Puedo controlar el difusor desde mi celular?",
     "Sí. Los difusores BRUGAFI pueden configurarse desde una app móvil para administrar horarios de funcionamiento y ajustar la intensidad de difusión."),
    ("¿Puedo comprar solo la fragancia?",
     "Sí. Tenemos aceite para difusor en 250 ml y fragancias para textiles en 150 ml y 350 ml, además de paquetes anuales con difusor."),
    ("¿Cómo pago?",
     "El pago se realizará mediante Stripe cuando se agreguen las ligas reales de checkout.")
]

HOME_TEMPLATE = r"""
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ brand.name }} | Difusores profesionales y fragancias premium</title>
<meta name="description" content="Difusores profesionales de aceite para hogar y oficina. Fragancias premium libres de ftalatos y parabenos.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --gold: {{ brand.colors.rich_gold }};
  --night: {{ brand.colors.moonless_night }};
  --ivory: {{ brand.colors.ivory }};
  --sand: {{ brand.colors.sand }};
  --gray: {{ brand.colors.warm_gray }};
  --text: {{ brand.colors.text }};
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:Inter,sans-serif;color:var(--text);background:#faf7f1}
a{text-decoration:none;color:inherit}
.container{width:min(1180px,calc(100% - 32px));margin:auto}
header{position:sticky;top:0;z-index:20;background:rgba(250,247,241,.9);backdrop-filter:blur(12px);border-bottom:1px solid rgba(0,0,0,.06)}
nav{display:flex;justify-content:space-between;align-items:center;padding:16px 0;gap:22px}
.logo{font-family:"Cormorant Garamond",serif;font-size:32px;letter-spacing:.12em}
.links{display:flex;gap:18px;flex-wrap:wrap;font-size:14px}
.hero{padding:52px 0}
.hero-grid{display:grid;grid-template-columns:1fr;gap:28px}
.hero-copy,.brand-panel{border-radius:28px;min-height:590px}
.hero-copy{padding:54px;background:#fff;display:flex;flex-direction:column;justify-content:center;box-shadow:0 18px 45px rgba(0,0,0,.06)}
.eyebrow{font-size:13px;text-transform:uppercase;letter-spacing:.12em;color:#75632f;font-weight:700}
h1,h2{font-family:"Cormorant Garamond",serif;color:var(--night)}
h1{font-size:clamp(52px,7vw,86px);line-height:.95;margin:18px 0}
.lead{font-size:18px;line-height:1.75;color:#5a544b}
.btn{display:inline-flex;padding:14px 22px;border-radius:999px;font-weight:700}
.btn-dark{background:var(--night);color:#fff}
.btn-outline{border:1px solid rgba(0,0,0,.15)}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.hero-points{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:28px}
.point{padding:16px;border-radius:16px;background:#f8f4ec}
.point strong{display:block;margin-bottom:5px}
.brand-panel{background:var(--night);padding:34px;color:#fff;display:flex;align-items:center;justify-content:center}
.label{width:100%;padding:42px 24px;border:1px solid var(--gold);outline:1px solid var(--gold);outline-offset:-12px;text-align:center}
.label .b{font-family:"Cormorant Garamond",serif;color:#dcc77f;font-size:clamp(58px,7vw,96px);letter-spacing:.08em}
.label .s{color:#dcc77f;text-transform:uppercase;letter-spacing:.28em}
section{padding:82px 0}
.section-head{display:flex;justify-content:space-between;gap:24px;align-items:end;margin-bottom:28px;flex-wrap:wrap}
.section-head h2{font-size:48px;margin:0}
.section-head p{max-width:650px;color:#5e584f;line-height:1.7}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.card{background:#fff;border-radius:24px;overflow:hidden;box-shadow:0 14px 36px rgba(0,0,0,.06);border:1px solid rgba(0,0,0,.05)}
.media{height:285px;background:#f3eee5;display:flex;align-items:center;justify-content:center;padding:22px;text-align:center;color:#777}
.media img{max-width:100%;max-height:245px;object-fit:contain}
.content{padding:26px}
.kicker{display:inline-block;background:rgba(200,178,115,.18);padding:8px 12px;border-radius:999px;font-size:12px;font-weight:700}
.content h3{margin:14px 0 8px}
.content p,.content li{color:#5f584f;line-height:1.7}
.content ul{padding-left:20px}
.price{font-weight:700;margin:16px 0}
.disabled{background:#d7d2c9;color:#777;pointer-events:none}
.collection{background:#fff;border-radius:28px;padding:30px;margin-bottom:22px;box-shadow:0 14px 36px rgba(0,0,0,.05)}
.scent-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.scent{padding:18px;border-radius:18px;background:#faf7f1;border:1px solid rgba(0,0,0,.05)}
.scent h4{margin:0 0 10px;font-size:20px}
.scent p{font-size:14px;line-height:1.6;color:#5f584f}
.promise{background:var(--night);color:#eee5d7;border-radius:28px;padding:42px}
.promise h2{color:#dcc77f;margin-top:0}
.faq{background:#fff;border-radius:18px;padding:20px;margin-bottom:12px}
footer{padding:40px 0 60px;border-top:1px solid rgba(0,0,0,.08)}
footer p{color:#6b645a}

.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.best-card .media{height:260px}
.best-card .media img{width:100%;height:100%;object-fit:cover;border-radius:12px}
.collection-gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.collection-tile{position:relative;border-radius:26px;overflow:hidden;min-height:360px;display:block;box-shadow:0 14px 36px rgba(0,0,0,.06);background:#d8cfbf}
.collection-tile img{width:100%;height:100%;object-fit:cover;display:block}
.collection-overlay{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;background:linear-gradient(180deg,rgba(0,0,0,.12),rgba(0,0,0,.30));padding:22px}
.collection-overlay h3{color:#fff;font-size:2rem;line-height:1.1;margin:0}
@media(max-width:1100px){.grid4,.collection-gallery{grid-template-columns:1fr 1fr}}
@media(max-width:900px){
  .hero-grid,.grid3,.grid2,.scent-grid,.grid4,.collection-gallery{grid-template-columns:1fr}
  .hero-points{grid-template-columns:1fr}
  .hero-copy,.brand-panel{min-height:auto}
  .links{display:none}
}
</style>
</head>
<body>
<header>
  <div class="container">
    <nav>
      <div class="logo">BRUGAFI</div>
      <div class="links">
        <a href="#difusores">Difusores</a>
        <a href="#fragancias">Fragancias</a>
        <a href="#paquetes">Paquetes anuales</a>
        <a href="#colecciones">Colecciones</a>
      </div>
    </nav>
  </div>
</header>

<div class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      <div class="eyebrow">Difusión profesional para hogar y oficina</div>
      <h1>Haz que tu espacio se sienta extraordinario.</h1>
      <p class="lead">Difusores profesionales de aceite y fragancias premium con una inspiración sensorial de hospitalidad, boutiques y perfumería de lujo.</p>
      <div class="actions">
        <a class="btn btn-dark" href="#difusores">Descubrir la experiencia</a>
        <a class="btn btn-outline" href="#colecciones">Explorar aromas</a>
      </div>
      <div class="hero-points">
        <div class="point"><strong>Control desde tu celular</strong>Programa horarios y ajusta la intensidad desde una app móvil.</div>
        <div class="point"><strong>45, 70 y 140 m²</strong>Elige el difusor según el tamaño de tu espacio.</div>
        <div class="point"><strong>250 ml · 150 ml · 350 ml</strong>Aceite para difusor y fragancias para textiles.</div>
        <div class="point"><strong>Fórmula cuidada</strong>Fragancias libres de ftalatos y parabenos.</div>
      </div>
    </div>
</div>
</div>

<section id="colecciones">
<div class="container">
  <div class="section-head">
    <h2>Colecciones</h2>
    <p>Explora cada colección visualmente. Al dar clic se abre una nueva ventana con todos los aromas de esa línea.</p>
  </div>
  <div class="collection-gallery">
    {% for c in collections %}
    <a class="collection-tile" href="/coleccion/{{ c['slug'] }}" target="_blank">
      <img src="/static/{{ c['cover_image'] }}" alt="{{ c['title'] }}" onerror="this.style.display='none';">
      <div class="collection-overlay"><h3>{{ c['title'] }}</h3></div>
    </a>
    {% endfor %}
  </div>
</div>
</section>

<section id="difusores">
<div class="container">
  <div class="section-head">
    <h2>Elige tu difusor</h2>
    <p>Controla horarios e intensidad desde tu celular y crea una experiencia aromática constante, elegante y personalizada.</p>
  </div>
  <div class="grid3">
  {% for d in diffusers %}
    <article class="card">
      <div class="media">
        <img src="/static/{{ d.image_file }}" alt="{{ d.code }}" onerror="this.style.display='none';this.parentElement.innerHTML='Agregar imagen BRUGAFI del {{ d.code }}';">
      </div>
      <div class="content">
        <span class="kicker">{{ d.code }}</span>
        <h3>{{ d.coverage }}</h3>
        <p>{{ d.description }}</p>
        <ul>{% for f in d.features %}<li>{{ f }}</li>{% endfor %}</ul>
        <div class="price">Precio: {{ d.price }}</div>
        {% if d.available %}
          <a class="btn btn-dark" href="{{ d.stripe_url }}" target="_blank">Quiero esta sensación en mi espacio</a>
        {% else %}
          <span class="btn disabled">Agregar liga Stripe</span>
        {% endif %}
      </div>
    </article>
  {% endfor %}
  </div>
</div>
</section>

<section id="fragancias">
<div class="container">
  <div class="section-head">
    <h2>Fragancias BRUGAFI</h2>
    <p>Aceite para difusor en 250 ml y fragancias para textiles en 150 ml y 350 ml. Libres de ftalatos y parabenos.</p>
  </div>
  <div class="grid2">
  {% for b in bottles %}
    <article class="card">
      <div class="media">
        <img src="/static/{{ b.image_file }}" alt="Fragancia BRUGAFI {{ b.size }}" onerror="this.style.display='none';this.parentElement.innerHTML='Agregar botella BRUGAFI con etiqueta cuadrada';">
      </div>
      <div class="content">
        <span class="kicker">{{ b.size }}</span>
        <h3>{{ b.title }}</h3>
        <p>{{ b.description }}</p>
        <p><strong>Libre de ftalatos y parabenos.</strong></p>
        <div class="price">Precio: {{ b.price }}</div>
        {% if b.available %}
          <a class="btn btn-dark" href="{{ b.stripe_url }}" target="_blank">Quiero vivir esta sensación</a>
        {% else %}
          <span class="btn disabled">Agregar liga Stripe</span>
        {% endif %}
      </div>
    </article>
  {% endfor %}
  </div>
</div>
</section>

<section id="paquetes">
<div class="container">
  <div class="section-head">
    <h2>Experiencia anual</h2>
    <p>Difusor + abastecimiento de fragancia para mantener tu espacio acompañado por BRUGAFI durante todo el año.</p>
  </div>
  <div class="grid3">
  {% for p in packages %}
    <article class="card">
      <div class="content">
        <span class="kicker">{{ p.coverage }}</span>
        <h3>{{ p.name }}</h3>
        <p>Paquete anual con difusor y fragancia. La cantidad exacta de aceite se definirá antes de publicar el precio final.</p>
        <div class="price">Precio: {{ p.price }}</div>
        {% if p.available %}
          <a class="btn btn-dark" href="{{ p.stripe_url }}" target="_blank">Quiero que mi espacio se sienta así todo el año</a>
        {% else %}
          <span class="btn disabled">Agregar liga Stripe</span>
        {% endif %}
      </div>
    </article>
  {% endfor %}
  </div>
</div>
</section>





<section>
<div class="container">
  <div class="promise">
    <h2>Una experiencia cuidada también en su formulación</h2>
    <p>Las fragancias BRUGAFI son libres de ftalatos y parabenos.</p>
  </div>
</div>
</section>

<section>
<div class="container">
  <div class="section-head"><h2>Preguntas frecuentes</h2></div>
  {% for q,a in faqs %}
    <div class="faq"><strong>{{ q }}</strong><p>{{ a }}</p></div>
  {% endfor %}
</div>
</section>

<footer>
<div class="container">
  <div class="logo">BRUGAFI</div>
  <p>Scent a Beautiful Life · {{ brand.domain }}</p>
  <p>© {{ year }} BRUGAFI. Todos los derechos reservados.</p>
</div>
</footer>
</body>
</html>
"""


COLLECTION_TEMPLATE = r"""
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ collection['title'] }} | BRUGAFI</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--gold:#C8B273;--night:#0A0A0C;--text:#1E1C19}
*{box-sizing:border-box}body{margin:0;font-family:Inter,sans-serif;background:#faf7f1;color:var(--text)}a{text-decoration:none;color:inherit}
.container{width:min(1180px,calc(100% - 32px));margin:auto}.header{padding:28px 0;border-bottom:1px solid rgba(0,0,0,.08);background:#fff}
.logo{font-family:"Cormorant Garamond",serif;font-size:34px;letter-spacing:.10em}.back{display:inline-block;margin-top:10px;color:#6f675d}
.hero{padding:60px 0 34px}.hero-grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:center}
.hero-image{border-radius:28px;overflow:hidden;min-height:420px;background:#eee}.hero-image img{width:100%;height:100%;object-fit:cover}
.hero-copy h1{font-family:"Cormorant Garamond",serif;font-size:58px;line-height:1;margin:0 0 16px}.hero-copy p{line-height:1.8;color:#5f584f;font-size:17px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;padding:24px 0 80px}.card{background:#fff;border-radius:24px;overflow:hidden;box-shadow:0 12px 30px rgba(0,0,0,.06)}
.media{height:260px;background:#f0ebe3;display:flex;align-items:center;justify-content:center;padding:18px;text-align:center;color:#777}.media img{width:100%;height:100%;object-fit:cover;border-radius:14px}
.content{padding:22px}.content h3{margin:0 0 10px}.content p{margin:0 0 10px;color:#5f584f;line-height:1.7}
.btn{display:inline-flex;padding:12px 18px;border-radius:999px;background:var(--night);color:#fff;font-weight:700;margin-top:10px}.disabled{background:#d7d2c9;color:#777}
@media(max-width:900px){.hero-grid,.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="header"><div class="container"><div class="logo">BRUGAFI</div><a class="back" href="/">← Volver al inicio</a></div></div>
<div class="hero"><div class="container hero-grid">
  <div class="hero-image"><img src="/static/{{ collection['cover_image'] }}" alt="{{ collection['title'] }}" onerror="this.style.display='none';this.parentElement.innerHTML='Agregar imagen de portada';"></div>
  <div class="hero-copy"><h1>{{ collection['title'] }}</h1><p>{{ collection['intro'] }}</p></div>
</div></div>
<div class="container"><div class="grid">
{% for s in collection['items'] %}
<article class="card">
  <div class="media"><img src="/static/{{ s['image_file'] }}" alt="{{ s['name'] }}" onerror="this.style.display='none';this.parentElement.innerHTML='Agregar imagen de {{ s['name'] }}';"></div>
  <div class="content">
    <h3>{{ s['name'] }}</h3>
    <p><strong>Perfil:</strong> {{ s['profile'] }}</p>
    <p><strong>Notas:</strong> {{ s['notes'] }}</p>
    <p><strong>Sensación:</strong> {{ s['mood'] }}</p>
    {% if s['stripe_url'].startswith('https://') %}<a class="btn" href="{{ s['stripe_url'] }}" target="_blank">Elegir este aroma</a>{% else %}<span class="btn disabled">Agregar liga Stripe</span>{% endif %}
  </div>
</article>
{% endfor %}
</div></div>
</body>
</html>
"""

@app.context_processor
def inject_globals():
    return {"year": datetime.now().year}

@app.route("/")
def home():
    return render_template_string(
        HOME_TEMPLATE,
        brand=BRAND,
        diffusers=DIFFUSERS,
        bottles=BOTTLES,
        packages=ANNUAL_PACKAGES,
        collections=COLLECTIONS,
        faqs=FAQS
    )

@app.route("/coleccion/<slug>")
def collection_detail(slug):
    collection = next((c for c in COLLECTIONS if c["slug"] == slug), None)
    if not collection:
        abort(404)
    return render_template_string(COLLECTION_TEMPLATE, brand=BRAND, collection=collection)

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True)
