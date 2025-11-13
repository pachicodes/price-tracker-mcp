# Price Tracker MCP Server

Servidor MCP para buscar lavadoras e secadoras de roupas pelos menores preços.

## Recursos

- 🔍 Busca de lavadoras e secadoras em diversos sites brasileiros
- 💰 Comparação de preços
- 📊 Ordenação por menor preço
- 🔗 Links diretos para os produtos

## Instalação

```bash
pip install -e .
```

## Uso

```bash
python -m price_tracker_mcp.server
```

## Configuração no Claude Desktop

Adicione ao seu `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "price-tracker": {
      "command": "python",
      "args": ["-m", "price_tracker_mcp.server"]
    }
  }
}
```

## Ferramentas Disponíveis

- `search_washers`: Busca lavadoras de roupas pelos menores preços
- `search_dryers`: Busca secadoras de roupas pelos menores preços
- `search_combo`: Busca lavadoras e secadoras combinadas (lava e seca)
- `compare_prices`: Compara preços de um produto específico em diferentes lojas
