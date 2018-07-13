import pickle
import webbrowser
import random

# Want to work with 2 files: 
# 1. List (sorted)
# 2. object (dicttionary)

# READ from file (DE-SERIALIZE)
with open('all_image_data.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    images = pickle.load(f)

print("Loaded all {} images".format( str(len(images)) ) )
print()
print("Exaple of data for a randomly chosen image:")
print()
random_choice = random.randint(0, len(images))

for key, value in images[random_choice].items():
	if key == 'labels':
		print('\t' + key.upper() )
		print('\t\tWORD\t\tSCORE')
		for x in value:
			print('\t\t{}\t\t{}'.format( x['word'], str(x['score']).format('0.2f') ) )
	else:
		print('\t{}\t{}'.format( key.upper(), str(value) ) )

