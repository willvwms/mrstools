import pickle

with open('image_urls_gcv_processed_PLUS_66.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    image_urls = pickle.load(f)

# for url in image_urls[0:10]:
# 	print("="*50)
# 	print("="*50)
# 	print("adult:")
# 	print(url['adult'])
# 	print("racy:")
# 	print(url['racy'])
# 	print("medical:")
# 	print(url['medical'])
# 	print()
# 	print("labels:")
# 	print("-"*25)
# 	for label in url['labels']:
# 		print('\t'+ label['word'] + ': ' + str(label['score']))
# 	print("-"*25)
# 	print()


# slice_start, slice_end = 982, 992
# for x in image_urls[slice_start:slice_end]:
# 	for y, z in x.items():
# 		print(y)
# 		print(z)
# 		print()	