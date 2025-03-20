import requests
import json
import os
from typing import Dict, Any, Optional


class ContextLoader:
    """
    Clase para cargar contexto de APIs externas y guardar los resultados en archivos JSON.
    """
    
    def __init__(self, cache_dir: str = "cache/data"):
        """
        Inicializa el cargador de contexto.
        
        Args:
            cache_dir: Directorio donde se guardarán los archivos JSON.
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def fetch_data(self, url: str, headers: Optional[Dict[str, str]] = None, 
                   params: Optional[Dict[str, Any]] = None, 
                   filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Realiza una solicitud GET a la URL especificada y guarda la respuesta en un archivo JSON.
        Si ya existe un archivo en caché, lo carga directamente sin hacer la solicitud.
        
        Args:
            url: URL a la que se hará la solicitud.
            headers: Encabezados HTTP opcionales para la solicitud.
            params: Parámetros opcionales para la solicitud.
            filename: Nombre del archivo donde se guardará la respuesta.
                     Si no se proporciona, se generará basado en la URL.
                     
        Returns:
            Datos de la respuesta como diccionario.
        """
        # Generar nombre de archivo si no se proporciona
        if filename is None:
            # Crear un nombre de archivo basado en la URL
            url_parts = url.split('://')[-1].replace('/', '_').replace('?', '_')
            filename = f"{url_parts}.json"
        
        # Asegurar que el archivo termine con .json
        if not filename.endswith('.json'):
            filename += '.json'
            
        # Ruta completa al archivo
        file_path = os.path.join(self.cache_dir, filename)
        
        # Verificar si el archivo ya existe en caché
        if os.path.exists(file_path):
            print(f"Cargando datos desde caché: {file_path}")
            return self.load_cached_data(filename)
        
        try:
            # Realizar la solicitud HTTP
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Lanzar excepción si hay error HTTP
            
            # Convertir respuesta a JSON
            data = response.json()
            
            # Guardar datos en archivo JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            print(f"Datos guardados exitosamente en {file_path}")
            return data
            
        except requests.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")
            return {}
        except json.JSONDecodeError:
            print("Error al decodificar la respuesta JSON")
            return {}
        except IOError as e:
            print(f"Error al escribir el archivo: {e}")
            return {}
    
    def load_cached_data(self, filename: str) -> Dict[str, Any]:
        """
        Carga datos previamente almacenados en caché.
        
        Args:
            filename: Nombre del archivo a cargar.
            
        Returns:
            Datos cargados como diccionario.
        """
        # Asegurar que el archivo termine con .json
        if not filename.endswith('.json'):
            filename += '.json'
            
        file_path = os.path.join(self.cache_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al cargar datos desde {file_path}: {e}")
            return {}
