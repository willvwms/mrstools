import pickle

with open('classified_images.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    images = pickle.load(f)

print("Successfully loaded classified images into memory!")
print("Total images = " + str(len(images))) 

product_counter = 0
action_counter = 0
combined_counter = 0
neither_counter = 0
edge_cases = 0

for image in images:
	if image['product_still'] and not image['action_shot']:
		product_counter += 1
	elif not image['product_still'] and image['action_shot']:
		action_counter += 1
	elif image['product_still'] and image['action_shot']:
		combined_counter += 1
	elif not image['product_still'] and not image['action_shot']:
		neither_counter += 1
	else:
		edge_cases += 1


print("product_counter:")
print(str(product_counter))
print("action_counter:")
print(str(action_counter))
print("combined_counter:")
print(str(combined_counter))
print("neither_counter:")
print(str(neither_counter))
print("edge_cases:")
print(str(edge_cases))
print()
print("Sum of all counters should equal " + str(len(images)))
print("Sum is actually " + str(product_counter + action_counter + combined_counter + neither_counter + edge_cases)) 

