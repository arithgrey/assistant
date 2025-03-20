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
        self.context = ssl._create_unverified_context()
    
    def top_sellers(self):
        try:
            url = f'{self.base_url}/productos/top-sellers/?format=json'
            response = urllib.request.urlopen(url, context=self.context)
            return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            # En lugar de lanzar una excepción, devolver una lista vacía o datos predeterminados
            print(f'Error al obtener los productos: {str(e)}')
            return []  # Devolver lista vacía en caso de error
    
    def products_category(self, category_slug: str ):
        try:
            url = f'{self.base_url}/product-category/{category_slug}/'
            response = urllib.request.urlopen(url, context=self.context)
            return json.loads(response.read().decode('utf-8'))

        except Exception as e:
            print(f'Error al obtener productos por categoría: {str(e)}')
            return []  # Devolver lista vacía en caso de error
