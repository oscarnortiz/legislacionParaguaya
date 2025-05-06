import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

leyes_df = pd.read_csv("data/leyes.csv", encoding="utf-8")
articulos = []

def normalizar_texto(t):
    return re.sub(r'\s+', ' ', t.strip())

# Nuevas expresiones regulares para detectar artículos
ARTICULO_RE = re.compile(
    r"^(ART[IÍ]CULO|Art\.?)\s*\.?\s*(\d+)[º°\.-]?\s*[-:]?\s*(.*)$",
    re.IGNORECASE
)

def parsear_articulos(parrafos, ley_id):
    articulos_extraidos = []
    i = 0
    while i < len(parrafos):
        texto = parrafos[i]
        match = ARTICULO_RE.match(texto)
        if match:
            nro = match.group(2)
            titulo = match.group(3).strip()
            contenido = titulo
            i += 1
            while i < len(parrafos):
                siguiente = parrafos[i]
                if ARTICULO_RE.match(siguiente):
                    break
                contenido += " " + siguiente.strip()
                i += 1
            articulos_extraidos.append({
                "ley": ley_id,
                "articulo": f"Artículo {nro}",
                "texto": contenido.strip()
            })
        else:
            i += 1
    return articulos_extraidos

for _, row in leyes_df.iterrows():
    ley_id = row["ley"]
    titulo = row["titulo"]
    url = row["url"]

    print(f"📖 Procesando: {ley_id} - {titulo}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"⚠️ Error al acceder a {url}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    descargar_headers = soup.find_all("h4")
    descargar_header = None
    for h4 in reversed(descargar_headers):
        strong = h4.find("strong")
        if strong and "descargar archivo" in strong.get_text(strip=True).lower():
            descargar_header = h4
            break

    if not descargar_header:
        print(f"⚠️ No se encontró 'Descargar Archivo' en {url}")
        continue

    contenido_html = []
    for elem in descargar_header.find_all_next():
        if elem.name == "footer" and "entry-footer" in elem.get("class", []):
            break
        if elem.name in ["p", "div"]:
            texto = elem.get_text(strip=True)
            if texto:
                contenido_html.append(texto)

    if not contenido_html:
        print(f"⚠️ No se encontró contenido posterior al encabezado en {url}")
        continue

    articulos_ley = parsear_articulos(contenido_html, ley_id)
    articulos.extend(articulos_ley)
    print(f"✅ {ley_id} procesada con {len(articulos_ley)} artículos acumulados.")
    time.sleep(1)

df = pd.DataFrame(articulos)
df.to_csv("data/articulos.csv", index=False)
print(f"\n📦 Listo. Se guardaron {len(df)} artículos en 'articulos.csv'")
