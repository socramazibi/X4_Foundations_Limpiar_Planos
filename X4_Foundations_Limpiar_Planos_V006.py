import xml.etree.ElementTree as ET
import os

def clean_xml_files(input_folder, output_folder):
    # Asegurar que las carpetas existen
    if not os.path.exists(input_folder):
        print(f"La carpeta de entrada '{input_folder}' no existe. Creándola...")
        os.makedirs(input_folder, exist_ok=True)
        print("Por favor, añade archivos XML en la carpeta de entrada y vuelve a ejecutar el programa.")
        os.system("pause")
        return
    
    os.makedirs(output_folder, exist_ok=True)
    
    errores = []
    total_archivos = 0
    archivos_limpiados = 0
    
    # Obtener archivos XML en la carpeta de entrada
    xml_files = [f for f in os.listdir(input_folder) if f.endswith(".xml")]
    if not xml_files:
        print("No se encontraron archivos XML en la carpeta de entrada. Agrega archivos y vuelve a intentarlo.")
        os.system("pause")
        return
    
    # Recorrer todos los archivos XML
    for filename in xml_files:
        total_archivos += 1
        input_path = os.path.join(input_folder, filename)
        base_name, ext = os.path.splitext(filename)
        
        # Evitar doble guion bajo en el nombre
        if base_name.endswith("_"):
            base_name = base_name[:-1]
        
        output_path = os.path.join(output_folder, f"{base_name}_clean.xml")
        
        try:
            # Cargar el archivo XML
            tree = ET.parse(input_path)
            root = tree.getroot()
            
            # Modificar el atributo name agregando _clean
            plan = root.find(".//plan")
            if plan is not None and "name" in plan.attrib:
                plan.attrib["name"] += "_clean"
            
            # Buscar y eliminar los nodos <upgrades>
            for entry in root.findall(".//entry"):
                upgrades = entry.find("upgrades")
                if upgrades is not None:
                    entry.remove(upgrades)
            
            # Guardar el archivo limpio
            tree.write(output_path, encoding="utf-8", xml_declaration=True)
            archivos_limpiados += 1
            print(f"Archivo limpio guardado: {output_path}")
        
        except ET.ParseError:
            errores.append(f"Error al analizar el archivo XML: {filename}")
        except Exception as e:
            errores.append(f"Error desconocido con {filename}: {e}")
    
    print("\nResumen del proceso:")
    print(f"Archivos limpiados correctamente: {archivos_limpiados} de {total_archivos}")
    
    if errores:
        print("\nSe encontraron algunos errores:")
        for error in errores:
            print(error)
    else:
        print("\nProceso completado con éxito. Todos los archivos se limpiaron correctamente.")
    
    # Pausa al final para evitar el error con input()
    os.system("pause")

# Ejemplo de uso
input_folder = "entrada"
output_folder = "salida"
clean_xml_files(input_folder, output_folder)
