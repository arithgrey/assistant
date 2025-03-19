from rest_framework.response import Response
from rest_framework import status
import requests
from django.core.cache import cache

class ApiClient:
    
    def __init__(self):
        self.base_url = 'http://enid_store:8000/api/enid'
        self.session = requests.Session()  # Crear una sesión
        self.headers = {
            'X-Store-Id': '1',
            'Referer': 'https://enidservice.com/'
        }
    
    def top_sellers(self):
        try:
            url = f'{self.base_url}/productos/top-sellers/'
            # Usar la sesión para mantener las cookies
            response = self.session.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            return response.json()
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