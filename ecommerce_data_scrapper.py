import requests 
from bs4 import BeautifulSoup
import time
import pandas as pd

def Get_data():
  raw_data = []
  for page in range(1,6):
    url = "https://www.flipkart.com/search"
    headers = {
      "User-Agent": "Mozilla/5.0"
      }
    params = {
    'q': 'laptops',
    'page': page
    }
    res = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(res.text,'html.parser')
    products = soup.find_all('div', class_= 'nZIRY7')#class for products
    time.sleep(1)
    for product in products:
      name = product.find('div',class_='RG5Slk').text.strip()
      price = product.find('div',class_='hZ3P6w').text.strip()
      price = float(price.replace('₹','').replace(',',''))
      if name and price:
        name = name.text.strip()
        price = float(price.text.replace('₹','').replace(',','')#Error Handling, if div is missing
      raw_data.append({
      'name': name,
      'price': price
      })
      
    if res.status_code==429:
      time.sleep(5)
      continue
    if res.status_code != 200:
      return None
  return raw_data

def filter_data(details):
  filter_data = []
  sorted_data = sorted(details,key = lambda x:x['price'])
  for product in sorted_data:
    if product['price']<50000:
      filter_data.append(product)
  return filter_data

def Data_Format(information):
  df= pd.DataFrame(information)
  df = df.sort_values(by='price')
  df['Top Cheapest'] = 'No'
  df.iloc[:5, df.columns.get_loc('Top Cheapest')] = 'Yes'
  df.to_csv("Cheapest_Products.csv",index = False)
  print('Saved data to Cheapest_Products.csv!\n')
  return df

def main():
  print('Fetching Data...')
  time.sleep(1)
  info = Get_data()
  if info is None:
    print("Failed to fetch data")
    return
  data = filter_data(info)
  prod = Data_Format(data)
  print('Data Fetching completed!!\n')

if __name__ == '__main__':
  main()
