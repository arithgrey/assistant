from django.apps import AppConfig


class CacheConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cache'
    
    def ready(self):
        from cache.loader import ContextLoader
        
        base_url = "https://enidservice.com/api/enid/"
        endpoints = [
            {"path": "productos/top-sellers/", "filename": "top_seller.json"},
            {"path": "product-category/pesas-y-barras/?format=json", "filename": "pesas-y-barras.json"},
            {"path": "product-category/calistenia/?format=json", "filename": "calistenia.json"},
            {"path": "product-category/accesorios/?format=json", "filename": "accesorios.json"},
        ]
        
        loader = ContextLoader()
        
        for endpoint in endpoints:
            url = base_url + endpoint["path"]
            loader.fetch_data(url=url, filename=endpoint["filename"])
        
        
        
            