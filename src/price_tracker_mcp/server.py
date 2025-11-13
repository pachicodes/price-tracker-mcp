#!/usr/bin/env python3
"""Servidor MCP para buscar lavadoras e secadoras pelos menores preços."""

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
        return [{'error': f'Erro ao buscar no Mercado Livre: {str(e)}'}]


def search_amazon(query: str, max_results: int = 10) -> list[dict[str, Any]]:
    """Busca produtos na Amazon (simulado - API real requer credenciais)."""
    # Nota: Para produção, use a API oficial da Amazon
    return [{
        'info': 'Amazon Brasil - Requer API oficial para busca em tempo real',
        'suggestion': 'Visite: https://www.amazon.com.br/s?k=' + query.replace(' ', '+')
    }]


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Lista as ferramentas disponíveis."""
    return [
        types.Tool(
            name="search_washers",
            description="Busca lavadoras de roupas pelos menores preços em lojas brasileiras",
            inputSchema={
                "type": "object",
                "properties": {
                    "brand": {
                        "type": "string",
                        "description": "Marca específica (opcional, ex: Brastemp, Electrolux, LG, Samsung)",
                    },
                    "capacity": {
                        "type": "string",
                        "description": "Capacidade em kg (opcional, ex: 10kg, 12kg, 15kg)",
                    },
                    "max_results": {
                        "type": "number",
                        "description": "Número máximo de resultados (padrão: 10)",
                        "default": 10
                    }
                },
            },
        ),
        types.Tool(
            name="search_dryers",
            description="Busca secadoras de roupas pelos menores preços em lojas brasileiras",
            inputSchema={
                "type": "object",
                "properties": {
                    "brand": {
                        "type": "string",
                        "description": "Marca específica (opcional, ex: Brastemp, Electrolux, LG, Samsung)",
                    },
                    "capacity": {
                        "type": "string",
                        "description": "Capacidade em kg (opcional, ex: 10kg, 11kg)",
                    },
                    "max_results": {
                        "type": "number",
                        "description": "Número máximo de resultados (padrão: 10)",
                        "default": 10
                    }
                },
            },
        ),
        types.Tool(
            name="search_combo",
            description="Busca lavadoras e secadoras combinadas (lava e seca) pelos menores preços",
            inputSchema={
                "type": "object",
                "properties": {
                    "brand": {
                        "type": "string",
                        "description": "Marca específica (opcional, ex: Brastemp, Electrolux, LG, Samsung)",
                    },
                    "capacity": {
                        "type": "string",
                        "description": "Capacidade em kg (opcional, ex: 10kg, 11kg)",
                    },
                    "max_results": {
                        "type": "number",
                        "description": "Número máximo de resultados (padrão: 10)",
                        "default": 10
                    }
                },
            },
        ),
        types.Tool(
            name="compare_prices",
            description="Compara preços de um produto específico em diferentes lojas",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Nome completo ou modelo do produto",
                    },
                    "max_results": {
                        "type": "number",
                        "description": "Número máximo de resultados por loja (padrão: 5)",
                        "default": 5
                    }
                },
                "required": ["product_name"],
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
    
    max_results = arguments.get("max_results", 10)
    
    if name == "search_washers":
        # Construir query de busca
        query = "lavadora de roupas"
        if arguments.get("brand"):
            query += f" {arguments['brand']}"
        if arguments.get("capacity"):
            query += f" {arguments['capacity']}"
        
        results = search_mercadolivre(query, max_results)
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(results, indent=2, ensure_ascii=False),
            )
        ]
    
    elif name == "search_dryers":
        # Construir query de busca
        query = "secadora de roupas"
        if arguments.get("brand"):
            query += f" {arguments['brand']}"
        if arguments.get("capacity"):
            query += f" {arguments['capacity']}"
        
        results = search_mercadolivre(query, max_results)
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(results, indent=2, ensure_ascii=False),
            )
        ]
    
    elif name == "search_combo":
        # Construir query de busca
        query = "lavadora e secadora lava e seca"
        if arguments.get("brand"):
            query += f" {arguments['brand']}"
        if arguments.get("capacity"):
            query += f" {arguments['capacity']}"
        
        results = search_mercadolivre(query, max_results)
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(results, indent=2, ensure_ascii=False),
            )
        ]
    
    elif name == "compare_prices":
        product_name = arguments.get("product_name", "")
        if not product_name:
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({"error": "Nome do produto é obrigatório"}, indent=2),
                )
            ]
        
        results = search_mercadolivre(product_name, max_results)
        
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
