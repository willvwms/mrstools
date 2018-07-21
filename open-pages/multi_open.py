import json
import webbrowser
with open("s:/internet sales office/web/credentials/magento.json", "r") as f:
    kw = json.load(f)

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

# Build two comprehensive dictionaries of the edit and view links:
edit_urls = dict()

for i in products:
	sku = i
	ID = products[i]['id']
	editURL = "https://www.mr-s-leather.com/mslpanel/catalog/product/edit/id/{}/key/b44ab2d7422184f5cf18e0f393136f027ea29e5b3c32c95e3f292e8fce0abe47/".format(ID)
	edit_urls.update({sku: editURL})

def view(sku):
	try:
		url = products[sku]['url']
		webbrowser.open_new(url)
	except:
		print("Couldn't open {}".format(sku))

def edit(sku):
	try:
		url = edit_urls[sku]
		webbrowser.open_new(url)
	except:
		print("Couldn't open {}".format(sku))

# ----------------------------------------------------------------
# MAIN PROCESS
# ----------------------------------------------------------------
print(kw['login'])

keepgoing = True

while keepgoing:
	raw = input("View (v) / edit(e) SKUs:")
	skus = raw.upper().split(" ")
	if skus[0] == 'E' or skus[0] == "EDIT":
		for sku in skus[1:]:
			edit(sku)
	elif skus[0] == 'V' or skus[0] == "VIEW":
		for sku in skus[1:]:
			view(sku)
	else:
		print("Preface your list of SKUs with either \"view (v)\" or \"edit (e)\"")


