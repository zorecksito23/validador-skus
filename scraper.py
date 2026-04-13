import requests
import time
from googlesearch import search

# PEGA TU URL DE APPS SCRIPT AQUÍ ADENTRO DE LAS COMILLAS
WEBAPP_URL = "TU_URL_DE_APPS_SCRIPT_AQUI"

def process_skus():
    # 1. GitHub le pregunta a tu Google Sheet: "¿Qué filas faltan?"
    print("Obteniendo SKUs pendientes...")
    response = requests.get(WEBAPP_URL)
    pendientes = response.json()
    
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
                modelo_validado = sku # Si hay link, el modelo está correcto
                break
        except Exception as e:
            print(f"Error al buscar: {e}")
            time.sleep(10) # Si Google se enoja, esperamos 10 segundos

        # 3. GitHub le manda el resultado de vuelta a tu Google Sheet
        payload = {
            "row": row,
            "validado": modelo_validado,
            "link": link_coincidencia
        }
        requests.post(WEBAPP_URL, json=payload)
        
        # Pausa obligatoria para que Google no nos detecte como robot
        time.sleep(3) 

if __name__ == "__main__":
    process_skus()
