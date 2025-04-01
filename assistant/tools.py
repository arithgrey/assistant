from langchain.tools import Tool
from cache.services import CacheService

class Tools:
    def __init__(self):
        self.cache_service = CacheService()

    def top_sellers_tool(self) -> Tool:
        def _top_sellers(_: str) -> str:
            return self.cache_service.top_sellers()
           
        return Tool.from_function(
            name="obtener_top_sellers",
            func=_top_sellers,
            description="""
            Usa esta herramienta para obtener una lista de los productos más vendidos.
            Si el usuario pregunta por productos (estos son los productos más vendidos), o lo que recomiendas.

            El resultado debe presentarse en formato 
                - imagen  
                - Poco texto pero dirigido a que el cliente compre
                - al dar click en la imagen se redirige al enlace de la web para ver el producto con detalle, 
                - Debe mostrar el enlace directo de compra, 
                - detalles como precio y peso. 
            Tu misión es ayudar a que el cliente compre fácilmente.
            Regresa el resultado en formato Markdown ya que mostraras el resultado en un chat.
            Identificas las imagenes ya que normalmento son links que llevan la palabla uploads/
            """
        )


    def product_category_tool(self) -> Tool:
        def _product_category(_: str) -> str:
            return self.cache_service.products_category()

        return Tool.from_function(
            name="obtener_productos_por_categoria",
            func=_product_category,
            description="""Usa esta herramienta si el cliente quiere ver productos por categoría  y manten el formato
            de la herramienta _top_sellers"""
        )

    def get_tools(self) -> list[Tool]:
        return [
            self.top_sellers_tool(),
            self.product_category_tool(),
        ]
