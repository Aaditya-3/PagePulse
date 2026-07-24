from bs4 import BeautifulSoup
import requests

def parse_html(html):
    soup = BeautifulSoup(html , "html.parser")
    title = "No Title"
    if soup.title:
        title = soup.title.get_text(strip = True)

    meta_tag = soup.find("meta" , attrs = {'name' : 'description'})
    meta = "No Description"
    if meta_tag and meta_tag.get("content"):
        meta = meta_tag.get("content")

    h1_count = len(soup.find_all("h1")) # find all returns list

    images = soup.find_all("img")
    imageCount = 0
    for image in images:
        if not image.get("alt"):
            imageCount += 1

    text = soup.get_text(separator = " " , strip = True)
    words = text.split()
    wordCount = len(words)

    return{
        'title' : title,
        'meta_description' : meta , 
        'h1_count' : h1_count,
        'imagesWithMissingAlt' : imageCount,
        'wordCount' : wordCount
    }

    




    