import pickle
import webbrowser

action = [
	"barechestedness",
	"muscle",
	"man",
	"male",
	"arm",
	"chest",
	"body man",
	"facial hair",
	"neck",
	"abdomen",
	"mouth",
	"hand",
	"boy",
	"bodybuilder",
	"wrestler",
	"model",
	"chin",
	"leg",
	"finger",
	"standing",
	"fetish model",
	"joint",
	"chest hair",
	"shoulder",
	"flesh",
	"thigh",
	"beard",
	"human body",
	]

still = [
	"product design",
	"product",
	"black and white",
	"monochrome",
	"metal",
	"still life photography",
	"monochrome photography",
	"hardware",
	"fashion accessory",
	"automotive design",
	"silver",
	"black",
	"photography",
	"strap",
	"angle",
	"technology",
	"hardware accessory",
	"brand",
	"computer wallpaper",
	"audio equipment",
	"glass",
	"personal protective equipment",
	"buckle",
	"leather",
	"belt",
	"close up",
	"material",
	"shoe",
	"jewellery",
	"light",
	"ring",
	"audio",
	"bottle",
	"circle",
	"liquid",
	"wheel",
	"glass bottle",
	"plastic",
	"headgear",
	"macro photography",
	"mask",
	"cylinder",
	"electronics accessory",
	"figurine",
	"weapon",
	"body jewelry",
	"tool",
	"sculpture",
	"chain",
	"automotive exterior",
	"electronic device",  
	]

with open('image_urls_gcv_processed.pickle', 'rb') as f:
# The protocol version used is detected automatically, so we do not
# have to specify it.
	images = pickle.load(f)

for x in images:

	x['standard_product_shot'] = False
	x['action_shot'] = False
	x['xxx'] = False
	x['safe'] = False

	standard_product_shot = x['standard_product_shot']
	action_shot = x['action_shot']
	xxx = x['xxx']

	labels = x['labels']

	for label in labels:

		# vars for indiv labels
		word = label['word']
		score = label['score']

		# vars for image data points:
		adult = x['adult']
		racy = x['racy']
		nsfw = x['nsfw']

		# vars image T/F flags
		standard_product_shot = x['standard_product_shot']
		action_shot = x['action_shot']
		xxx = x['xxx']
		safe = x['safe']



		# ---------------------------------------
		# Test determine if this is an action shot:

		action_counter = 0

		if (word in action) and (score > .5):

			action_counter += 1

		if (action_counter > 2 ):


		# ---------------------------------------

		if (label['word'] in action) and (x['nsfw'] > .7) and (x['adult'] >3) and (x['racy'] > 3):

			x['xxx'] = True

			xxx_urls.append(x['url'])

		if (label['word'] in action) and ( (x['nsfw'] < .7) or (x['adult'] <= 3) or (x['racy'] <= 3) ) :

			x['pg13']

			pg13_urls.append(x['url'])

		if (label['word'] in still) and (label['word'] not in action) and (x['nsfw'] < .4):

			x['standard_product_shot'] = True

			still_urls.append(x['url'])

# WRITE data object to file (SERIALIZE)
with open('classified_images.pickle', 'wb') as f:
	# Pickle the 'data' dictionary using the highest protocol available.
	pickle.dump(images, f, pickle.HIGHEST_PROTOCOL)

print("x['standard_product_shot']")
print("x['action_shot']")
print("x['pg13']")
print("x['xxx']")
