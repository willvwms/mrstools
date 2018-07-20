import json
import webbrowser

keepgoing = True

with open('previous-scrape.json', 'r') as f:
    products = json.load(f)

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

while keepgoing:
	raw = input("Edit sku(s):")
	skus = raw.upper().split(" ")
	for sku in skus:
		edit(sku)
