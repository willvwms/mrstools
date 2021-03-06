# --------------------------------------------------------------------------------
# DEPENDENCIES
# --------------------------------------------------------------------------------
import sys
import os
import requests
from datetime import datetime
import webbrowser
from bs4 import BeautifulSoup
from unidecode import unidecode
import json
import copy

# --------------------------------------------------------------------------------
# GLOBAL VARIABLES, FUNCTIONS
# --------------------------------------------------------------------------------
# directory = "C:/Users/mrs.BradBlandin-PC/Desktop"
now = datetime.now()
date, time = now.strftime("%m-%d-%y"), now.strftime("%H-%M") # 03/13/28, 10:10 AM

counter, URLs, skipped_urls, products_array, non_items = 1, list(), list(), list(), [
	"com/bondage-bdsm/",
	"com/leather/",
	"com/neoprene/",
	"com/puppy-park/",
	"com/rubber/",
	"com/sex-toys/",
	"com/sportwear-streetwear/",
	"com/new-hot/",
	"com/promo",
	"com/help/",
	"com/homepage",
	"shipping-fees-international",
	"com/catalog",
	"com/privacy",
	"com/enable",
	"com/home",
	"com/compliance",
	"com/affiliates",
	"com/shipping",
	"com/standard",
	"testattribute",
	"harness-template",
	"com/mr-s-leather-gift-card",
	"holy-trainer-kit-mock-up",
	"com/back-alley-bulldog-test",
	"com/template-all-around-strap",
	"com/testattribute",
	"com/newsletter",
],

# --------------------------------------------------------------------------------
# HYDRATE THE PREVIOUS COMPARISON OBJECT
# --------------------------------------------------------------------------------
with open('last-scrape.json', 'r') as f:
    previous = json.load(f)

# --------------------------------------------------------------------------------
# HYDRATE CHANGE LOG & COPY IT
# --------------------------------------------------------------------------------
try:
	with open('last-change-log.json', 'r') as f:
	    change_log = json.load(f)
except:
	print("Error - could not load change log from JSON file!")

change_log_COPY = copy.deepcopy(change_log)

# --------------------------------------------------------------------------------
# HIT SITEMAP, BUILD LIST OF URLS, FILTER OUT CATEGORY ENDPOINTS
# --------------------------------------------------------------------------------
raw_xml = requests.get("https://www.mr-s-leather.com/sitemap.xml").text
parsed_xml = BeautifulSoup(raw_xml, 'lxml')
urls_soup_object = parsed_xml.body.find_all('loc')
[URLs.extend(loc_tag.contents) for loc_tag in urls_soup_object]
# remove non-item URLs
item_urls = list(filter(lambda url: (not any(category_name in url for category_name in non_items)), URLs))
# remove first 7 (these are top-level category URLs; they get skipped in the filter above because their endpoint does not terminate with "/")
del item_urls[0:7]

for url in item_urls:

	try:
		soup = BeautifulSoup((requests.get(url).text), "html5lib")

		if (soup.find(attrs={'class':'product-item-manufacturer'})) is not None:
			manufacturer = soup.find(attrs={'class':'product-item-manufacturer'}).strong.get_text(strip=True)
		else:
			manufacturer = ''

		deploy_url = url
		ID = str(soup.find("div", {"class":"price-final_price"})['data-product-id'])
		edit_url = "https://www.mr-s-leather.com/mslpanel/catalog/product/edit/id/{}/key/b44ab2d7422184f5cf18e0f393136f027ea29e5b3c32c95e3f292e8fce0abe47/".format(ID)
		sku = soup.find(attrs={ "itemprop" : "sku" }).get_text(strip=True)
		name = soup.find(attrs={'itemprop':'name'}).get_text(strip=True)
		description = unidecode(str(soup.find(id="product-details").get_text('\n\n', strip=True)))
		images, videos = [], []

		# Grab, sort and append video/image URLs
		for div in soup.find_all('div', attrs={"class":"gallery-image-container"}): # this will grab both videos and images; need to distinguish videos by addl class name "js-chosen-video"

			#Video block:
			if "js-chosen-video" in str(div):
				vid_url = div.get('data-videourl')
				videos.append( vid_url )

			#Image block:
			else:
				url_start = str(div).find( "url('") + 5  # index + 5 to acct for characters u-r-l-(-'
				url_end = str(div).find( "')" )
				img_url = str(div)[ url_start : url_end ]
				images.append( img_url )

		item = {
			"id": ID,
			"sku": sku,
			"deploy_url": deploy_url,
			"edit_url" : edit_url,
			"name": name,
			"manufacturer": manufacturer,
			"description": description,
			"images" : images,
			"videos": videos,
		}

		products_array.append(item)
		print("Scraped " + str(counter) + " of " + str( len( item_urls ) ) )
		counter += 1

	except Exception as err:
		skipped_urls.append(url)
		print("============================================")
		print("SKIPPED #{} of {}".format( str(counter), str( len(item_urls) ) ) )
		print("URL: {}".format(url))
		print("Error:")
		print("line: " + str(sys.exc_info()[-1].tb_lineno) )
		print(err)
		print("============================================")

		counter +=1

# --------------------------------------------------------------------------------
# SERIALIZE THE PRODUCT DATA:
# --------------------------------------------------------------------------------

# Make dictionary from array for subsequent steps
product_dictionary = dict()
[product_dictionary.update({item['sku']:item}) for item in products_array]

# --------------------------------------------------------------------------------
# COMPARE MISSING / ADDED ITEMS AND LOG THEM:
# --------------------------------------------------------------------------------
current = product_dictionary

for key, value in current.items():
	if key not in previous.keys():
		change_log_COPY['items'].append(value)
		new_index = len(change_log_COPY['items'])-1
		change_log_COPY['items'][new_index]['date'] = date.replace("-","/")
		change_log_COPY['items'][new_index]['action'] = 'add'

for key, value in previous.items():
	if key not in current.keys():
		change_log_COPY['items'].append(value)
		new_index = len(change_log_COPY['items'])-1
		change_log_COPY['items'][new_index]['date'] = date.replace("-","/")
		change_log_COPY['items'][new_index]['action'] = 'deactivate'

with open("./changelog-archive/{}_{}_changelog.json".format(date,time), 'w') as f:
	json.dump(change_log_COPY, f, indent=1)

with open("LAST-CHANGE-LOG.json", 'w') as f:
	json.dump(change_log_COPY, f, indent=1)

# For display purposes:
new_entries_index = len(change_log['items'])
new_changes_slice = change_log_COPY['items'][new_entries_index:]
print(("-"*80))
print("PRODUCTS CHANGED:")
print(json.dumps(new_changes_slice, indent=1))
print(("-"*80))

# --------------------------------------------------------------------------------
# ASSIGN CATEGORIES TO EVERY ITEM, THEN CHECK FOR ORPHAN ITEMS
# --------------------------------------------------------------------------------

# Hydrate Categories data object
with open('LAST-INVENTORY.json', 'r') as f:
    categories = json.load(f)

# Run through list of items
for sku, data in product_dictionary.items():
	# add new attribute to hold list of Category names
	data['categories'] = list()

	for category, item_list in categories.items():

		if sku in item_list:
			data['categories'].append(category)

non_cat_items = [ key for key, value in product_dictionary.items() if (len(value['categories'])<1) ]
print("-"*80)
print("ITEMS WITHOUT CATEGORIES:")
for x in non_cat_items: print(x)
print("-"*80)

# --------------------------------------------------------------------------------
# OVER-WRITE THE COMPARISON OBJECT & UPDATE THE CHANGE LOG
# --------------------------------------------------------------------------------

# Save two copies of finished JSON data:
# 1: dated archive
with open("./scrape-archive/scrape__{}__{}.json".format(date, time), 'w') as f:
	json.dump(product_dictionary, f, indent=1)
# 2: over-write 'previous scrape' for future comparison
with open('last-scrape.json', 'w') as f:
	json.dump(product_dictionary, f, indent=1)
