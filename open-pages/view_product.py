import json
import webbrowser

# ----------------------------------------------------------------
# BUILD OBJECT OF PRODUCT DATA FOR ACTIVE AND INACTIVE ITEMS:
# ----------------------------------------------------------------
products = dict()

# Source 1: active products (dict):
with open('../product-data-scraper/previous-scrape.json', 'r') as f:
    actives = json.load(f)
# Source 2: inactive products (list):
with open('../product-data-scraper/last-change-log.json', 'r') as f:
    changelog = json.load(f)
inactives = list(filter(lambda x: x['action'] == 'deactivate', changelog['items']))

for value in inactives:
	key = value['sku']
	products.update( { key : value} )

for key, value in actives.items():
	products.update( { key : value } )

def view(sku):
	try:
		url = products[sku]['url']
		webbrowser.open_new(url)
	except:
		print("Couldn't open {}".format(sku))

# ----------------------------------------------------------------
# MAIN PROCESS:
# ----------------------------------------------------------------
keepgoing = True

while keepgoing:
	raw = input("View/open sku(s):")
	skus = raw.upper().split(" ")
	for sku in skus:
		view(sku)
