import os

def recortar_imagen(ruta_imagen, x, y, ancho, alto):
    from PIL import Image

    # Verificar si la imagen existe
    if not os.path.exists(ruta_imagen):
        raise FileNotFoundError(f"La imagen {ruta_imagen} no existe.")

    # Abrir la imagen
    with Image.open(ruta_imagen) as img:
        # Recortar la imagen
        img_recortada = img.crop((x, y, x + ancho, y + alto))
        
        # Guardar la imagen recortada
        ruta_recortada = f"recortada_{os.path.basename(ruta_imagen)}"
        img_recortada.save(ruta_recortada)
        
        return ruta_recortada
    
# Ejemplo de uso
if __name__ == "__main__":
    ruta = "media/productos/default.png"
    #cortamos un poco de la parte inferior
    x, y, ancho, alto = 0, 0, 260, 260  # Coordenadas y dimensiones del recorte
    try:
        ruta_recortada = recortar_imagen(ruta, x, y, ancho, alto)
        print(f"Imagen recortada guardada en: {ruta_recortada}")
    except Exception as e:
        print(f"Error: {e}")