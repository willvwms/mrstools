import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json

# ------------------------------------------------------------------------------
# GLOBAL VARIABLES
# ------------------------------------------------------------------------------
categories = [
 "https://www.mr-s-leather.com/bondage-bdsm/bdsm-restraints/wrist-restraints-ankle-restraints",
 "https://www.mr-s-leather.com/bondage-bdsm/bdsm-restraints/heavy-bondage-restraints",
 "https://www.mr-s-leather.com/bondage-bdsm/bdsm-restraints/bondage-mitts-restraints",
 "https://www.mr-s-leather.com/bondage-bdsm/gags",
 "https://www.mr-s-leather.com/bondage-bdsm/blindfolds",
 "https://www.mr-s-leather.com/bondage-bdsm/collars-leashes",
 "https://www.mr-s-leather.com/bondage-bdsm/bondage-hoods-muzzles/leather-hoods-muzzles-masks",
 "https://www.mr-s-leather.com/bondage-bdsm/bondage-hoods-muzzles/rubber-hoods-muzzles-masks",
 "https://www.mr-s-leather.com/bondage-bdsm/bondage-hoods-muzzles/neoprene-hoods-muzzles-masks",
 "https://www.mr-s-leather.com/bondage-bdsm/bondage-hoods-muzzles/spandex-hoods-muzzles-masks",
 "https://www.mr-s-leather.com/bondage-bdsm/bondage-hoods-muzzles/muzzles",
 "https://www.mr-s-leather.com/bondage-bdsm/bondage-hoods-muzzles/bdsm-masks",
 "https://www.mr-s-leather.com/bondage-bdsm/bondage-hoods-muzzles/gas-masks",
 "https://www.mr-s-leather.com/bondage-bdsm/sleepsacks",
 "https://www.mr-s-leather.com/bondage-bdsm/straitjackets",
 "https://www.mr-s-leather.com/bondage-bdsm/suspension",
 "https://www.mr-s-leather.com/bondage-bdsm/fetters-usa-bondage",
 "https://www.mr-s-leather.com/bondage-bdsm/iron-restraints",
 "https://www.mr-s-leather.com/bondage-bdsm/handcuffs",
 "https://www.mr-s-leather.com/bondage-bdsm/male-chastity",
 "https://www.mr-s-leather.com/bondage-bdsm/floggers-whips/floggers",
 "https://www.mr-s-leather.com/bondage-bdsm/floggers-whips/whips",
 "https://www.mr-s-leather.com/bondage-bdsm/paddles-canes/paddles",
 "https://www.mr-s-leather.com/bondage-bdsm/paddles-canes/canes-crops",
 "https://www.mr-s-leather.com/bondage-bdsm/rope-tape",
 "https://www.mr-s-leather.com/bondage-bdsm/spreader-bars",
 "https://www.mr-s-leather.com/bondage-bdsm/locks-accessories",
 "https://www.mr-s-leather.com/sex-toys/ass-play/square-peg-silicone-ass-play",
 "https://www.mr-s-leather.com/sex-toys/ass-play/oxballs-silicone-ass-play",
 "https://www.mr-s-leather.com/sex-toys/ass-play/perfect-fit-ass-play",
 "https://www.mr-s-leather.com/sex-toys/ass-play/hankey-s-toys-dildos",
 "https://www.mr-s-leather.com/sex-toys/ass-play/butt-plugs-ass-play",
 "https://www.mr-s-leather.com/sex-toys/ass-play/cock-extenders",
 "https://www.mr-s-leather.com/sex-toys/ass-play/suction-cup-dildos",
 "https://www.mr-s-leather.com/sex-toys/ass-play/double-ended-sex-toys-dildos",
 "https://www.mr-s-leather.com/sex-toys/ass-play/dildo-harnesses-ass-play",
 "https://www.mr-s-leather.com/sex-toys/ass-play/vibes-prostate-ass-play",
 "https://www.mr-s-leather.com/sex-toys/ass-play/realistic-cocks",
 "https://www.mr-s-leather.com/sex-toys/ass-play/vac-u-lock-sex-toys",
 "https://www.mr-s-leather.com/sex-toys/ass-play/inflatable-dildos-ass-play",
 "https://www.mr-s-leather.com/sex-toys/ass-play/vixen-silicone-ass-play",
 "https://www.mr-s-leather.com/sex-toys/ass-play/pvc-vinyl-sex-toys",
 "https://www.mr-s-leather.com/sex-toys/ass-play/anal-beads",
 "https://www.mr-s-leather.com/sex-toys/ass-play/metal-sex-toys",
 "https://www.mr-s-leather.com/sex-toys/ass-play/depth-toys-ass-play",
 "https://www.mr-s-leather.com/sex-toys/ass-prep-douche-enema-toys",
 "https://www.mr-s-leather.com/sex-toys/square-peg-sex-toys/peg-away-putty",
 "https://www.mr-s-leather.com/sex-toys/square-peg-sex-toys/square-peg-beginner",
 "https://www.mr-s-leather.com/sex-toys/square-peg-sex-toys/square-peg-intermediate",
 "https://www.mr-s-leather.com/sex-toys/square-peg-sex-toys/square-peg-advanced",
 "https://www.mr-s-leather.com/sex-toys/square-peg-sex-toys/square-peg-expert",
 "https://www.mr-s-leather.com/sex-toys/square-peg-sex-toys/square-peg-plugs",
 "https://www.mr-s-leather.com/sex-toys/square-peg-sex-toys/square-peg-fisting",
 "https://www.mr-s-leather.com/sex-toys/square-peg-sex-toys/square-peg-cocks",
 "https://www.mr-s-leather.com/sex-toys/square-peg-sex-toys/square-peg-depth",
 "https://www.mr-s-leather.com/sex-toys/square-peg-sex-toys/square-peg-puppy-play-tails",
 "https://www.mr-s-leather.com/sex-toys/square-peg-sex-toys/all-square-peg",
 "https://www.mr-s-leather.com/sex-toys/cock-ball/stretch-cock-ball-toys",
 "https://www.mr-s-leather.com/sex-toys/cock-ball/metal-cockrings",
 "https://www.mr-s-leather.com/sex-toys/cock-ball/metal-ball-stretchers-ball-weights",
 "https://www.mr-s-leather.com/sex-toys/cock-ball/leather-cockstraps",
 "https://www.mr-s-leather.com/sex-toys/cock-ball/cock-ball-torture-cbt",
 "https://www.mr-s-leather.com/sex-toys/cock-ball/oxballs-cock-ball",
 "https://www.mr-s-leather.com/sex-toys/oxballs",
 "https://www.mr-s-leather.com/sex-toys/electro-play/power-boxes-electro-play",
 "https://www.mr-s-leather.com/sex-toys/electro-play/butt-toys-electro-play",
 "https://www.mr-s-leather.com/sex-toys/electro-play/cock-ball-toys-electro-play",
 "https://www.mr-s-leather.com/sex-toys/electro-play/more-toys-electro-play",
 "https://www.mr-s-leather.com/sex-toys/electro-play/wires-accessories-electro-play",
 "https://www.mr-s-leather.com/sex-toys/electro-play/violet-wands-electro-play",
 "https://www.mr-s-leather.com/sex-toys/electro-play/electrastim",
 "https://www.mr-s-leather.com/sex-toys/electro-play/erostek",
 "https://www.mr-s-leather.com/sex-toys/electro-play/e-stim-systems",
 "https://www.mr-s-leather.com/sex-toys/electro-play/mystim",
 "https://www.mr-s-leather.com/sex-toys/nexus",
 "https://www.mr-s-leather.com/sex-toys/fleshjack-strokers",
 "https://www.mr-s-leather.com/sex-toys/perfect-fit",
 "https://www.mr-s-leather.com/sex-toys/penis-pumping",
 "https://www.mr-s-leather.com/sex-toys/urethral-sounding",
 "https://www.mr-s-leather.com/sex-toys/tit-toys",
 "https://www.mr-s-leather.com/sex-toys/medical-sex-toys",
 "https://www.mr-s-leather.com/sex-toys/lube-cleaner-boner-pills",
 "https://www.mr-s-leather.com/sex-toys/gloves-condoms",
 "https://www.mr-s-leather.com/sex-toys/fucking-machines",
 "https://www.mr-s-leather.com/sex-toys/fuck-sheets",
 "https://www.mr-s-leather.com/sex-toys/sex-slings-furniture",
 "https://www.mr-s-leather.com/sex-toys/books-music",
 "https://www.mr-s-leather.com/leather/leather-harnesses",
 "https://www.mr-s-leather.com/leather/leather-jocks",
 "https://www.mr-s-leather.com/leather/leather-shorts-leather-kilts",
 "https://www.mr-s-leather.com/leather/leather-pants-leather-chaps",
 "https://www.mr-s-leather.com/leather/leather-shirts-leather-vests",
 "https://www.mr-s-leather.com/leather/leather-belts-sam-browne",
 "https://www.mr-s-leather.com/leather/leather-suspenders",
 "https://www.mr-s-leather.com/leather/leather-caps-hats-leather-gloves",
 "https://www.mr-s-leather.com/leather/leather-jackets",
 "https://www.mr-s-leather.com/leather/leather-boots/all-boot-care-boot-accessories",
 "https://www.mr-s-leather.com/leather/leather-boots/all-boots",
 "https://www.mr-s-leather.com/leather/leather-wristbands-leather-armbands",
 "https://www.mr-s-leather.com/leather/leather-accessories",
 "https://www.mr-s-leather.com/rubber/rubber-jocks-shorts",
 "https://www.mr-s-leather.com/rubber/rubber-pants-rubber-chaps",
 "https://www.mr-s-leather.com/rubber/rubber-shirts-latex-shirts",
 "https://www.mr-s-leather.com/rubber/latex-rubber-suits-rubber-bondage",
 "https://www.mr-s-leather.com/rubber/rubber-harnesses",
 "https://www.mr-s-leather.com/rubber/rubber-socks-latex-gloves",
 "https://www.mr-s-leather.com/rubber/rubber-accessories",
 "https://www.mr-s-leather.com/neoprene/neoprene-jocks-neoprene-shorts",
 "https://www.mr-s-leather.com/neoprene/neoprene-pants-neoprene-chaps",
 "https://www.mr-s-leather.com/neoprene/neoprene-shirts-neoprene-vests",
 "https://www.mr-s-leather.com/neoprene/neoprene-suits-neoprene-bondage",
 "https://www.mr-s-leather.com/neoprene/neoprene-harnesses",
 "https://www.mr-s-leather.com/neoprene/neoprene-accessories",
 "https://www.mr-s-leather.com/sportwear-streetwear/fuckgear",
 "https://www.mr-s-leather.com/sportwear-streetwear/open-ass-gear",
 "https://www.mr-s-leather.com/sportwear-streetwear/jockstraps",
 "https://www.mr-s-leather.com/sportwear-streetwear/underwear",
 "https://www.mr-s-leather.com/sportwear-streetwear/socks",
 "https://www.mr-s-leather.com/sportwear-streetwear/singlets",
 "https://www.mr-s-leather.com/sportwear-streetwear/tees-tanks",
 "https://www.mr-s-leather.com/sportwear-streetwear/shorts-kilts",
 "https://www.mr-s-leather.com/sportwear-streetwear/pants",
 "https://www.mr-s-leather.com/sportwear-streetwear/jackets-hoodies",
 "https://www.mr-s-leather.com/sportwear-streetwear/caps-accessories",
 "https://www.mr-s-leather.com/sportwear-streetwear/cellblock13",
 "https://www.mr-s-leather.com/sportwear-streetwear/maskulo",
 "https://www.mr-s-leather.com/sportwear-streetwear/do-it",
 "https://www.mr-s-leather.com/sportwear-streetwear/mr-s-leather-logo-gear",
 "https://www.mr-s-leather.com/sportwear-streetwear/nasty-pig/nasty-pig-jocks-socks-and-caps",
 "https://www.mr-s-leather.com/sportwear-streetwear/nasty-pig/nasty-pig-sportswear-and-swimwear",
 "https://www.mr-s-leather.com/sportwear-streetwear/boxer-barcelona",
 "https://www.mr-s-leather.com/puppy-park/neoprene-puppy-hoods",
 "https://www.mr-s-leather.com/puppy-park/neoprene-muzzles",
 "https://www.mr-s-leather.com/puppy-park/leather-puppy-hoods",
 "https://www.mr-s-leather.com/puppy-park/leather-muzzles",
 "https://www.mr-s-leather.com/puppy-park/rubber-puppy-hoods",
 "https://www.mr-s-leather.com/puppy-park/puppy-collars-leashes",
 "https://www.mr-s-leather.com/puppy-park/puppy-tails-mitts",
 "https://www.mr-s-leather.com/puppy-park/puppy-tees-accessories"
]

now = datetime.now()
date, time = now.strftime("%m-%d-%y"), now.strftime("%H-%M") # 03/13/28, 10:10 AM
failed_scrapes = list()

# ------------------------------------------------------------------------------
# GLOBAL FUNCTIONS
# ------------------------------------------------------------------------------
def get_soup(url):
  response = requests.get(url).text
  soup = BeautifulSoup(response, "html5lib")
  return soup

def get_skus(category):
  skus = []
  try:
    soup = get_soup(category)
    products = soup.find('div',attrs={"class":"medium-9"}).find_all('a',attrs={"class":"product-item-link"})
    for element in products:
      try:
        sku = get_soup(element.get('href')).find(attrs={'itemprop':'sku'}).get_text(strip=True)
        skus.append(sku)
      except Exception as err:
        failed_scrapes.append(category)
        print("============================================")
        print("SKIPPED #{}".format(category) )
        print("Error:")
        print("line: " + str(sys.exc_info()[-1].tb_lineno) )
        print(err)
        print("============================================")
        print("failed on #{}".format(counter))
        skus.append("REDIRECTED? {}".format(element.get('href')))
    return skus
  except Exception as err:
    print("============================================")
    print("Error scraping {}".format(category))
    print("line: " + str(sys.exc_info()[-1].tb_lineno) )
    print(err)
    skus.append("REDIRECTED? {}".format(element.get('href')))
    print("============================================")
    return skus

def validate_inventory(data):
  for category, contents in data.items():
    if len(contents) < 1:
      print("Re-scraping {}".format(category))
      contents = rescrape(category)
      validate_inventory(data)

def build_inventory(categories_list):
  counter = 1
  categories_and_their_products = dict()
  print("Total categories to scrape: {}\n".format(len(categories_list)))
  for category in categories_list:
    try:
      print("Scanning {} of {} ({})".format( counter, len(categories_list), category[category.rfind("/")+1:] ) )
      categories_and_their_products.update( {category : get_skus(category) } )
      counter += 1
    except Exception as err:
      failed_scrapes.append(category)
      print("============================================")
      print("SKIPPED {}".format(category) )
      print("Error:")
      print("line: " + str(sys.exc_info()[-1].tb_lineno) )
      print(err)
      print("============================================")
      categories_and_their_products.update( {category : [] } )
      counter +=1
  return categories_and_their_products

# ------------------------------------------------------------------------------
# MAIN PROCESS
# ------------------------------------------------------------------------------
inventory = build_inventory(categories)
validate_inventory(inventory)

#Serialize as JSON
with open('../product-data-scraper/LAST-INVENTORY.json', 'w') as f:
  json.dump(inventory, f, indent=1)
with open('./archive/inventory__{}__{}.json'.format(date,time), 'w') as f:
  json.dump(inventory, f, indent=1)

print(json.dumps(inventory, indent=1))