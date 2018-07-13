import io
import os
import pickle

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "S:\\Internet Sales Office\\Web\\credentials\\google-cloud-vision\\mr-s-image-project-8827e477db4a.json"

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Labels
def detect_labels_uri(uri):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    # print('Labels:')

    # for label in labels:
    #     print(label.description)

    return labels

# Safe Search

def detect_safe_search_uri(uri):
    """Detects unsafe features in the file located in Google Cloud Storage or
    on the Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    # likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
    #                    'LIKELY', 'VERY_LIKELY')
    # print('Safe search:')

    # print('adult: {}'.format(likelihood_name[safe.adult]))
    # print('medical: {}'.format(likelihood_name[safe.medical]))
    # print('spoofed: {}'.format(likelihood_name[safe.spoof]))
    # print('violence: {}'.format(likelihood_name[safe.violence]))
    # print('racy: {}'.format(likelihood_name[safe.racy]))

    return safe


with open('image_urls_w_nsfw_rating.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    image_urls = pickle.load(f)

# print("Loaded image urls!")
# print("len(image_urls) = " + str(len(image_urls)))
# print()

# Variables to report to console during processing:
error_urls = []
counter = 0

# for image in image_urls[500:510]:
for image in image_urls:

    counter += 1

    try:
        url = image['url']

        safe_search_object = detect_safe_search_uri(url)
        labels_object = detect_labels_uri(url)

        labels = []
        for item in labels_object:
            word = item.description
            score = round(item.score, 2)
            label = { "word": word, "score": score  }
            labels.append(label)

        image['labels'] = labels
        image['adult'] = safe_search_object.adult
        image['racy'] = safe_search_object.racy
        image['medical'] = safe_search_object.medical

        print("Processed image " + str(counter) + " of " + str(len(image_urls)) )

    except:

        error_urls.append(image)

        print("============================================")
        print("Skipped: " + image['sku'] + '\n' + image['url'])
        print("line: " + str(sys.exc_info()[-1].tb_lineno) )
        print(err)
        print("============================================")

print("Finished!")
print()


# WRITE data object to file (SERIALIZE)
with open('image_urls_gcv_processed.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(image_urls, f, pickle.HIGHEST_PROTOCOL)


# WRITE ERRORS list to file (SERIALIZE)
with open('error_urls.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(error_urls, f, pickle.HIGHEST_PROTOCOL)