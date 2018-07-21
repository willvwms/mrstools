import json
import webbrowser

# This program is for items that are not yet scraped (b/c not yet active) - takes Magneto item ID and opens edit link

def edit(ID):
	try:
		url = "https://www.mr-s-leather.com/mslpanel/catalog/product/edit/id/{}/key/b44ab2d7422184f5cf18e0f393136f027ea29e5b3c32c95e3f292e8fce0abe47/".format(ID)
		webbrowser.open_new(url)
	except:
		print("Couldn't open {}".format(sku))

# ----------------------------------------------------------------
# MAIN PROCESS:
# ----------------------------------------------------------------

keepgoing = True
while keepgoing:
	raw = input("Activate sku(s):")
	skus = raw.upper().split(" ")
	for sku in skus:
		edit(sku)
