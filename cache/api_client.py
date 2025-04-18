from rest_framework.response import Response
from rest_framework import status
import requests
from django.core.cache import cache

class ApiClient:
    
    def __init__(self):
        self.base_url = 'https://enidservice.com/api/enid'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
            'Accept': 'application/json, text/plain, */*',
            'X-Store-Id': '1',
            'Referer': 'https://enidservice.com/'
        }
    
    def top_sellers(self):
        try:
            url = f'{self.base_url}/productos/top-sellers/'
            response = requests.get(url, headers=self.headers)
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