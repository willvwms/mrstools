import pickle
import random
import webbrowser
import requests
import csv

# Want to work with 2 files: 
# 1. List (sorted)
# 2. object (dicttionary)

# READ from file (DE-SERIALIZE)
with open('00_COMPLETE_PRODUCT_DATA_LIST.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    products = pickle.load(f)

print("Loaded product array:")
print("len(products) = " + str(len(products)))
print()

# Explanation of how each record is structured:
print("""

prodcuts: 	LIST
contents: ~ 1,620 PRODUCT DICTIONARIES
	
	EACH PRODUCT DICTIONARY:
	10 kv pairs:
	
		k1 sku 				v: str
		k2 url 				v: str
		k3 name				v: str
		k4 manufacturer		v: str
		k5 ascii_description v: str
		k6 html_description	v: str
		
		k7 images 			v: LIST
							elements = strings (urls)
		
		k8 videos			v: LIST
							elements = strings (urls)

		k9 video_data 		v: LIST
							contents: 0 - 7 VIDEO DICTIONARIES
								EACH VIDEO DICTIONARY:
								2 kv pairs:

									k1: 'urls' 
									v: str

									k2: 'type' 
									v: Boolean

		k10 image_data		v: LIST
							contents: 0 - 30 IMAGE DICTIONARIES
								EACH IMAGE DICTIONARY:
								9 kv pairs:

									k1: "image_type"
									v:	None (eventually str: XXX, PG13, G)

									k2: "sku"
									v: str

									k3: "url"
									v: str

									k4: "url_match"
									v: str

									k5: "nsfw"
									v: FLOAT (0.00 - 1.00)

									k6: "adult"
									v: int (0-5)

									k7: "racy"
									v: int (0-5)
									
									k8: "medical"
									v: int (0-5)
									
									k9: "labels"  
									v: LIST
									contents: 0 - 10 LABEL DICTIONARIES

										EACH LABEL DICTIONARY:
										2 kv pairs:

											k: "word"
											v: str

											k: "score"
											v: FLOAT

Accessing data:
sku  	sample['sku']
name  	sample['name']
url  	sample['url']
mfr  	sample['manufacturer']
ascii  	sample['ascii_description']
html	sample['html_description']
imgs	[ x for x in sample['images'] ]
vids	[ x for x in sample['videos'] ]
			e.g. 
			[ webbrowser.open_new(x) for x in sample['images'] ]
			[ print(x) for x in sample['videos'] ]
labels	[ x for x in sample['image_data'] ]

""")

random_index = random.randint(0, len(products) )
sample = products[random_index]

def print_image_data(image):
	print( '\t' + ('='*50) )
	print( '\turl\t' + image['url'])
	print( '\n\tmatch?\t' + str( image['url_match'] == image['url'] ) )
	print( '\ttype\t' 	+ str(image['image_type'] )	)
	print( '\n\tnsfw\t' 	+ str( image['nsfw']	) ) 
	print( '\n\tadult\t' 	+ str( image['adult']	) ) 
	print( '\tracy\t' 	+ str( image['racy']	) ) 
	print( '\tmedical\t'+ str( image['medical']	) ) 

	print( '\n\t\tscore\t\tlabel' )
	
	for label in image['labels']:
		score, word = str( list(label.values())[1] ), list(label.values())[0]
		print('\t\t' + score + '\t\t' + word)

print("Example product:")
print('products[' + str(random_index) + ']' )
sku= print('sku\t' + sample['sku'])
name = print('name\t' + sample['name'])
url = print('url\t' + sample['url'])
display_mfr = print('mfr\t' + sample['manufacturer']) if len(sample['manufacturer']) > 0 else ''
descrip = print('description' + '\n' + ('-'*50) + '\n' + sample['ascii_description'] + '\n' + ('-'*50))
vidct = print("vids\t" + str( len(sample['videos']) ) )
imgct = print("imgs\t" + str( len(sample['images']) ) ) 
image_data = [ print_image_data(image) for image in sample['image_data'] ]

