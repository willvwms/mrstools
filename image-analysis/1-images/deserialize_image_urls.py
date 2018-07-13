import pickle

# Want to work with 2 files: 
# 1. List (sorted)
# 2. object (dicttionary)

# READ from file (DE-SERIALIZE)
with open('image_urls.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    image_urls = pickle.load(f)

print("Loaded image urls!")
print("len(image_urls) = " + str(len(image_urls)))
print()
