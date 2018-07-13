import pickle
import webbrowser
import requests

with open('00_COMPLETE_PRODUCT_DATA_LIST.pickle', 'rb') as f:
    products = pickle.load(f)

urls = list()
[urls.append({"url": x['url'], "sku":x['sku']}) for x in products]

skus = True

while skus:
	raw = input("Next series of skus:")
	skus = raw.upper().split(" ")
	[webbrowser.open(x['url']) for x in urls if x['sku'] in skus]