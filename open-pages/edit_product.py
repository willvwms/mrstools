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

urls = dict()

for i in products:
	sku = i
	ID = products[i]['id']
	url = "https://www.mr-s-leather.com/mslpanel/catalog/product/edit/id/{}/key/b44ab2d7422184f5cf18e0f393136f027ea29e5b3c32c95e3f292e8fce0abe47/".format(ID)
	urls.update({sku: url})

def edit(sku):
	try:
		url = urls[sku]
		webbrowser.open_new(url)
	except:
		print("Couldn't open {}".format(sku))

# ----------------------------------------------------------------
# MAIN PROCESS:
# ----------------------------------------------------------------

keepgoing = True
while keepgoing:
	raw = input("Edit sku(s):")
	skus = raw.upper().split(" ")
	for sku in skus:
		edit(sku)
