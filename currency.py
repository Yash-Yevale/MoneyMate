from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse

r=requests.get("https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=EUR").content
soup = BeautifulSoup(r, "html.parser")

a=soup.find_all("p", attrs={"class": "result__BigRate-sc-1bsijpp-1 iGrAod"})

print(a)
a=str(a)

a=a.split(">")
a=a[1].split("<")
a=a[0]
print(a)
