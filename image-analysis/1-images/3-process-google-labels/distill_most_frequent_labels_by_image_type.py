import numpy 
import pickle

def distill_labels(set_of_label_lists, image_category):

	# Iterate over the compilation of sorted label lists
	# and pull out individual labels, consoliate them into one list
	consolidated_labels = []
	for indiv_list in set_of_label_lists:
		for label in indiv_list:
			consolidated_labels.append(label['word'])

	# Collapse consolidate list into a the unique items and their frequency
	uniques = numpy.unique(consolidated_labels, return_counts=True)	
	
	# numpy returns a numpy object: a tuple of 2 lists (1. words, 2. their frequency)
	# Extract them into simple lists, then combine them into one list of pairs using zip()
	words = uniques[0]
	frequencies = uniques[1]

	# unique_labels is a numpy_object 
	zipped = zip(words, frequencies)

	# Output to file
	filename = image_category + '_label_frequencies.txt'
	outfile = open(filename, 'w')
	for pair in zipped:
		label = str( pair[0] )
		frequency = str( pair[1] ) 
		outfile.write( label + '\t' + frequency + '\n')
	outfile.close()

nudity_set_of_label_lists = []
product_set_of_label_lists = []
undergarment_set_of_label_lists = []

with open('image_urls_gcv_processed.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    image_urls = pickle.load(f)

# Use AND operator for most common two keywords to identify most distinct/representative label sets
for x in image_urls:
	for y in x['labels']:
		if 'muscle' and 'barechestedness' in y['word']:
			nudity_set_of_label_lists.append(x['labels'])
		elif 'product' and 'design' in y['word']:
			product_set_of_label_lists.append(x['labels'])
		elif 'active undergarment' in y['word']:
			undergarment_set_of_label_lists.append(x['labels'])

distill_labels(nudity_set_of_label_lists, 'nudity')
distill_labels(product_set_of_label_lists, 'product_stills')
distill_labels(undergarment_set_of_label_lists, 'undergarment')

# # Write to csv for easy, visual sorting in excel
# outfile = open('nudity_label_frequencies.txt', 'w')
# for word in nudity_label_summary:
# 	outfile.write(str(word[0]) + '\t' + str(word[1]) + '\n')
# outfile.close()