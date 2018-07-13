# DEPENDENCIES
import requests
from bs4 import BeautifulSoup

# GLOBAL VARIABLES
counter, catches, URLs, non_items = 0, list(), list(), [
	"com/bondage",
	"com/leather",
	"com/neoprene",
	"com/puppy",
	"com/rubber",
	"com/sex-toys",
	"com/sportwear",
	"com/new",
	"com/promo",
	"com/help",
	"com/homepage",
	"vonnda.net",
	"com/catalog",
	"com/privacy",
	"com/enable",
	"com/home",
	"com/compliance",
	"com/affiliates",
	"com/shipping",
	"com/standard",
]

# HIT SITEMAP, BUILD LIST OF URLS, FILTER OUT CATEGORY ENDPOINTS
raw_xml = requests.get("https://www.mr-s-leather.com/sitemap.xml").text
parsed_xml = BeautifulSoup(raw_xml, 'lxml')
urls_soup_object = parsed_xml.body.find_all('loc')
[URLs.extend(loc_tag.contents) for loc_tag in urls_soup_object]
item_urls = list(filter(lambda url: (not any(category_name in url for category_name in non_items)), URLs))


for url in item_urls:

	try:
		soup = BeautifulSoup((requests.get(url).text), "html5lib")
		column_section = soup.find(attrs={'class':'product-add-form'})
		span_elements = column_section.find_all('span')
		spans = [ str(span) for span in span_elements]
		if (any('ey' in string for string in spans)) or (any('515' in string for string in spans)):
			catches.append(url)
			print("FOUND POTENTIAL KEYED ALIKE: \n" + url)
		counter += 1
		print("Checked item #{} out of {}".format(str(counter), str(len(item_urls))) )

	except:
		(print("Couldn't finish:\n"+url+'\n'))
		counter +=1

