def to_xml(df, filename=None, mode='w'):
    def row_to_xml(row):
        xml = ['<item>']
        for i, col_name in enumerate(row.index):
            xml.append('  <field name="{0}">{1}</field>'.format(col_name, row.iloc[i]))
        xml.append('</item>')
        return '\n'.join(xml)
    res = '\n'.join(df.apply(row_to_xml, axis=1))

    if filename is None:
        return res
    with open(filename, mode) as f:
        f.write(res)


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Chrome("C:\chromedriver")
URLS=[]
data =[]
driver.get("https://www.greennote.co.uk/events-page/")
content = driver.page_source
soup = BeautifulSoup(content,'html.parser')
for event in soup.findAll('div', attrs={'class':'wp_theatre_event'}):
	URLS.append(event.find('div',attrs={'class':'wp_theatre_event_title'}).find('a')['href'])
 

for url in URLS:
	driver.get(url)
	content = driver.page_source
	soup = BeautifulSoup(content,'html.parser')
	main = soup.find('div',attrs={'class':'entry-content'})
	description = ""
	videos=[]
	for p in main.findAll('p'):
		if p.find('div',attrs={'class':'fluid-width-video-wrapper'}) is None:
			description = description+ p.text
		for v in main.findAll('div',attrs={'class':'fluid-width-video-wrapper'}):
			if v.find("iframe") is None:
				if v.find("embed") is None:
					break
				videos.append(v.find("embed").get("src"))
			else :
				videos.append(v.find("iframe").get("src"))
			
	artist=soup.find('h1',attrs={'class':'entry-title'}).text
	venues=soup.find('div',attrs={'class':'wp_theatre_event_venue'}).text
	date=soup.find('div',attrs={'class':'wp_theatre_event_datetime'}).text
	if soup.find('div',attrs={'class':'wp_theatre_event_prices'}) is None:
		price="Cancelled"
	else:
		price=soup.find('div',attrs={'class':'wp_theatre_event_prices'}).text
	newObj = {
		'Artist':artist,
		'Description':description,
		'venue':venues,
		'Date':date,
		'price':price,
		'videos':videos
	}
	data.append(newObj)
df = pd.DataFrame(data)
print(df.head())

df.to_csv('res.csv')