gallery = the 'div' that holds all images and videos
imgs = []
videos = []

PROBLEM: every image exists twice on page: 1. div revealed for med/browser viewports, and 2. div revealed for sm/mobile viewports
(Example: the neoprene blue jock (NEO108B) has 5 pics)
pics = soup.find_all('div', attrs={"class":"gallery-image-container"})
len(pics)
10 ==> actually there are only 5 unique images

SOLUTION: first make soup object from medium/browswer viewport and navigate to its descendants.

BeautifulSoup selectors:

gallery:
.find('div',attrs={"class":"medium-3 columns hide-for-small-only"})
.get: n/a

images:
.find_all('div', attrs={"class":"gallery-image-container"})
.get: 'background-image'

videos:
.find_all('div', attrs={"class":"gallery-image-container js-chosen-video" })
.get: 'data-videourl'


videos = [] // hold img urls
imgs = [] // hold video urls


gallery.find()
gallery.find_all()


ex1 (buttballs cocksling)
IMG:14
VID:2
"https://www.mr-s-leather.com/sex-toys/oxballs/buttballs-cocksling-ass-lock"

ex2 (holy trainer ring)
IMG:1
VID:3
"https://www.mr-s-leather.com/ring-for-v3-holy-trainer"

ex3 (neoprene blue jock)
IMG:5
VID:00
"https://www.mr-s-leather.com/neoprene-double-stripe-jock-blue"