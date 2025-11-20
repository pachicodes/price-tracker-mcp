import httpx
from bs4 import BeautifulSoup

def inspect():
    query = "lava e seca samsung"
    url = f"https://lista.mercadolivre.com.br/{query.replace(' ', '-')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    print(f"Fetching {url}...")
    response = httpx.get(url, headers=headers, follow_redirects=True)
    print(f"Status: {response.status_code}")
    
    with open("ml_dump.html", "w") as f:
        f.write(response.text)
    print("Saved to ml_dump.html")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check for common containers
    divs = soup.find_all('div')
    print(f"Total divs: {len(divs)}")
    
    lis = soup.find_all('li')
    print(f"Total lis: {len(lis)}")
    
    # Look for anything that looks like a search result
    # Usually they have 'ui-search' in the class
    search_classes = set()
    for tag in soup.find_all(True, class_=True):
        for cls in tag['class']:
            if 'ui-search' in cls or 'poly-' in cls:
                search_classes.add(cls)
                
    print("\nPotential search classes found:")
    for cls in sorted(search_classes):
        print(f"- {cls}")

if __name__ == "__main__":
    inspect()
