import requests
import time
from duckduckgo_search import DDGS

# Tu URL de Apps Script
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

    # Inicializamos el buscador anti-bloqueos
    ddgs = DDGS()

    for item in pendientes:
        row = item['row']
        sku = item['sku']
        print(f"Buscando fila {row}: {sku}")

        link_coincidencia = "no encontrado"
        modelo_validado = "no encontrado"

        try:
            # Buscamos la coincidencia exacta en la web
            query = f'"{sku}"'
            resultados = list(ddgs.text(query, max_results=1))
            
            # Si la lista de resultados no está vacía, extraemos el link
            if resultados:
                link_coincidencia = resultados[0]['href']
                modelo_validado = sku 
        except Exception as e:
            print(f"Error al buscar: {e}")
            time.sleep(5)

        # Mandamos el resultado de vuelta a Google Sheets
        payload = {
            "row": row,
            "validado": modelo_validado,
            "link": link_coincidencia
        }
        
        try:
            requests.post(WEBAPP_URL, json=payload)
            print(f"Resultado guardado en la fila {row}")
        except Exception as e:
            print(f"Error al guardar en Google Sheets: {e}")
        
        # Pausa de cortesía de 2 segundos
        time.sleep(2) 

if __name__ == "__main__":
    process_skus()
