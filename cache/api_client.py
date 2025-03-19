from rest_framework.response import Response
from rest_framework import status
import requests
from django.core.cache import cache
from django.conf import settings
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class ApiClient:
    
    def __init__(self):
        # Usar el nombre del servicio de la tienda en la red Docker
        self.base_url = 'http://enid_store:8080/api/enid'
        self.session = requests.Session()
        
        # Configurar reintentos
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
            'Accept': 'application/json, text/plain, */*',
            'X-Store-Id': '1',
            'Referer': 'https://enidservice.com/'
        }
    
    def top_sellers(self):
        try:
            url = f'{self.base_url}/productos/top-sellers/'
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise Exception('Tiempo de espera agotado al conectar con el servicio')
        except requests.ConnectionError:
            raise Exception('No se pudo establecer conexión con el servicio de productos')
        except requests.RequestException as e:
            raise Exception(f'Error al obtener los productos: {str(e)}')
    
    def products_category(self, category_slug: str ) -> list:
        try:
            url = f'{self.base_url}/product-category/{category_slug}/'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f'Error al obtener productos por categoría: {str(e)}')