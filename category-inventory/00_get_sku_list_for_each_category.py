import requests
from bs4 import BeautifulSoup
import bondage, leather, neoprene, puppy, rubber, sextoys, sport
import os
import json

# GLOBAL VARIABLES & FUNCTIONS

failed_scrapes = list()

def get_soup(url):
  response = requests.get(url).text
  soup = BeautifulSoup(response, "html5lib")
  return soup

def get_skus_in_category(categories_list):
  counter = 1
  categories_and_their_products = dict()
  print("Total categories to scrape: {}\n".format(len(categories_list)))

  for category in categories_list:

    try:
      category_name = category.replace("https://www.mr-s-leather.com/","").replace("-"," ").replace("/"," => ").title()
      print("Scanning {} ({})".format( counter, category_name) )

      soup = get_soup(category)
      products = soup.find('div',attrs={"class":"medium-9"}).find_all('a',attrs={"class":"product-item-link"})

      skus = []

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

      categories_and_their_products.update( {category_name : skus} )

      counter += 1

    except Exception as err:
      failed_scrapes.append(category)
      print("============================================")
      print("SKIPPED {}".format(category) )
      print("Error:")
      print("line: " + str(sys.exc_info()[-1].tb_lineno) )
      print(err)
      print("============================================")

      counter +=1

  return categories_and_their_products

bondage = bondage.endpoints
sextoys = sextoys.endpoints
leather = leather.endpoints
rubber = rubber.endpoints
neoprene = neoprene.endpoints
sport = sport.endpoints
puppy = puppy.endpoints

all_categories = []
all_categories.extend(bondage)
all_categories.extend(sextoys)
all_categories.extend(leather)
all_categories.extend(rubber)
all_categories.extend(neoprene)
all_categories.extend(sport)
all_categories.extend(puppy)

def main():
  inventory = get_skus_in_category(all_categories)

  # Serialize as JSON
  # os.chdir("C:/Users/mrs.BradBlandin-PC/Desktop")
  with open('category-inventory.json', 'w') as f:
    json.dump(inventory, f, indent=1)

  print(json.dumps(inventory, indent=1))

# MAIN PROCESS
main()
