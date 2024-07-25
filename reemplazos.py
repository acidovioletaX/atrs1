import os
import shutil

# Definir la ruta del directorio
directory = r'C:\Users\VLADO 2\Desktop\CODING1\PLAYGROUND\atrs1'
backup_directory = r'D:\copiahtml'

# Crear el directorio de copia si no existe
if not os.path.exists(backup_directory):
    os.makedirs(backup_directory)

# Recorrer todos los archivos en el directorio
for filename in os.listdir(directory):
    # Verificar si el archivo es un archivo HTML
    if filename.endswith('.html'):
        # Definir la ruta completa del archivo
        filepath = os.path.join(directory, filename)
        
        # Copiar el archivo al directorio de copia
        backup_filepath = os.path.join(backup_directory, filename)
        shutil.copy(filepath, backup_filepath)
        print(f"Archivo copiado: {filename} a {backup_directory}")
        
        # Leer el contenido del archivo
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Reemplazar logo.svg por logo.png
        content = content.replace('logo.svg', 'logo.png')
        
        # Reemplazar expart por expert
        content = content.replace('expart', 'expert')
        
        # Grabar de nuevo el archivo con los cambios
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"Archivo procesado: {filename}")

print("Proceso completado.")
