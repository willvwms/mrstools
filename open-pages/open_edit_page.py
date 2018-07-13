import json
import webbrowser
import requests

with open('00-previous-scrape.json', 'rb') as f:
    products = json.load(f)

def edit(sku):
	try:
		sku = sku.upper()
		ID = [products[item]['id'] for item in products if item == sku][0]
		template = "https://www.mr-s-leather.com/mslpanel/catalog/product/edit/id/{}/key/b44ab2d7422184f5cf18e0f393136f027ea29e5b3c32c95e3f292e8fce0abe47/"
		url = template.format(ID)
		webbrowser.open_new(url)
	except:
		print("Couldn't open {}".format(sku))

keepgoing = True

while keepgoing:
	raw = input("Edit sku(s):")
	skus = raw.upper().split(" ")
	for element in skus:
		edit(element)

