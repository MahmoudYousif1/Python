from bs4 import BeautifulSoup
from pip._vendor import requests
import pandas as pd
from IPython.display import display, HTML



def title(soup):
    try:
        title = soup.find("span", attrs={"id": "productTitle"})
        title_name = title.get_text(strip=True) if title else ""
    except AttributeError:
        title_name = ""
    return title_name



def prices(soup):
    try:
        price = soup.find("span", attrs={"class": "a-price-whole"})
        price_value = price.get_text(strip=True) if price else ""
    except AttributeError:
        price_value = ""
    return price_value



def ratings(soup):
    try:
        rating = soup.find("span", attrs={"class": "a-icon-alt"})
        rating_text = rating.get_text(strip=True) if rating else ""
    except AttributeError:
        rating_text = ""
    return rating_text



def reviews(soup):
    try:
        review = soup.find("span", attrs={"id": "acrCustomerReviewText"})
        review_text = review.get_text(strip=True) if review else ""
    except AttributeError:
        review_text = ""
    return review_text




URL = "https://www.amazon.co.uk/s?k=playstation+5&crid=1DZW6085PFENM&sprefix=playst%2Caps%2C76&ref=nb_sb_ss_ts-doa-p_2_6"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")


product_list = []

for link in links:
    product_path = link.get("href")
    if product_path.startswith("/"):
        product_url = "https://www.amazon.co.uk" + product_path
    else:
        product_url = product_path

    product_response = requests.get(product_url, headers=HEADERS)
    product_soup = BeautifulSoup(product_response.text, "html.parser")

    product_data = {
        "Title": title(product_soup),
        "Price": prices(product_soup),
        "Rating": ratings(product_soup),
        "Reviews": reviews(product_soup)
    }

    product_list.append(product_data)


df = pd.DataFrame(product_list)


display(HTML(df.to_html()))