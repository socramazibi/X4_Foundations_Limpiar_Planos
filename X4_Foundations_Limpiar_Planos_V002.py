import xml.etree.ElementTree as ET
import os

def clean_xml_files(input_folder, output_folder):
    # Asegurar que la carpeta de salida existe
    os.makedirs(output_folder, exist_ok=True)
    
    errores = []
    
    # Recorrer todos los archivos en la carpeta de entrada
    for filename in os.listdir(input_folder):
        if filename.endswith(".xml"):  # Procesar solo archivos XML
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
                print(f"Archivo limpio guardado: {output_path}")
            
            except ET.ParseError:
                errores.append(f"Error al analizar el archivo XML: {filename}")
            except Exception as e:
                errores.append(f"Error desconocido con {filename}: {e}")
    
    if errores:
        print("\nSe encontraron algunos errores:")
        for error in errores:
            print(error)
    else:
        print("\nProceso completado con éxito. Todos los archivos se limpiaron correctamente.")
    
    input("Presiona Enter para salir...")

# Ejemplo de uso
input_folder = "entrada"
output_folder = "salida"
clean_xml_files(input_folder, output_folder)
