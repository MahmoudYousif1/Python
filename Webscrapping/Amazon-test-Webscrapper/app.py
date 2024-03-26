from bs4 import BeautifulSoup
import requests
import pandas as pd
from flask import Flask, request

app = Flask(__name__)

def title(soup):
    try:
        title = soup.find("span", attrs={"id": "productTitle"})
        title_name = title.get_text(strip=True) if title else ""
        
    except AttributeError:
        title_name = ""
        
    except AssertionError:
        title_name = ""
        
    return title_name

def prices(soup):
    try:
        price = soup.find("span", attrs={"class": "a-price-whole"})
        price_value = price.get_text(strip=True) if price else ""
        
    except AttributeError:
        
        price_value = ""
        
    except ArithmeticError:
        price_value = 0
        
    return f" {price_value}00"


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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_query = request.form.get("search_query")
        if search_query:
            loading_html = """
                <html>
                <head>
                    <style>
                        /* Styles for sorted tables */
                        table.sorted {
                            width: 90%;
                            margin: 20px auto;
                            border-collapse: collapse;
                            border: 2px solid #007BFF;
                        }
                        th, td {
                            padding: 10px;
                            text-align: left;
                            border-bottom: 1px solid #ddd;
                            font-size: 16px;
                        }
                        th {
                            background-color: #007BFF;
                            color: white;
                        }

                        /* Styles for loading spinner */
                        .loading {
                            text-align: center;
                            margin: 20px;
                        }
                        .spinner {
                            border: 4px solid rgba(255, 255, 255, 0.3);
                            border-top: 4px solid #007BFF;
                            border-radius: 50%;
                            width: 30px;
                            height: 30px;
                            animation: spin 2s linear infinite;
                            margin: 0 auto;
                        }
                        @keyframes spin {
                            0% { transform: rotate(0deg); }
                            100% { transform: rotate(360deg); }
                        }
                    </style>
                </head>
                <body>
                    <div class="loading">
                        <div class="spinner"></div>
                    </div>
                    <script>
                        document.querySelector("form").style.display = "none";
                    </script>
                </body>
                </html>
            """
            return loading_html + fetch_and_display_results(search_query)

    return """
        <html>
        <head>
            <style>
                /* Styles for search container */
                body {
                    background-color: black;
                    color: white;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                .search-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                    margin: 20px;
                }
                input[type="text"] {
                    padding: 10px;
                    width: 400px;
                    font-size: 18px;
                }
                button {
                    padding: 10px 20px;
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-size: 18px;
                }
                table {
                    width: 90%;
                    margin: 20px auto;
                    border-collapse: collapse;
                    border: 2px solid #007BFF;
                }
                th, td {
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                    font-size: 16px;
                }
                th {
                    background-color: #007BFF;
                    color: white;
                }
            </style>
        </head>
        <body>
            <div class="search-container">
                <form method="POST">
                    <input type="text" name="search_query" placeholder="Search for a product">
                    <button type="submit">Search</button>
                </form>
            </div>
        </body>
        </html>
    """

def fetch_and_display_results(search_query):
    search_url = f"https://www.amazon.co.uk/s?k={search_query.replace(' ', '+')}"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
    }
    response = requests.get(search_url, headers=HEADERS)
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
            
    sorted_by_price = sorted(product_list, key=lambda x: float(x.get("Price").replace(",", "").strip("£")) if x.get("Price") else 0, reverse=False)
    sorted_by_ratings = sorted(product_list, key=lambda x: float(x.get("Rating").split(' ')[0]) if ' ' in x.get("Rating") and x.get("Rating").split(' ')[0].isdigit() else 0, reverse=True)
    sorted_by_reviews = sorted(product_list, key=lambda x: int(x.get("Reviews").replace(",", "").split(' ')[0]) if x.get("Reviews") else 0, reverse=True)
    
    return f"""
            <html>
            <head>
                <style>
                    /* Styles for sorted tables */
                    table.sorted {{
                        width: 90%;
                        margin: 20px auto;
                        border-collapse: collapse;
                        border: 2px solid #007BFF;
                    }}
                    th, td {{
                        padding: 10px;
                        text-align: left;
                        border-bottom: 1px solid #ddd;
                        font-size: 16px;
                    }}
                    th {{
                        background-color: #007BFF;
                        color: white;
                    }}

                    /* Styles for loading spinner */
                    .loading {{
                        text-align: center;
                        margin: 20px;
                    }}
                    .spinner {{
                        border: 4px solid rgba(255, 255, 255, 0.3);
                        border-top: 4px solid #007BFF;
                        border-radius: 50%;
                        width: 30px;
                        height: 30px;
                        animation: spin 2s linear infinite;
                        margin: 0 auto;
                    }}
                    @keyframes spin {{
                        0% {{ transform: rotate(0deg); }}
                        100% {{ transform: rotate(360deg); }}
                    }}
                </style>
            </head>
            <body>
                <div class="loading">
                    <div class="spinner"></div>
                </div>
                <script>
                    document.querySelector("form").style.display = "none";
                </script>
                <h1>Products sorted by cheapest Price</h1>
                {generate_table(sorted_by_price)}
                <h1>Products sorted by Most Ratings</h1>
                {generate_table(sorted_by_ratings)}
                <h1>Products sorted by Most Reviews</h1>
                {generate_table(sorted_by_reviews)}
            </body>
            </html>
        """

def generate_table(product_list):
    table_html = """
        <table class="sorted">
            <tr>
                <th>Title</th>
                <th>Price</th>
                <th>Rating</th>
                <th>Reviews</th>
            </tr>
    """

    for product in product_list:
        table_html += f"""
            <tr>
                <td>{product['Title']}</td>
                <td>{product['Price']}</td>
                <td>{product['Rating']}</td>
                <td>{product['Reviews']}</td>
            </tr>
        """

    table_html += "</table>"
    return table_html

if __name__ == "__main__":
    app.run(debug=True)
