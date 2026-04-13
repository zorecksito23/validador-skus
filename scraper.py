import requests
import time
from googlesearch import search

# Tu URL de Apps Script ya configurada
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbxSdlfQxwaReBLO_mw0MD5KLPBoPvzc4INUk9UT9k955A81cjhz3sXVhkpHZXHLVM3t/exec"

def process_skus():
    # 1. GitHub le pregunta a tu Google Sheet: "¿Qué filas faltan por buscar?"
    print("Obteniendo SKUs pendientes...")
    try:
        response = requests.get(WEBAPP_URL)
        response.raise_for_status() # Verifica si hay errores de conexión
        pendientes = response.json()
    except Exception as e:
        print(f"Error al conectar con Google Sheets: {e}")
        return
    
    print(f"Se encontraron {len(pendientes)} SKUs para validar.")

    for item in pendientes:
        row = item['row']
        sku = item['sku']
        print(f"Buscando fila {row}: {sku}")

        link_coincidencia = "no encontrado"
        modelo_validado = "no encontrado"

        try:
            # 2. Busca en Google la coincidencia exacta
            query = f'"{sku}"'
            for url in search(query, num_results=1, sleep_interval=5):
                link_coincidencia = url
                modelo_validado = sku # Si hay link, el modelo existe y está correcto
                break
        except Exception as e:
            print(f"Error al buscar en Google: {e}")
            time.sleep(10) # Si Google se pone estricto, esperamos 10 segundos

        # 3. GitHub manda el resultado de vuelta a tu Google Sheet
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
        
        # Pausa de 3 segundos obligatoria para no saturar a Google
        time.sleep(3) 

if __name__ == "__main__":
    process_skus()
