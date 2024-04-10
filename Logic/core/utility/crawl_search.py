import requests
from bs4 import BeautifulSoup
import json

queries = ['spiderman', 'batman', 'master', 'man', 'shawshank', 'hero', 'father', 'future', 'pain', 'meal']

def get(query):
  url = "https://www.imdb.com/find/?q="+query[0]+"&s=tt&exact=true&ref_=fn_tt_ex"
  response = requests.get(url, headers={
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  })

  html_content = response.text
  soup = BeautifulSoup(html_content, 'html.parser')
  a_tags = soup.find_all('a', class_='ipc-metadata-list-summary-item__t')
  tt_values = [a['href'].split('/')[2] for a in a_tags]
  return tt_values

dic = {}
for q in queries:
  dic[q] = get(q)

file_path = './eval_data.json'
with open(file_path, "w") as json_file:
    json.dump(dic, json_file)