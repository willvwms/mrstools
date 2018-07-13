import pickle

# Want to work with 2 files: 
# 1. List (sorted)
# 2. object (dicttionary)

# READ from file (DE-SERIALIZE)
with open('video_urls.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    video_urls = pickle.load(f)

print("Loaded video urls!")
print("len(video_urls) = " + str(len(video_urls)))
print()
