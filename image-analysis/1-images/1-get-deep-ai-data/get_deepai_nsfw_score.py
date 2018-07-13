import requests
import sys
import os
import pickle

skipped_items = []

os.environ["DEEP_AI_API_KEY"] = "S:\\Internet Sales Office\\Web\\credentials\\deepAI\\key.txt"

apikey = os.environ.get["DEEP_AI_API_KEY"]

with open('image_urls.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    image_urls = pickle.load(f)


print("Loaded image urls!")
print("len(image_urls) = " + str(len(image_urls)))
print()

print("Now requesting from Deep AI")
print()

counter = 0

for dictionary in image_urls:

    try:

        url = dictionary['url']
        rating = requests.post("https://api.deepai.org/api/nsfw-detector", data={'image':url},headers={'api-key':apikey})
        dictionary['nsfw'] = rating.json()['output']['nsfw_score']

        counter += 1
        print("Updated image " + str(counter) + " out of " + str(len(image_urls)))

    except Exception as err:

        dictionary['nsfw'] = None

        skipped_items.append(dictionary)
        print("============================================")
        print("Skipped: " + dictionary['sku'] + '\n' + dictionary['url'])
        print("line: " + str(sys.exc_info()[-1].tb_lineno) )
        print(err)
        print("============================================")

print("Finished!")
print()

# WRITE to file (SERIALIZE)
with open('additional_testing.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(image_urls, f, pickle.HIGHEST_PROTOCOL)