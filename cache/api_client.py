from rest_framework.response import Response
from rest_framework import status
import requests
import json
import urllib.request
import ssl
from django.core.cache import cache

class ApiClient:
    
    def __init__(self):
        self.base_url = 'http://localhost:8000/api/enid'
        self.headers = {}
    
    def top_sellers(self):
        try:
            url = f'{self.base_url}/productos/top-sellers/?format=json'
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(url, context=context)
            return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            # En lugar de lanzar una excepción, devolver una lista vacía o datos predeterminados
            print(f'Error al obtener los productos: {str(e)}')
            return []  # Devolver lista vacía en caso de error
    
    def products_category(self, category_slug: str ) -> list:
        try:
            url = f'{self.base_url}/product-category/{category_slug}/'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f'Error al obtener productos por categoría: {str(e)}')