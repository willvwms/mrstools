import pickle

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

with open('all_image_data.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    images = pickle.load(f)

for image in images:

  image['product_still'] = False
  image['action_shot'] = True

  words = [ x['word'] for x in image['labels'] ]

  # for label in image['labels']:

  #   word = label['word']:
  
  if any(matched_term in words for matched_term in action):
    image['action_shot'] = True

  if any(matched_term in words for matched_term in still):
    image['product_still'] = True
    
# WRITE data object to file (SERIALIZE)
# with open('classified_images.pickle', 'wb') as f:
#     # Pickle the 'data' dictionary using the highest protocol available.
#     pickle.dump(image_urls, f, pickle.HIGHEST_PROTOCOL)

    # for label in response['labelAnnotations']:
#   words = label['description'].split(" ") 
#   print(any(word in words for word in action))