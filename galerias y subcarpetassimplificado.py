import os
from PIL import Image, ExifTags, UnidentifiedImageError
from bs4 import BeautifulSoup

def print_info(message):
    print(message)

def correct_image_orientation(im):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(im._getexif().items())
        if exif[orientation] == 3:
            im = im.rotate(180, expand=True)
        elif exif[orientation] == 6:
            im = im.rotate(270, expand=True)
        elif exif[orientation] == 8:
            im = im.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # No EXIF information
        pass
    return im

# Solicitar rutas si es necesario
html_path = input("Introduce la ruta del archivo HTML: ").strip()
images_dir = input("Introduce la ruta de la carpeta 'commercial_roofing': ").strip()
output_dir = input("Introduce la ruta de la carpeta de salida para las imágenes redimensionadas: ").strip()

# Crear la carpeta de salida si no existe
if not os.path.exists(output_dir):
    try:
        os.makedirs(output_dir)
    except Exception as e:
        print_info(f"Error al crear la carpeta de salida: {e}")
        exit()

# Leer el HTML
with open(html_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Seleccionar el rango de líneas especificado
relevant_lines = lines[175:274]
html_content = ''.join(relevant_lines)
soup = BeautifulSoup(html_content, 'html.parser')

# Encontrar todas las imágenes en el rango de líneas especificado
gallery_images = soup.find_all('img')

# Procesar una imagen por subcarpeta
subfolders = [f.path for f in os.scandir(images_dir) if f.is_dir()]
images_processed = 0

for subfolder in subfolders:
    subfolder_name = os.path.basename(subfolder)
    images = [f for f in os.scandir(subfolder) if f.is_file() and (f.name.lower().endswith('.jpg') or f.name.lower().endswith('.jpeg') or f.name.lower().endswith('.png'))]
    
    if len(images) > 5:
        img_path = images[5].path  # Seleccionar la sexta imagen compatible
        try:
            with Image.open(img_path) as im:
                im = correct_image_orientation(im)
                im = im.convert('RGB')
                # Obtener tamaño original de la primera imagen de la galería
                src = gallery_images[images_processed % len(gallery_images)]['src']
                original_img_path = os.path.join(os.path.dirname(html_path), src)
                with Image.open(original_img_path) as original_im:
                    width, height = original_im.size
                
                im.thumbnail((width, height), Image.LANCZOS)
                
                # Centrar y recortar la imagen
                left = (im.width - width) / 2
                top = (im.height - height) / 2
                right = (im.width + width) / 2
                bottom = (im.height + height) / 2
                im = im.crop((left, top, right, bottom))
                
                # Guardar la imagen redimensionada
                output_path = os.path.join(output_dir, f'{subfolder_name}.jpg')
                im.save(output_path, 'JPEG', quality=85)
                
                # Actualizar el src, alt, y title en el HTML
                img_tag = gallery_images[images_processed % len(gallery_images)]
                img_tag['src'] = output_path
                img_tag['alt'] = subfolder_name
                img_tag['title'] = subfolder_name
                
                # Actualizar el título dentro del div con la clase "title"
                title_div = img_tag.find_previous_sibling("div", class_="title")
                if title_div:
                    title_div.string = "commercial work"
                
                # Actualizar el contenido del h4
                h4_tag = img_tag.find_next_sibling("h4")
                if h4_tag and h4_tag.a:
                    h4_tag.a.string = subfolder_name
                
                images_processed += 1
                print_info(f"Imagen procesada: {output_path}")
        except (UnidentifiedImageError, IOError):
            print_info(f"Archivo no compatible o no identificado: {img_path}")
            continue

# Reemplazar el contenido de las líneas relevantes en el archivo original
lines[175:274] = str(soup).splitlines(True)
output_html_path = os.path.join(os.path.dirname(html_path), 'modified_' + os.path.basename(html_path))
with open(output_html_path, 'w', encoding='utf-8') as file:
    file.writelines(lines)

# Informe final
print_info("\nProceso completado:")
print_info(f"HTML resultante: {output_html_path}")
print_info(f"Imágenes redimensionadas: {images_processed}")
print_info(f"Imágenes almacenadas en: {output_dir}")

