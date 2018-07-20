from bs4 import BeautifulSoup
import requests
from datetime import datetime
import emails

# --------------------------------------------------------------------------------
# FUNCTIONS:

def report_zeros(URLstotal, start_time):

	elapsed_time = datetime.now() - start_time

	print("Checked " + str(URLstotal) + " URLS in " + str(elapsed_time))
	return str(elapsed_time)


def show_progress(counter, totalURLs, start_time):

	# Calculate perfectage of URLs already reviewed
	percentage_complete = ( float(counter) / float(totalURLs) ) * 100
	time = datetime.now().strftime('%I:%M %p')

	# Formatted only for hours and minutes as requested
	print("\t" + time + '\t' +  format(percentage_complete, '2.0f') + '% complete')


# from get_all_active_urls import get_all_urls as scrape_urls
def print_contents_of_list(list):

	# for item in list:
		# print("Item {}:\n" .format( str(counter) ) )
		# for i in item.keys():
			# print( "\t{}:\t{}".format( str(i), str(item[i]) ) )
	for item in list:
		sku = str(item['sku'])
		name = ascii(item['item']).strip("b'").rstrip("'")
		url = str(item['url'])
		print("{}\t{}\t{}".format(sku, name, url))

# --------------------------------------------------------------------------------
# GLOBAL VARIABLES:

start_time = datetime.now()
zero_items = []
missing_cart_buttons = []
unchecked_URLs = []
counter = 0

# --------------------------------------------------------------------------------
# MAIN PROCESS:

print("Step 1 of 2: Taking snapshot of all currently active URLs.\n\n")

# Hit xml sitemap
r = requests.get("https://www.mr-s-leather.com/sitemap.xml")
xml = r.text

# Find every <loc> tag,
soup = BeautifulSoup(xml, 'lxml')
url_bs_object = soup.body.find_all('loc')

# Make a native/usable list from data in BeautifulSoup object
URLs =[]
for i in url_bs_object:
	URLs.extend(i.contents)

totalURLs = len(URLs)

print("\tFinished scraping sitemap -- found {} active URLs.\n\n".format(str(totalURLs)))
print("Step 2 of 2: Scanning all {} URLs for prices and add-to-cart buttons.\n\n".format(str(totalURLs)))
print('\tStatus updates (% complete):\n')

# print('\t00:00:00 \t0% complete')

# URLs = URLs[500:510]

for i in URLs:

	counter += 1
	if ( counter % 100 ) == 0:
		show_progress(counter, totalURLs, start_time)

	try:

		if 'https://www.mr-s-leather.com/promo' in i:
			continue
		elif 'vonnda.net' in i:
			continue

		else:
			response = requests.get(i)
			html = response.text
			soup = BeautifulSoup(html, 'html5lib')

			# ITEM PAGE BLOCK
			try:
				if(soup.find(attrs={'id':'product-details'})):

					button = soup.find("button", attrs={"id": "product-addtocart-button"})

					if button is None:

						missing_cart_buttons.append( {
							"url" : i ,
							"item" : soup.find(attrs={'itemprop':'name'}).get_text().encode('utf-8', errors='replace'),
							"sku" : soup.find(attrs={'itemprop':'sku'}).get_text() } )

			except:

				continue

			# CATEGORY / RELATED ITEM BLOCK
			try:
				for price in soup.find_all(attrs={'class':'price'}):

					price_check = float(price.get_text().strip( '$' ).replace(',',''))
					if (price_check < 0.01 ):

						name = price.parent.parent.parent.parent.parent.a.get_text().replace('\n', '').strip()
						sku = BeautifulSoup((requests.get(price.parent.parent.parent.parent.parent.a['href']).text), 'html5lib').find(attrs={'itemprop':'sku'}).get_text()
						zero_items.append( { "url" : i , "item" : name , "sku" : sku  } )

			except:
				continue
	except:
		unchecked_URLs.append(i)

# --------------------------------------------------------------------------------
# PRINT RESULTS TO CONSOLE AND EMAIL:

print()

if missing_cart_buttons or zero_items or unchecked_URLs:

	if missing_cart_buttons:
		print("-"*80)
		print('Missing "add-to-cart" buttons:')
		print_contents_of_list(missing_cart_buttons)

	if zero_items:
		print("-"*80)
		print('"$0.00" listings (and where they appeared):')
		print_contents_of_list(zero_items)

	if unchecked_URLs:
		print("-"*80)
		print('Unable to check the following URLs:')
		print_contents_of_list(unchecked_URLs)

else:
	print("Werq -- no new items found")
	print("zero_items:")
	print(zero_items)
	print("missing_cart_buttons:")
	print(missing_cart_buttons)
	print("unchecked_URLs:")
	print(unchecked_URLs)

elapsed_time = report_zeros(totalURLs, start_time)

time_taken_message = "<br><br> Scanned " + str(len(URLs)) + " URLs IN " + elapsed_time

if zero_items or missing_cart_buttons or unchecked_URLs:

	message_body = ""

	if missing_cart_buttons:
		message_body += '<br>'
		message_body += '<br>'
		message_body += 'MISSING ADD-TO-CART-BUTTONS:'
		message_body += '<br>'
		for i in missing_cart_buttons:
			message_body += '<br>URL:\t' + str(i["url"])
			message_body += '<br>Item\t' + str(i["item"])
			message_body += '<br>Sku:\t' + str(i["sku"])
			message_body += '<br>'

	if zero_items:
		message_body += '<br>'
		message_body += '<br>'
		message_body += '$0 ITEMS APPEAR ON FOLLOWING PAGES'
		for i in zero_items:
			message_body += '<br>URL:\t' + str(i["url"])
			message_body += '<br>Item:\t' + str(i["item"])
			message_body += '<br>Sku:\t' + str(i["sku"])
			message_body += '<br>'

	if unchecked_URLs:
		message_body += '<br>'
		message_body += '<br>'
		message_body += 'UNABLE TO CHECK THE FOLLOWING PAGES - CHECK THESE MANUALLY:'
		for i in unchecked_URLs:
			message_body += '<br>URL:\t' + str(i["url"])

	message_body += time_taken_message


	# message = emails.html(html="<p>Potential $0 items to look at: <br><br>" + str(zero_items), subject="$0 items found!", mail_from=('$0 Bot', 'webmanager@mr-s-leather.com'))
	message = emails.html(html=message_body, subject="ITEMS FOUND: " + start_time.strftime('%I:%M %p'), mail_from=('MR S BOT', 'product-unavailability-bot@gmail.com'))
	# message.attach(data=open('bill.pdf', 'rb'), filename='bill.pdf')

	send = message.send(to='will.wms@gmail.com', smtp={'host': 'aspmx.l.google.com', 'timeout': 5})
	assert send.status_code == 250

else:

	message_body = "No new items / issues found"

	message_body += time_taken_message

	# message = emails.html(html="<p>Potential $0 items to look at: <br><br>" + str(zero_items), subject="$0 items found!", mail_from=('$0 Bot', 'webmanager@mr-s-leather.com'))
	message = emails.html(html=message_body, subject="No new issues: " + start_time.strftime('%I:%M %p'), mail_from=('Mr. S Bot', 'mr-s-bot@gmail.com'))
	# message.attach(data=open('bill.pdf', 'rb'), filename='bill.pdf')

	send = message.send(to='will.wms@gmail.com', smtp={'host': 'aspmx.l.google.com', 'timeout': 5})
	assert send.status_code == 250

# from twilio.rest import Client

# # Find these values at https://twilio.com/user/account
# account_sid = "AC14deb9aa6bc4a96d140dfebd73934f8c"
# auth_token = "your_auth_token"

# client = Client(account_sid, auth_token)

# client.api.account.messages.create(
#     to="+12316851234",
#     from_="+15555555555",
#     body="Hello there!")

# print("Variable names:")
# print("zero_items")
# print("missing_cart_buttons")
# print("unchecked_URLs")
# print("results")
