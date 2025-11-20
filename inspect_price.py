from bs4 import BeautifulSoup

with open("ml_dump.html", "r") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
prices = soup.find_all(class_="poly-price__current")

print(f"Found {len(prices)} prices.")

if prices:
    print("--- First Price Structure ---")
    print(prices[0].prettify())
