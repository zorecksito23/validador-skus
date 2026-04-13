import requests
from bs4 import BeautifulSoup
import time

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbxSdlfQxwaReBLO_mw0MD5KLPBoPvzc4INUk9UT9k955A81cjhz3sXVhkpHZXHLVM3t/exec"

def process_skus():
    print("Obteniendo SKUs pendientes...")
    try:
        response = requests.get(WEBAPP_URL)
        response.raise_for_status()
        pendientes = response.json()
    except Exception as e:
        print(f"Error al conectar con Google Sheets: {e}")
        return
    
    print(f"Se encontraron {len(pendientes)} SKUs para validar.")

    # Cabeceras para simular que somos una persona en Google Chrome, no un bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    for item in pendientes:
        row = item['row']
        sku = item['sku']
        print(f"Buscando fila {row}: {sku}")

        link_coincidencia = "no encontrado"
        modelo_validado = "no encontrado"

        try:
            # Usamos DuckDuckGo Lite (versión sin bloqueos fuertes)
            url_search = "https://lite.duckduckgo.com/lite/"
            payload_search = {"q": f'"{sku}"'}
            
            # Hacemos la búsqueda
            res = requests.post(url_search, data=payload_search, headers=headers, timeout=15)
            
            # Leemos la página devuelta
            soup = BeautifulSoup(res.text, "html.parser")
            
            # Buscamos el primer link real que no sea del propio buscador
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('http') and 'duckduckgo.com' not in href:
                    link_coincidencia = href
                    modelo_validado = sku
                    break # Encontramos el primero, detenemos la búsqueda de links
                    
        except Exception as e:
            print(f"Error al buscar (Fila {row}): {e}")

        # Mandamos el resultado a tu Google Sheets
        payload_sheets = {
            "row": row,
            "validado": modelo_validado,
            "link": link_coincidencia
        }
        
        try:
            requests.post(WEBAPP_URL, json=payload_sheets)
            print(f"Guardado -> Fila {row} | Link: {link_coincidencia}")
        except Exception as e:
            print(f"Error al guardar en Sheets (Fila {row}): {e}")
        
        # Pausa obligatoria de 3 segundos para portarnos bien con el servidor
        time.sleep(3) 

if __name__ == "__main__":
    process_skus()
