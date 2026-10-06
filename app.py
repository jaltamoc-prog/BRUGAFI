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
        "description": "Presentación ideal para descubrir un aroma, rotarlo por temporada o mantener espacios de uso moderado.",
        "price": "TODO REEMPLAZAR",
        "stripe_url": STRIPE_LINKS["bottle_250"],
        "available": is_real_checkout(STRIPE_LINKS["bottle_250"]),
        "image_file": "img/fragancia-250-brugafi.png"
    },
    {
        "size": "450 ml",
        "description": "Opción recomendada para mayor continuidad aromática y espacios con uso más frecuente.",
        "price": "TODO REEMPLAZAR",
        "stripe_url": STRIPE_LINKS["bottle_450"],
        "available": is_real_checkout(STRIPE_LINKS["bottle_450"]),
        "image_file": "img/fragancia-450-brugafi.png"
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
        "title": "Colección Exclusiva",
        "intro": "Una selección BRUGAFI de carácter elegante, contemporáneo y personal.",
        "items": [
            {"name": "AVEL", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI."},
            {"name": "VAREN", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI."},
            {"name": "ELARA", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI."},
            {"name": "AMBREL", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI."},
            {"name": "LÉVAN", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI."},
            {"name": "NOXEN", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI."},
            {"name": "ORVAN", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI."},
            {"name": "ALVÉ", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI."},
            {"name": "SOREN", "profile": "Por confirmar", "notes": "Completar ficha olfativa.", "mood": "Colección exclusiva BRUGAFI."},
        ]
    },
    {
        "title": "Colección Hoteles",
        "intro": "Inspiración sensorial en grandes destinos, lobbies elegantes, spas costeros y estancias memorables.",
        "items": [
            {"name": "AUREN", "profile": "Neutro · Floral", "notes": "Orquídea, flores blancas, sándalo, incienso", "mood": "Elegancia serena, sobria y envolvente."},
            {"name": "VÉRIN", "profile": "Cítrico", "notes": "Green tea, algodón", "mood": "Limpieza luminosa y sofisticación ligera."},
            {"name": "NALÉ", "profile": "Cítrico", "notes": "Lima, bambú, flor de loto, cedro, vainilla", "mood": "Frescura verde con fondo suave y refinado."},
            {"name": "ORIEN", "profile": "Neutro", "notes": "Higo, almendra, ámbar, cedro, almizcle", "mood": "Calidez elegante con profundidad reconfortante."},
            {"name": "ZÉVOR", "profile": "Neutro", "notes": "Bergamota, rosa de damasco, orquídea, oud, ámbar, sándalo", "mood": "Lujo intenso, exótico y distinguido."},
            {"name": "LUREN", "profile": "Cítrico · Floral", "notes": "Lemongrass, almizcle, flores frescas, citrus", "mood": "Vitalidad limpia y fresca."},
            {"name": "AVIOR", "profile": "Cítrico · Amaderado", "notes": "Vetiver, naranja amarga, toronja roja", "mood": "Energía cítrica con elegancia mediterránea."},
            {"name": "EIRAN", "profile": "Floral · Ambarado", "notes": "Almizcle, tonka, ámbar gris, toronja, cassis, rosa, azahar", "mood": "Sensualidad cálida y floral."},
            {"name": "SAVEN", "profile": "Verde · Cítrico", "notes": "Galbano, tomillo, limón, violeta, rosa, cedro", "mood": "Frescura botánica distinguida."},
            {"name": "NERÉ", "profile": "Aromático · Fresco", "notes": "Menta, lavanda, eucalipto, toques cítricos", "mood": "Claridad fresca y relajante."},
            {"name": "VALEN", "profile": "Herbal · Fresco", "notes": "Eucalipto, menta americana, lavanda, toques cítricos", "mood": "Impulso revitalizante."},
            {"name": "ÉVORA", "profile": "Frutal · Floral", "notes": "Manzana, frambuesa, pomelo, cedro blanco, mezclas florales", "mood": "Carácter alegre y moderno."},
            {"name": "ARDEL", "profile": "Floral · Almizclado", "notes": "Lirio, jazmín, melón verde, anís, almizcle", "mood": "Suavidad pulcra y luminosa."},
        ]
    },
    {
        "title": "Colección Tiendas",
        "intro": "Inspiración sensorial en boutiques contemporáneas, espacios curados y ambientes sofisticados.",
        "items": [
            {"name": "VEYRA", "profile": "Amaderado", "notes": "Herbal, musgo, cedro, ámbar", "mood": "Calidez con carácter y profundidad."},
            {"name": "ÉLION", "profile": "Neutro", "notes": "Té blanco, tomillo", "mood": "Limpieza sofisticada y calma contemporánea."}
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
     "Sí. Hay presentaciones de 250 ml y 450 ml, además de paquetes anuales con difusor."),
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
.hero-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:28px}
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
@media(max-width:900px){
  .hero-grid,.grid3,.grid2,.scent-grid{grid-template-columns:1fr}
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
        <div class="point"><strong>250 ml y 450 ml</strong>Compra fragancias por frasco o en paquete anual.</div>
        <div class="point"><strong>Fórmula cuidada</strong>Fragancias libres de ftalatos y parabenos.</div>
      </div>
    </div>
    <div class="brand-panel">
      <div class="label">
        <div class="b">BRUGAFI</div>
        <div class="s">Home Fragrance</div>
        <br><br>
        <div class="s">Scent a Beautiful Life</div>
      </div>
    </div>
  </div>
</div>

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
    <p>Presentaciones de 250 ml y 450 ml. Libres de ftalatos y parabenos.</p>
  </div>
  <div class="grid2">
  {% for b in bottles %}
    <article class="card">
      <div class="media">
        <img src="/static/{{ b.image_file }}" alt="Fragancia BRUGAFI {{ b.size }}" onerror="this.style.display='none';this.parentElement.innerHTML='Agregar botella BRUGAFI con etiqueta cuadrada';">
      </div>
      <div class="content">
        <span class="kicker">{{ b.size }}</span>
        <h3>Fragancia premium</h3>
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

<section id="colecciones">
<div class="container">
  <div class="section-head">
    <h2>Colecciones aromáticas</h2>
    <p>La inspiración se comunica por sensaciones, perfiles y notas olfativas, sin depender de mencionar textualmente hoteles o tiendas.</p>
  </div>
  {% for c in collections %}
  <div class="collection">
    <h3>{{ c.title }}</h3>
    <p>{{ c.intro }}</p>
    <div class="scent-grid">
    {% for s in c.items %}
      <div class="scent">
        <h4>{{ s.name }}</h4>
        <p><strong>Perfil:</strong> {{ s.profile }}<br><strong>Notas:</strong> {{ s.notes }}<br><strong>Sensación:</strong> {{ s.mood }}</p>
      </div>
    {% endfor %}
    </div>
  </div>
  {% endfor %}
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

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True)
