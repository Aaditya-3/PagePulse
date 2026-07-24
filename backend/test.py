from bs4 import BeautifulSoup
import requests

soup = BeautifulSoup(requests.get("https://www.google.com").text , "html.parser")
print(type(soup.title))
print(type(soup))
print(soup.title.string)
print(soup.title.text)
print(type(soup.get_text()))
