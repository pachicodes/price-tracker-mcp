import httpx
from bs4 import BeautifulSoup

def test_mercadolivre():
    print("--- Testando Mercado Livre ---")
    query = "lavadora e secadora lava e seca"
    url = f"https://lista.mercadolivre.com.br/{query.replace(' ', '-')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    try:
        response = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        print(f"Status Code: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Testar seletor atual
        items = soup.find_all('div', class_='ui-search-result__wrapper')
        print(f"Seletor atual (div.ui-search-result__wrapper): {len(items)} itens")
        
        # Testar seletor alternativo comum
        items_alt = soup.find_all('li', class_='ui-search-layout__item')
        print(f"Seletor alternativo (li.ui-search-layout__item): {len(items_alt)} itens")
        
        if len(items) == 0 and len(items_alt) == 0:
            print("Nenhum item encontrado. Salvando HTML para análise...")
            with open("ml_debug.html", "w") as f:
                f.write(response.text)
                
    except Exception as e:
        print(f"Erro: {e}")

def test_magalu():
    print("\n--- Testando Magazine Luiza ---")
    query = "lava e seca"
    url = f"https://www.magazineluiza.com.br/busca/{query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    try:
        response = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        print(f"Status Code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('li', attrs={'data-testid': 'product-card'})
        print(f"Itens encontrados: {len(items)}")
        
        if len(items) == 0:
            print("Nenhum item encontrado na Magalu. Salvando HTML...")
            with open("magalu_debug.html", "w") as f:
                f.write(response.text)
    except Exception as e:
        print(f"Erro: {e}")

def test_amazon():
    print("\n--- Testando Amazon Brasil ---")
    query = "lava e seca"
    url = f"https://www.amazon.com.br/s?k={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    try:
        response = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        print(f"Status Code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', attrs={'data-component-type': 's-search-result'})
        print(f"Itens encontrados: {len(items)}")
        
        if len(items) == 0:
            print("Nenhum item encontrado na Amazon. Salvando HTML...")
            with open("amazon_debug.html", "w") as f:
                f.write(response.text)
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    # test_mercadolivre()
    # test_magalu()
    # test_casasbahia()
    test_amazon()
