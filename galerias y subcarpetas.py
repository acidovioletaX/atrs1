import os
from PIL import Image, ExifTags
from bs4 import BeautifulSoup

def corregir_orientacion(imagen):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(imagen._getexif().items())
        if exif[orientation] == 3:
            imagen = imagen.rotate(180, expand=True)
        elif exif[orientation] == 6:
            imagen = imagen.rotate(270, expand=True)
        elif exif[orientation] == 8:
            imagen = imagen.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # No se encuentra información EXIF
        pass
    return imagen

def redimensionar_y_ocupar_espacio(imagen, tamaño_objetivo):
    imagen.thumbnail(tamaño_objetivo, Image.LANCZOS)
    fondo = Image.new('RGB', tamaño_objetivo, (255, 255, 255))
    fondo.paste(imagen, (int((tamaño_objetivo[0] - imagen.size[0]) / 2), int((tamaño_objetivo[1] - imagen.size[1]) / 2)))
    return fondo

def redimensionar_imagenes(carpeta_imagenes, tamaño_por_defecto, carpeta_redimensionadas):
    if not os.path.exists(carpeta_redimensionadas):
        os.makedirs(carpeta_redimensionadas)
    imagenes_redimensionadas = {}

    for subcarpeta in os.listdir(carpeta_imagenes):
        ruta_subcarpeta = os.path.join(carpeta_imagenes, subcarpeta)
        if os.path.isdir(ruta_subcarpeta):
            archivos = [f for f in os.listdir(ruta_subcarpeta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if archivos:
                ruta_imagen = os.path.join(ruta_subcarpeta, archivos[0])
                try:
                    imagen = Image.open(ruta_imagen)
                    imagen = corregir_orientacion(imagen)
                    imagen_redimensionada = redimensionar_y_ocupar_espacio(imagen, tamaño_por_defecto)
                    nuevo_nombre = f"{subcarpeta}_{archivos[0]}"
                    ruta_imagen_redimensionada = os.path.join(carpeta_redimensionadas, nuevo_nombre)
                    imagen_redimensionada.save(ruta_imagen_redimensionada)
                    imagenes_redimensionadas[subcarpeta] = ruta_imagen_redimensionada
                    print(f"\033[34mImagen redimensionada guardada en: {ruta_imagen_redimensionada}\033[0m")
                except Exception as e:
                    print(f"\033[31mError procesando la imagen {ruta_imagen}: {e}\033[0m")
    return imagenes_redimensionadas

def procesar_html(ruta_html, imagenes_redimensionadas):
    with open(ruta_html, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    bloques = soup.select('.project-block-two')
    reemplazos = []

    for i, (subcarpeta, ruta_imagen_redimensionada) in enumerate(imagenes_redimensionadas.items()):
        if i < len(bloques):
            bloque = bloques[i]
            imagen_tag = bloque.find('img')
            titulo_tag = bloque.find('div', class_='title')

            if imagen_tag and titulo_tag:
                original_src = imagen_tag['src']
                nuevo_src = f"images/redimensionadas2/{os.path.basename(ruta_imagen_redimensionada)}"
                imagen_tag['src'] = nuevo_src
                titulo_tag.string = subcarpeta.replace("_", " ").title()
                reemplazos.append((original_src, nuevo_src, subcarpeta))
                print(f"\033[32mRuta de la imagen actualizada en el HTML: {original_src} -> {nuevo_src}\033[0m")

    ruta_nuevo_html = os.path.join(os.path.dirname(ruta_html), "PR.html")
    with open(ruta_nuevo_html, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"\033[32mHTML modificado guardado en: {ruta_nuevo_html}\033[0m")
    return reemplazos, ruta_nuevo_html

def main():
    ruta_html = input("Ingrese la ruta del archivo HTML a procesar: ")
    carpeta_imagenes = input("Ingrese la ruta de la carpeta con las subcarpetas de imágenes: ")
    carpeta_redimensionadas = os.path.join(carpeta_imagenes, 'redimensionadas2')
    tamaño_por_defecto = (630, 355)

    print(f"\033[32mPaso 1: Redimensionar imágenes\033[0m")
    imagenes_redimensionadas = redimensionar_imagenes(carpeta_imagenes, tamaño_por_defecto, carpeta_redimensionadas)

    print(f"\033[32mPaso 2: Actualizar el HTML\033[0m")
    reemplazos, ruta_nuevo_html = procesar_html(ruta_html, imagenes_redimensionadas)

    # Informe final
    print(f"\n\033[34mInforme Final:\033[0m")
    if imagenes_redimensionadas:
        print(f"\033[34mImágenes redimensionadas y su ubicación:\033[0m")
        for subcarpeta, ruta in imagenes_redimensionadas.items():
            print(f"\033[34m{subcarpeta}: {ruta}\033[0m")
    else:
        print(f"\033[31mNo se redimensionaron imágenes.\033[0m")

    if reemplazos:
        print(f"\033[34mReemplazos en el HTML:\033[0m")
        for original, nuevo, subcarpeta in reemplazos:
            print(f"\033[34m{original} -> {nuevo} (Título: {subcarpeta.replace('_', ' ').title()})\033[0m")
        print(f"\033[34mTotal de reemplazos realizados: {len(reemplazos)}\033[0m")
    else:
        print(f"\033[31mNo se realizaron reemplazos en el HTML.\033[0m")

    print(f"\033[34mHTML modificado guardado en: {ruta_nuevo_html}\033[0m")

if __name__ == "__main__":
    main()
