from flask import Flask             # used to create Server
from flask import render_template   # return & show HTML doc
from flask import request           # gets Form parameters
app = Flask('app')                  # creates application

import requests                     # makes get request to websites
from bs4 import BeautifulSoup       # reads HTML document
import concurrent.futures           # helps in multi-threading
import time                         # os timestamp

base_url = "https://www.coinlore.com/"
urls = []                           # all pages to be scraped
coins = []                          # all coins & its details

# Step 1: Prepare URLS of pages to be scraped
def pages(i):
  for p in range(i):
    urls.append(base_url+str(p+1))
  print('URLs ready')

# Step 2: Web Scrape required data
def scrape(url):
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html.parser")
  table = soup.find('table', attrs={'id':'mainpagetable'})
  table_body = table.find('tbody')
  rows = table_body.find_all('tr')
  
  print('scraping...')
  for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      coins.append([ele for ele in cols if ele])

# Step 3: Scrape WITHOUT MultiThreading
def sequentialScrape(scan_urls):
  print('Sequential')
  t1 = time.time()
  for p in scan_urls:
    scrape(p)
  t2 = time.time()  
  t = t2-t1
  print('Done in ',t,' secs')
  return t
  
# Step 4: Scrape WITH MultiThreading
def parallelScrape(scan_urls):
  print('Parallel')
  t1 = time.time()
  with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(scrape, scan_urls)
  t2 = time.time() 
  t = t2-t1
  print('Done in ',t,' secs')
  return t

# Step 5: 
@app.route('/', methods=['POST'])
def webscraper():
  multi = int(request.form['multi'])
  i = int(request.form['i'])
  pages(i)
  if multi == 1:
    time_taken = parallelScrape(urls)  
  else:
    time_taken = sequentialScrape(urls)  
  cryptos = coins
  urls.clear() 
  return render_template("index.html", **locals())

# Step 6: Display page & data
@app.route('/', methods=['GET'])
def hello_world():
  return render_template("index.html", **locals())

app.run(host='0.0.0.0', port=8080)      # creates server
