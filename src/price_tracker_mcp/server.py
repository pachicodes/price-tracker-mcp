#!/usr/bin/env python3
"""Servidor MCP para buscar máquinas lava e seca pelos menores preços."""

import asyncio
import json
from typing import Any
import httpx
from bs4 import BeautifulSoup
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio


# Criar instância do servidor
server = Server("price-tracker-mcp")


def search_mercadolivre(query: str, max_results: int = 10) -> list[dict[str, Any]]:
    """Busca produtos no Mercado Livre."""
    try:
        url = f"https://lista.mercadolivre.com.br/{query.replace(' ', '-')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        response = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        # Buscar itens de produtos
        items = soup.find_all('div', class_='ui-search-result__wrapper')[:max_results]
        
        for item in items:
            try:
                title_elem = item.find('h2', class_='ui-search-item__title')
                price_elem = item.find('span', class_='andes-money-amount__fraction')
                link_elem = item.find('a', class_='ui-search-link')
                
                if title_elem and price_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    price_text = price_elem.get_text(strip=True).replace('.', '')
                    link = link_elem.get('href', '')
                    
                    try:
                        price = float(price_text)
                        products.append({
                            'title': title,
                            'price': price,
                            'link': link,
                            'store': 'Mercado Livre'
                        })
                    except ValueError:
                        continue
            except Exception:
                continue
        
        return sorted(products, key=lambda x: x['price'])
    except Exception as e:
        return []


def search_magazineluiza(query: str, max_results: int = 10) -> list[dict[str, Any]]:
    """Busca produtos na Magazine Luiza."""
    try:
        url = f"https://www.magazineluiza.com.br/busca/{query.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        response = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        # Buscar itens de produtos
        items = soup.find_all('li', attrs={'data-testid': 'product-card'})[:max_results]
        
        for item in items:
            try:
                title_elem = item.find('h2', attrs={'data-testid': 'product-title'})
                price_elem = item.find('p', attrs={'data-testid': 'price-value'})
                link_elem = item.find('a', attrs={'data-testid': 'product-card-container'})
                
                if title_elem and price_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    price_text = price_elem.get_text(strip=True).replace('R$', '').replace('.', '').replace(',', '.').strip()
                    link = 'https://www.magazineluiza.com.br' + link_elem.get('href', '')
                    
                    try:
                        price = float(price_text)
                        products.append({
                            'title': title,
                            'price': price,
                            'link': link,
                            'store': 'Magazine Luiza'
                        })
                    except ValueError:
                        continue
            except Exception:
                continue
        
        return sorted(products, key=lambda x: x['price'])
    except Exception as e:
        return []


def search_casasbahia(query: str, max_results: int = 10) -> list[dict[str, Any]]:
    """Busca produtos na Casas Bahia."""
    try:
        url = f"https://www.casasbahia.com.br/busca/{query.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        response = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        # Buscar itens de produtos
        items = soup.find_all('div', class_='css-16zq8vo')[:max_results]
        
        for item in items:
            try:
                title_elem = item.find('h2', class_='css-s3s88i')
                price_elem = item.find('p', class_='css-1k6tihg')
                link_elem = item.find('a', class_='css-z7h5w9')
                
                if title_elem and price_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    price_text = price_elem.get_text(strip=True).replace('R$', '').replace('.', '').replace(',', '.').strip()
                    link = 'https://www.casasbahia.com.br' + link_elem.get('href', '')
                    
                    try:
                        price = float(price_text)
                        products.append({
                            'title': title,
                            'price': price,
                            'link': link,
                            'store': 'Casas Bahia'
                        })
                    except ValueError:
                        continue
            except Exception:
                continue
        
        return sorted(products, key=lambda x: x['price'])
    except Exception as e:
        return []


def search_amazon(query: str, max_results: int = 10) -> list[dict[str, Any]]:
    """Busca produtos na Amazon Brasil."""
    try:
        url = f"https://www.amazon.com.br/s?k={query.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        
        response = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        # Buscar itens de produtos
        items = soup.find_all('div', attrs={'data-component-type': 's-search-result'})[:max_results]
        
        for item in items:
            try:
                title_elem = item.find('h2', class_='s-size-mini-semi-bold')
                if not title_elem:
                    title_elem = item.find('span', class_='a-size-medium a-color-base a-text-normal')
                
                price_whole = item.find('span', class_='a-price-whole')
                price_fraction = item.find('span', class_='a-price-fraction')
                link_elem = item.find('a', class_='a-link-normal s-no-outline')
                
                if title_elem and price_whole and link_elem:
                    title = title_elem.get_text(strip=True)
                    price_text = price_whole.get_text(strip=True).replace('.', '')
                    if price_fraction:
                        price_text += '.' + price_fraction.get_text(strip=True)
                    else:
                        price_text += '.00'
                    
                    link = 'https://www.amazon.com.br' + link_elem.get('href', '')
                    
                    try:
                        price = float(price_text)
                        products.append({
                            'title': title,
                            'price': price,
                            'link': link,
                            'store': 'Amazon Brasil'
                        })
                    except ValueError:
                        continue
            except Exception:
                continue
        
        return sorted(products, key=lambda x: x['price'])
    except Exception as e:
        return []


def search_all_stores(query: str, max_results_per_store: int = 5) -> list[dict[str, Any]]:
    """Busca produtos em todas as lojas e combina os resultados."""
    all_products = []
    
    # Buscar em cada loja
    all_products.extend(search_mercadolivre(query, max_results_per_store))
    all_products.extend(search_magazineluiza(query, max_results_per_store))
    all_products.extend(search_casasbahia(query, max_results_per_store))
    all_products.extend(search_amazon(query, max_results_per_store))
    
    # Filtrar erros e ordenar por preço
    valid_products = [p for p in all_products if 'price' in p and 'error' not in p]
    return sorted(valid_products, key=lambda x: x['price'])


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Lista as ferramentas disponíveis."""
    return [
        types.Tool(
            name="search_washer_dryer",
            description="Busca máquinas lava e seca (que lavam E secam roupas) pelos menores preços em múltiplas lojas brasileiras (Mercado Livre, Magazine Luiza, Casas Bahia, Amazon)",
            inputSchema={
                "type": "object",
                "properties": {
                    "brand": {
                        "type": "string",
                        "description": "Marca específica (opcional, ex: Brastemp, Electrolux, LG, Samsung)",
                    },
                    "capacity": {
                        "type": "string",
                        "description": "Capacidade em kg (opcional, ex: 10kg, 11kg, 12kg)",
                    },
                    "max_results": {
                        "type": "number",
                        "description": "Número máximo de resultados totais (padrão: 15)",
                        "default": 15
                    }
                },
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Executa uma ferramenta."""
    if not arguments:
        arguments = {}
    
    max_results = arguments.get("max_results", 15)
    
    if name == "search_washer_dryer":
        # Construir query de busca para máquinas lava e seca
        query = "lavadora e secadora lava e seca"
        if arguments.get("brand"):
            query += f" {arguments['brand']}"
        if arguments.get("capacity"):
            query += f" {arguments['capacity']}"
        
        # Buscar em todas as lojas (aproximadamente 4 por loja)
        max_per_store = max(3, max_results // 4)
        results = search_all_stores(query, max_per_store)
        
        # Limitar ao máximo solicitado
        results = results[:max_results]
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(results, indent=2, ensure_ascii=False),
            )
        ]
    
    else:
        raise ValueError(f"Ferramenta desconhecida: {name}")


async def main():
    """Executar o servidor."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="price-tracker-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
