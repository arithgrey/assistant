from rest_framework.response import Response
from rest_framework import status
import requests
from django.core.cache import cache
from cache.api_client import ApiClient

class CacheService:
    def __init__(self):
        self.api_client = ApiClient()
    
    def get_cached_data(self, cache_key, fetch_function, timeout=60*60*24):
        try:
            
            # Intentar obtener datos del caché
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return cached_data
            data = fetch_function()
            cache.set(cache_key, data, timeout=timeout)
            
            return data
            
        except Exception as e:
            raise Exception(f'Error al obtener los datos: {str(e)}')
    
    def top_sellers(self):
        try:
            return self.get_cached_data(
                cache_key='_top_sellers_request',
                fetch_function=self.api_client.top_sellers
            )
        except Exception as e:
            raise Exception(f'Error al obtener los productos: {str(e)}')
  
    def products_category(self):        
        try:
        
            categorias = ['pesas-y-barras', 'accesorios', 'calistenia']            
            resultados = {}
            for categoria in categorias:
                resultados[categoria] = self.get_cached_data(
                    cache_key=f'_products_category_{categoria}_request',
                    fetch_function=lambda c=categoria: self.api_client.products_category(category_slug=c)
                )
            
            return resultados
            
        except Exception as e:
            raise Exception(f'Error al obtener los productos por categoría: {str(e)}')
        