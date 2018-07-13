import pickle
import webbrowser
from functools import reduce

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
	"automotive eimageterior",
	"electronic device",  
	]

# ---------------------------------------------------------------------------------

with open('all_image_data.pickle', 'rb') as f:
# The protocol version used is detected automatically, so we do not
# have to specify it.
	all_images = pickle.load(f)

# *********************************************************************************
# *********************************************************************************
# PART I. SUMMARTIZE/SORT THE DATA
#         
# Goal: Get an overview of the data points returned by Deep AI and Google Cloud Vision
# in order to choose a more meaningful sample for review in PART II (Interpretation)
# *********************************************************************************
# *********************************************************************************

# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
print( '\n\n\n' + ('='*60) )
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

# TEST 1:  
# See the range and distribution of Deep AI's nsfw ratings 
# How: sort individual ratings into brackets by .1 increments (0.00 to 1.00)

nsfw_up_to_1, nsfw_up_to_point_9, nsfw_up_to_point_8, nsfw_up_to_point_7, nsfw_up_to_point_6, nsfw_up_to_point_5, nsfw_up_to_point_4, nsfw_up_to_point_3, nsfw_up_to_point_2, nsfw_up_to_point_1, nsfw_unclassified, = [], [], [], [], [], [], [], [], [], [], []

for image in all_images:

	rating = image['nsfw']

	if   (rating <= 1.0 ) and (rating  > .9):
		nsfw_up_to_1.append(image)

	elif (rating <= .9 ) and (rating  > .8 ):
		nsfw_up_to_point_9.append(image)

	elif (rating <= .8 ) and (rating  > .7 ):		
		nsfw_up_to_point_8.append(image)

	elif (rating <= .7 ) and (rating  > .6 ):
		nsfw_up_to_point_7.append(image)

	elif (rating <= .6 ) and (rating  > .5 ):
		nsfw_up_to_point_6.append(image)

	elif (rating <= .5 ) and (rating  > .4 ):
		nsfw_up_to_point_5.append(image)

	elif (rating <= .4 ) and (rating  > .3 ):
		nsfw_up_to_point_4.append(image)

	elif (rating <= .3 ) and (rating  > .2 ):
		nsfw_up_to_point_3.append(image)

	elif (rating <= .2 ) and (rating  > .1 ):
		nsfw_up_to_point_2.append(image)

	elif (rating <= .1 ) and (rating  >= 0 ):
		nsfw_up_to_point_1.append(image)

	else:
		nsfw_unclassified.append(image)

# Check that no images escaped classification in the above sorting (should be zero):
# (If any results here, go back and fix the sorting structure)
print("(1) DEEP AI: \tNSFW RATING (0.0 - 1.0):")
print()
print("Unclassified: \t\t " + str(len(nsfw_unclassified)).rjust(5) + ' images')

# Stick each bracket into one master list for iterating:
nsfw_sorted_10_brackets = []
nsfw_sorted_10_brackets.append(nsfw_up_to_point_1)
nsfw_sorted_10_brackets.append(nsfw_up_to_point_2)
nsfw_sorted_10_brackets.append(nsfw_up_to_point_3)
nsfw_sorted_10_brackets.append(nsfw_up_to_point_4)
nsfw_sorted_10_brackets.append(nsfw_up_to_point_5)
nsfw_sorted_10_brackets.append(nsfw_up_to_point_6)
nsfw_sorted_10_brackets.append(nsfw_up_to_point_7)
nsfw_sorted_10_brackets.append(nsfw_up_to_point_8)
nsfw_sorted_10_brackets.append(nsfw_up_to_point_9)
nsfw_sorted_10_brackets.append(nsfw_up_to_1)

# Total images sorted:
sublist_lengths = [ len(sublist) for sublist in nsfw_sorted_10_brackets ]
total_nsfw = reduce( (lambda x,y : x+y) , sublist_lengths ) 


# Print statistics about the sorting to the console:
for bracket in nsfw_sorted_10_brackets:

	rating_values = []

	for image in bracket:

		rating = image['nsfw']
		rating_values.append(rating)

	bracket_min = str( min( rating_values ) )
	bracket_max = str( max( rating_values ) )
	bracket_count = str( len( bracket ) )
	percent = round( int( bracket_count ) / total_nsfw * 100  )

	print("Range {} to {}:\t {} images \t< {}% >".format( bracket_min, bracket_max, bracket_count.rjust(5), str(percent).format('.0f') ) )

print()
print( "Total:\t\t\t {} ".format( total_nsfw ).rjust(5) + 'images' )

# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
print( '\n\n\n' + ('='*60) )
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

# TEST 2: GOOGLE IMAGE LABELS 

# Two-part examination:
# See overall range and distribution of Google Cloud Vision's label scores 
# The scores represent the applicability of a label to the image.
# Goal is to find whether there is anything meaningful in the score distribution
# to assist in filtering the data points later.

# ---------------------------------------------------------------------------------
# Test 2 - Part 1: GOOGLE LABELS (SCORE DISTRIBUTION)
# See the distribution of individual label scores (i.e., GCV's confidence in a label's accuracy) 
# How: sort individual labels into brackets by their score in .1 incremenets (0.0 - 1.0)
# ---------------------------------------------------------------------------------

cgv_label_scores_up_to_1, cgv_label_scores_up_to_point_9, cgv_label_scores_up_to_point_8, cgv_label_scores_up_to_point_7, cgv_label_scores_up_to_point_6, cgv_label_scores_up_to_point_5, cgv_label_scores_up_to_point_4, cgv_label_scores_up_to_point_3, cgv_label_scores_up_to_point_2, cgv_label_scores_up_to_point_1, cgv_label_scores_unclassified, = [], [], [], [], [], [], [], [], [], [], []

for image in all_images:

	for label in image['labels']:

		score = label['score']

		if   (score <= 1.0 ) and (score  > .9):
			cgv_label_scores_up_to_1.append(score)

		elif (score <= .9 ) and (score  > .8 ):
			cgv_label_scores_up_to_point_9.append(score)

		elif (score <= .8 ) and (score  > .7 ):		
			cgv_label_scores_up_to_point_8.append(score)

		elif (score <= .7 ) and (score  > .6 ):
			cgv_label_scores_up_to_point_7.append(score)

		elif (score <= .6 ) and (score  > .5 ):
			cgv_label_scores_up_to_point_6.append(score)

		elif (score <= .5 ) and (score  > .4 ):
			cgv_label_scores_up_to_point_5.append(score)

		elif (score <= .4 ) and (score  > .3 ):
			cgv_label_scores_up_to_point_4.append(score)

		elif (score <= .3 ) and (score  > .2 ):
			cgv_label_scores_up_to_point_3.append(score)

		elif (score <= .2 ) and (score  > .1 ):
			cgv_label_scores_up_to_point_2.append(score)

		elif (score <= .1 ) and (score  >= 0 ):
			cgv_label_scores_up_to_point_1.append(score)

		else:
			cgv_label_scores_unclassified.append(score)

# Check that no images escaped classification in the above sorting (should be zero):
# (If any results here, go back and fix the sorting structure)
print("(2) GOOGLE CLOUD VISION: \tIMAGE CONTENT LABELS")
print()
print()
print('\t' + '-'*52)
print("\t2(a) Individual Label Scores (0.00 - 1.00):")
print()
print("\tUnclassified: \t\t " + str(len(cgv_label_scores_unclassified)).rjust(5) + ' scores')

# Stick each bracket into one master list for iterating:
gcv_label_scores_sorted_10_brackets = []
gcv_label_scores_sorted_10_brackets.append(cgv_label_scores_up_to_point_1)
gcv_label_scores_sorted_10_brackets.append(cgv_label_scores_up_to_point_2)
gcv_label_scores_sorted_10_brackets.append(cgv_label_scores_up_to_point_3)
gcv_label_scores_sorted_10_brackets.append(cgv_label_scores_up_to_point_4)
gcv_label_scores_sorted_10_brackets.append(cgv_label_scores_up_to_point_5)
gcv_label_scores_sorted_10_brackets.append(cgv_label_scores_up_to_point_6)
gcv_label_scores_sorted_10_brackets.append(cgv_label_scores_up_to_point_7)
gcv_label_scores_sorted_10_brackets.append(cgv_label_scores_up_to_point_8)
gcv_label_scores_sorted_10_brackets.append(cgv_label_scores_up_to_point_9)
gcv_label_scores_sorted_10_brackets.append(cgv_label_scores_up_to_1)

# total_nsfw = max(map(len, nsfw_sorted_10_brackets))
sublist_lengths = [ len(sublist) for sublist in gcv_label_scores_sorted_10_brackets ]
total_gcv_label_scores = reduce( (lambda x,y : x+y) , sublist_lengths ) 

# Print statistics about the sorting to the console:
bracket_min, bracket_max = -.1, 0
for bracket in gcv_label_scores_sorted_10_brackets:
	bracket_min += .1
	bracket_min_string = str( round(bracket_min, 1) )
	bracket_max += .1
	bracket_max_string = str( round(bracket_max, 1) )
	bracket_count = len( bracket )
	percent = round( int( bracket_count ) / total_gcv_label_scores * 100  )
	print("\tRange {} to {}:\t {} scores\t< {}% >".format( str(bracket_min_string), str(bracket_max_string), str(bracket_count).rjust(5), str(percent).format('.0f') ) )

print()
print( "\tTotal:\t\t\t {} ".format( total_gcv_label_scores ).rjust(5) + 'scores' )
print('\t' + '-'*52)

# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
print()
print()
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

# Test 2 - Part 2: GOOGLE LABELS (COUNTS)
# Examine the range/distribution in the number of labels GCV assigned to every image
# How: Classify images by number of labels assigned (10 brackets, 0 - 10 labels)
# ---------------------------------------------------------------------------------

cgv_label_count_10, cgv_label_count_9, cgv_label_count_8, cgv_label_count_7, cgv_label_count_6, cgv_label_count_5, cgv_label_count_4, cgv_label_count_3, cgv_label_count_2, cgv_label_count_1, cgv_label_count_0, cgv_label_count_unclassified, = [], [], [], [], [], [], [], [], [], [], [], []

for image in all_images:

	count = len(image['labels'])

	if   (count == 10):
		cgv_label_count_10.append(image)

	elif (count == 9):
		cgv_label_count_9.append(image)

	elif (count == 8 ) :
		cgv_label_count_8.append(image)

	elif (count == 7 ) :
		cgv_label_count_7.append(image)

	elif (count == 6 ) :
		cgv_label_count_6.append(image)

	elif (count == 5 ) :
		cgv_label_count_5.append(image)

	elif (count == 4 ) :
		cgv_label_count_4.append(image)

	elif (count == 3 ) :
		cgv_label_count_3.append(image)

	elif (count == 2 ) :
		cgv_label_count_2.append(image)

	elif (count == 1 ) :
		cgv_label_count_1.append(image)
	
	elif (count == 0 ) :
		cgv_label_count_0.append(image)

	else:
		cgv_label_counts_unclassified.append(image)

# Check that no images escaped classification in the above sorting (should be zero):
# (If any results here, go back and fix the sorting structure)
print('\t' + '-'*52)
print("\t2(b) Number of Labels per Image (0 - 10):")
print()
print("\tUnclassified: \t\t " + str(len(cgv_label_scores_unclassified)).rjust(5) + ' images')

# Stick each bracket into one master list for iterating:
gcv_label_counts_sorted_11_brackets = []
gcv_label_counts_sorted_11_brackets.append(cgv_label_count_0)
gcv_label_counts_sorted_11_brackets.append(cgv_label_count_1)
gcv_label_counts_sorted_11_brackets.append(cgv_label_count_2)
gcv_label_counts_sorted_11_brackets.append(cgv_label_count_3)
gcv_label_counts_sorted_11_brackets.append(cgv_label_count_4)
gcv_label_counts_sorted_11_brackets.append(cgv_label_count_5)
gcv_label_counts_sorted_11_brackets.append(cgv_label_count_6)
gcv_label_counts_sorted_11_brackets.append(cgv_label_count_7)
gcv_label_counts_sorted_11_brackets.append(cgv_label_count_8)
gcv_label_counts_sorted_11_brackets.append(cgv_label_count_9)
gcv_label_counts_sorted_11_brackets.append(cgv_label_count_10)

# total_nsfw = max(map(len, nsfw_sorted_10_brackets))
sublist_lengths = [ len(sublist) for sublist in gcv_label_counts_sorted_11_brackets ]
total_gcv_label_counts = reduce( (lambda x,y : x+y) , sublist_lengths ) 

# Print statistics about the sorting to the console:
bracket_number = 0
for bracket in gcv_label_counts_sorted_11_brackets:
	
	bracket_count = len( bracket )
	percent =  round( ( int( bracket_count ) / total_gcv_label_counts ) * 100 ) 

	print("\t{} labels:\t\t {} images\t< {}% >".format( str( bracket_number ), str(bracket_count).rjust(5), str(percent).format('.0f') ) )
	bracket_number += 1

print()
print( "\tTotal:\t\t\t {} ".format( total_gcv_label_counts ).rjust(5) + 'images' )
print('\t' + '-'*52)
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
print( '\n\n\n' + ('='*60) )
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# TEST 3: 	GOOGLE SAFE SEARCH -- ADULT
# Examine distribution of GCV's evaluation of each image for "adult" content (0 - 5)
# How: Classify images by rating (range: 0 - 5, integers) 
# 0 = "Unknown" 
# 1 = "Very Unlikely" 
# 5 = "Very Likely"
# ---------------------------------------------------------------------------------

adult_rated_5, adult_rated_4, adult_rated_3, adult_rated_2, adult_rated_1, adult_rated_0, adult_unclassified, = [], [], [], [], [], [], []

for image in all_images:

	adult_rated_rating = image['adult']

	if (adult_rated_rating == 5 ) :
		adult_rated_5.append(image)

	elif (adult_rated_rating == 4 ) :
		adult_rated_4.append(image)

	elif (adult_rated_rating == 3 ) :
		adult_rated_3.append(image)

	elif (adult_rated_rating == 2 ) :
		adult_rated_2.append(image)

	elif (adult_rated_rating == 1 ) :
		adult_rated_1.append(image)
	
	elif (adult_rated_rating == 0 ) :
		adult_rated_0.append(image)

	else:
		adult_unclassified.append(image)

# Check that no images escaped classification in the above sorting (should be zero):
# (If any results here, go back and fix the sorting structure)
print("(3) GOOGLE CLOUD VISION: ADULT")
print()
print("Unclassified: \t\t " + str(len(adult_unclassified)).rjust(5) + ' images')

# Stick each bracket into one master list for iterating:
adult_sorted_6_brackets = []
adult_sorted_6_brackets.append(adult_rated_0)
adult_sorted_6_brackets.append(adult_rated_1)
adult_sorted_6_brackets.append(adult_rated_2)
adult_sorted_6_brackets.append(adult_rated_3)
adult_sorted_6_brackets.append(adult_rated_4)
adult_sorted_6_brackets.append(adult_rated_5)

sublist_lengths = [ len(sublist) for sublist in adult_sorted_6_brackets ]
total_adult = reduce( (lambda x,y : x+y) , sublist_lengths ) 

# Print statistics about the sorting to the console:
bracket_number = 0
for bracket in adult_sorted_6_brackets:
	
	bracket_count = len( bracket )
	percent = round( int( bracket_count ) / total_adult * 100  )

	print("Rated {}:\t\t {} images\t< {}% >".format( str( bracket_number ), str(bracket_count).rjust(5), str(percent).format('.0f') ) )
	bracket_number += 1

print()
print( "Total:\t\t\t {} ".format( total_adult ).rjust(5) + 'images' )
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
print( '\n\n\n' + ('='*60) )
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# TEST 4: 	GOOGLE SAFE SEARCH -- RACY
# Examine distribution of GCV's evaluation of each image for "racy" content (0 - 5)
# How: Classify images by rating (range: 0 - 5, integers) 
# 0 = "Unknown" 
# 1 = "Very Unlikely" 
# 5 = "Very Likely"
# ---------------------------------------------------------------------------------

racy_rated_5, racy_rated_4, racy_rated_3, racy_rated_2, racy_rated_1, racy_rated_0, racy_unclassified, = [], [], [], [], [], [], []

for image in all_images:

	racy_rated_rating = image['racy']

	if (racy_rated_rating == 5 ) :
		racy_rated_5.append(image)

	elif (racy_rated_rating == 4 ) :
		racy_rated_4.append(image)

	elif (racy_rated_rating == 3 ) :
		racy_rated_3.append(image)

	elif (racy_rated_rating == 2 ) :
		racy_rated_2.append(image)

	elif (racy_rated_rating == 1 ) :
		racy_rated_1.append(image)
	
	elif (racy_rated_rating == 0 ) :
		racy_rated_0.append(image)

	else:
		racy_unclassified.append(image)

# Check that no images escaped classification in the above sorting (should be zero):
# (If any results here, go back and fix the sorting structure)
print("(4) GOOGLE CLOUD VISION: RACY")
print()
print("Unclassified: \t\t " + str(len(racy_unclassified)).rjust(5) + ' images')

# Stick each bracket into one master list for iterating:
racy_sorted_6_brackets = []
racy_sorted_6_brackets.append(racy_rated_0)
racy_sorted_6_brackets.append(racy_rated_1)
racy_sorted_6_brackets.append(racy_rated_2)
racy_sorted_6_brackets.append(racy_rated_3)
racy_sorted_6_brackets.append(racy_rated_4)
racy_sorted_6_brackets.append(racy_rated_5)

sublist_lengths = [ len(sublist) for sublist in racy_sorted_6_brackets ]
total_racy = reduce( (lambda x,y : x+y) , sublist_lengths ) 

# Print statistics about the sorting to the console:
bracket_number = 0
for bracket in racy_sorted_6_brackets:
	
	bracket_count = len( bracket )
	percent = round( int( bracket_count ) / total_racy * 100  )

	print("Rated {}:\t\t {} images\t< {}% >".format( str( bracket_number ), str(bracket_count).rjust(5), str(percent).format('.0f') ) )
	bracket_number += 1

print()
print( "Total:\t\t\t {} ".format( total_racy ).rjust(5) + 'images' )

# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
print( '\n\n\n' + ('='*60) )
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# TEST 5: 	GOOGLE SAFE SEARCH -- MEDICAL
# Examine distribution of GCV's evaluation of each image for "medical" content (0 - 5)
# How: Classify images by rating (range: 0 - 5, integers) 
# 0 = "Unknown" 
# 1 = "Very Unlikely" 
# 5 = "Very Likely"
# ---------------------------------------------------------------------------------


medical_rated_5, medical_rated_4, medical_rated_3, medical_rated_2, medical_rated_1, medical_rated_0, medical_unclassified, = [], [], [], [], [], [], []

for image in all_images:

	medical_rated_rating = image['medical']

	if (medical_rated_rating == 5 ) :
		medical_rated_5.append(image)

	elif (medical_rated_rating == 4 ) :
		medical_rated_4.append(image)

	elif (medical_rated_rating == 3 ) :
		medical_rated_3.append(image)

	elif (medical_rated_rating == 2 ) :
		medical_rated_2.append(image)

	elif (medical_rated_rating == 1 ) :
		medical_rated_1.append(image)
	
	elif (medical_rated_rating == 0 ) :
		medical_rated_0.append(image)

	else:
		medical_unclassified.append(image)

# Check that no images escaped classification in the above sorting (should be zero):
# (If any results here, go back and fix the sorting structure)
print("(5) GOOGLE CLOUD VISION: MEDICAL")
print()
print("Unclassified: \t\t " + str(len(medical_unclassified)).rjust(5) + ' images')

# Stick each bracket into one master list for iterating:
medical_sorted_6_brackets = []
medical_sorted_6_brackets.append(medical_rated_0)
medical_sorted_6_brackets.append(medical_rated_1)
medical_sorted_6_brackets.append(medical_rated_2)
medical_sorted_6_brackets.append(medical_rated_3)
medical_sorted_6_brackets.append(medical_rated_4)
medical_sorted_6_brackets.append(medical_rated_5)

sublist_lengths = [ len(sublist) for sublist in medical_sorted_6_brackets ]
total_medical = reduce( (lambda x,y : x+y) , sublist_lengths ) 

# Print statistics about the sorting to the console:
bracket_number = 0
for bracket in medical_sorted_6_brackets:
	
	bracket_count = len( bracket )
	percent = round( int( bracket_count ) / total_medical * 100  )

	print("Rated {}:\t\t {} images\t< {}% >".format( str( bracket_number ), str(bracket_count).rjust(5), str(percent).format('.0f') ) )
	bracket_number += 1

print()
print( "Total:\t\t\t {} ".format( total_medical ).rjust(5) + 'images' )

# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
print( '\n\n\n' + ('='*60))
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------


# *********************************************************************************
# *********************************************************************************
# PART II. INSPECT IMAGES & INTERPRET THEIR ASSOCIATED DATA
# 
# How: View a 10% sample of each sorted data set to determine where human/company 
# assessment of images' NSFWness corresponds to the data points returned from each API.
# *********************************************************************************
# *********************************************************************************

choices = {
	"nsfw 0 to .1": nsfw_up_to_point_1,
	"nsfw .1 to .2": nsfw_up_to_point_2,
	"nsfw .2 to .3": nsfw_up_to_point_3,
	"nsfw .3 to .4": nsfw_up_to_point_4,
	"nsfw .4 to .5": nsfw_up_to_point_5,
	"nsfw .5 to .6": nsfw_up_to_point_6,
	"nsfw .6 to .7": nsfw_up_to_point_7,
	"nsfw .7 to .8": nsfw_up_to_point_8,
	"nsfw .8 to .9": nsfw_up_to_point_9,
	"nsfw .9 to 1.0": nsfw_up_to_1,
	"adult rated 0" : adult_rated_0,
	"adult rated 1" : adult_rated_1,
	"adult rated 2" : adult_rated_2,
	"adult rated 3" : adult_rated_3,
	"adult rated 4" : adult_rated_4,
	"adult rated 5" : adult_rated_5,
	"racy rated 0" : racy_rated_0,
	"racy rated 1" : racy_rated_1,
	"racy rated 2" : racy_rated_2,
	"racy rated 3" : racy_rated_3,
	"racy rated 4" : racy_rated_4,
	"racy rated 5" : racy_rated_5,
	"medical rated 0" : medical_rated_0,
	"medical rated 1" : medical_rated_1,
	"medical rated 2" : medical_rated_2,
	"medical rated 3" : medical_rated_3,
	"medical rated 4" : medical_rated_4,
	"medical rated 5" : medical_rated_5,
	"label count 0" : cgv_label_count_0,
	"label count 1" : cgv_label_count_1,
	"label count 2" : cgv_label_count_2,
	"label count 3" : cgv_label_count_3,
	"label count 4" : cgv_label_count_4,
	"label count 5" : cgv_label_count_5,
	"label count 6" : cgv_label_count_6,
	"label count 7" : cgv_label_count_7,
	"label count 8" : cgv_label_count_8,
	"label count 9" : cgv_label_count_9
	}

keep_going = 'y'
while keep_going == 'y':

	user_input = None
	sample = None

	print('-'*60)
	print("Enter exact name of the list you want to sample:")
	for x in choices.keys():
		print('\t' + x)
	print('-'*60)

	print()

	while (user_input not in choices.keys()) :
		user_input = input("Enter the exact name of the list you want to sample: ")
		user_input.lower().strip()
		if user_input not in choices.keys():
			print("Sorry, didn't get that -- try again")

	sample = choices[user_input]

	# check_sample = eval(input("Enter the name of the sorted to check: "))
	
	for x in sample[0::10]:
		webbrowser.open_new(x['url'])

		print('-'*50)
		print('URL:\t' + x['url'])
		print('\tSKU:\t' + x['sku'])
		print('\tNSFW:\t' + str(x['nsfw']) )
		print('\tAdult:\t' + str(x['adult']) )
		print('\tRacy:\t' + str(x['racy']) )
		print('\tMedical:\t' + str(x['medical']) )
		print()

	# Prompt user to check another sample:
	keep_going = input("Keep going with another set? Enter 'y' or 'n': ")
	keep_going.lower()
	if keep_going == 'y' or keep_going == 'n':
		continue
	else: 
		print()
		print("Sorry, didn't get that --")
		input("Keep going with another set? Enter 'y' or 'n': ")
		print()