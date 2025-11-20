import sys
import os
import json

# Adicionar o diretório src ao path para importar o módulo
sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    from price_tracker_mcp.server import search_mercadolivre
    
    print("--- Testando Lógica do Servidor (search_mercadolivre) ---")
    query = "lava e seca samsung"
    print(f"Buscando por: '{query}'...")
    
    try:
        results = search_mercadolivre(query)
        
        if results:
            print(f"\n✅ Sucesso! Encontrados {len(results)} produtos.")
            print("\nPrimeiro produto encontrado:")
            print(json.dumps(results[0], indent=2, ensure_ascii=False))
        else:
            print("\n⚠️ Nenhum resultado encontrado (lista vazia).")
            
    except Exception as e:
        print(f"\n❌ Erro ao executar a busca: {e}")

except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Verifique se você está na raiz do projeto e se 'src/price_tracker_mcp/server.py' existe.")
