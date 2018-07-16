import json
import webbrowser

keepgoing = True

with open('previous-scrape.json', 'r') as f:
    products = json.load(f)

def open(sku):
	try:
		url = products[sku]['url']
		webbrowser.open_new(url)
	except:
		print("Couldn't open {}".format(sku))

while keepgoing:
	raw = input("View/open sku(s):")
	skus = raw.upper().split(" ")
	for sku in skus:
		open(sku)
