from bs4 import BeautifulSoup

with open("ml_dump.html", "r") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
titles = soup.find_all(class_="poly-component__title")

print(f"Found {len(titles)} titles.")

if titles:
    print("--- First Title Structure ---")
    # Print the parent of the title to see the context
    parent = titles[0].parent
    print(parent.prettify())
    
    print("\n--- Grandparent Structure ---")
    print(parent.parent.prettify()[:500]) # Limit output
