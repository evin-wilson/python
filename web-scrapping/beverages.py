import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

###---------------------------------------------------- www.uptownspirits,com ----------------------------------------------------
base_url = "https://uptownspirits.com/"
req = requests.get(base_url, headers=headers)
print(req.status_code)
src = req.content
sheets={}
for items in soup.findAll('li',{'class':'category'}):
    name = []
    prize = []
    url = items.a['href']
    bottle = items.a.text
    
    while url:
        src = requests.get(url, headers=headers).text
        soup = BeautifulSoup(src, "lxml")
        inner_div = soup.findAll("div", {"class" : "product-inner product-item__inner"})
        for item in inner_div:
            try:
                n = item.find("h2").text
                p = item.find("span",{"class": "woocommerce-Price-amount amount"}).text
                name.append(n)
                prize.append(p)
            except:
                prize.append("None")
        try:    
            next_page = soup.find('a',{'class':'next page-numbers'})
            url = next_page['href']
        except:
            break
        print(url)
        print(" ")
    df = pd.DataFrame({"Name":name, "prize":prize})
    sheets[bottle] = df
    
writer = pd.ExcelWriter('scrapping_uptownspirits.xlsx', engine='xlsxwriter')
for bottle in sheets.keys():
    sheets[bottle].to_excel(writer, sheet_name=bottle,index=False)
writer.save()



### ----------------------------------------------------- www.reservebar.com  -----------------------------------------------------
urls = [
    "https://www.reservebar.com/collections/scotch",
    "https://www.reservebar.com/collections/all-bourbon",
    "https://www.reservebar.com/collections/whiskey-bourbon",
    "https://www.reservebar.com/collections/tequila",
    "https://www.reservebar.com/collections/cognac",
    "https://www.reservebar.com/collections/vodka",
    "https://www.reservebar.com/collections/gin",
    "https://www.reservebar.com/collections/rum",
    "https://www.reservebar.com/collections/liqueur",
    "https://www.reservebar.com/collections/moonshine",
    "https://www.reservebar.com/collections/cocktails-mixers",
    "https://www.reservebar.com/collections/champagne",
    "https://www.reservebar.com/collections/wine"
]

sheets={}
for url in urls:
    name = []
    prize = []
    re1 = requests.get(url, headers=headers).text
    soup1 = BeautifulSoup(re1, 'lxml')
    title = soup1.find('title').text
    spirits = title.partition('|')[0]
    print(spirits)
    while url:
        req = requests.get(url, headers=headers).text
        soup = BeautifulSoup(req, 'lxml')
        for items in soup.findAll('li',{'class':'grid__item grid__item--collection-template small--one-half medium-up--one-quarter'}):
            div = items.find('div',{'class':'h4 grid-view-item__title product-card__title'}).text
            span = items.find('span',{'class':'price-item price-item--sale'}).text

            prize.append(span.strip())
            name.append(div)
        # Walk through the pages    
        try:
            ul = soup.find('ul',{'class':'list--inline pagination'})
            page = ul.select_one('ul li:nth-of-type(3)').find('a')['href']
            url = "https://www.reservebar.com/"+page[1:]
            print(url)
        except:
            break
    # Create pandas dataframe from acquired dat
    df = pd.DataFrame({'Name':name,'Prize':prize})
    # save dataframes in dict with sheet-name as key 
    sheets[spirits] = df
    print('  ')
# Create pandas Excelwritter
writer = pd.ExcelWriter('scrapper_reservebar.xlsx', engine='xlsxwriter')

# loop through the sheets and save it as excel object
for spirits in sheets:
	# Convert the dataframe to an XlsxWriter Excel object.
    sheets[spirits].to_excel(writer, sheet_name=spirits, index=False)
writer.save()



### ------------------------------------------------------ www.delmesaliquor.com ------------------------------------------------------ 

urls = {
    'barrel-picks':'https://www.delmesaliquor.com/product-category/spirits/barrel-picks/',
    'spirits':'https://www.delmesaliquor.com/product-category/spirits/?product_count=72',
    'wine':'https://www.delmesaliquor.com/product-category/wine/?product_count=72',
    'craft-beer':'https://www.delmesaliquor.com/product-category/craft-beer/?product_count=72',
    'soda-snaks':'https://www.delmesaliquor.com/product-category/sodas-snacks/'
}

sheets ={}
for bottle,url in urls.items():
	print(bottle)
	name = []
	prize = []
    while url:
        req = requests.get(url, headers=headers).text
        soup = BeautifulSoup(req, 'lxml')
        for i in soup.find('ul',{'class':'products clearfix products-4'}).findAll('li'):
            n=i.find('h3').a.text.strip()
            try:
                p = i.find('ins').find('span',{'class','woocommerce-Price-amount amount'}).text.strip()
                p_ = i.find('span',{'class','woocommerce-Price-amount amount'}).text.strip()
            except:
                try:
                    p=i.find('span',{'class','woocommerce-Price-amount amount'}).text.strip()
                except:
                    p='null'
            name.append(n)
            prize.append(p)
        try:
            url = soup.find('nav',{'class':'woocommerce-pagination'}).find('a',{'class':'next page-numbers'})['href']
            print(url)
        except:
            break
    df = pd.DataFrame({'Name':name,'Prize':prize})
    sheets[bottle] = df
    
writer = pd.ExcelWriter('scrapping_delmesaliquor.xlsx', engine='xlsxwriter')
for bottle in sheets.keys():
    sheets[bottle].to_excel(writer, sheet_name=bottle,index=False)
writer.save()


