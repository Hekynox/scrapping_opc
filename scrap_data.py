from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urljoin

# variables des données a récupérer 
product_page_url = []
universal_product_code = []
title = []
price_including_tax = []
price_excluding_tax = []
number_available = []
product_description = []
category = []
review_rating = []
image_url = []

url = "http://books.toscrape.com/catalogue/neither-here-nor-there-travels-in-europe_198/index.html"
reponse = requests.get(url)
page = reponse.content

base_url = "http://books.toscrape.com"
# verifie que la requête est un succès
if reponse.status_code == 200:
    soup = BeautifulSoup(page, "html.parser")
    # recupere l'url
    product_page_url.append(reponse.url)

# Recuperation des données

for i in soup.find_all("table", class_="table table-striped"):
    # recuperation de l'UPC
    for upc in i.find("td"):
        universal_product_code.append(upc)
    # recuperation Prix
    for target in i.find_all("th"):
        # Recupere le prix sans taxe
        if target.get_text() == "Price (excl. tax)":
            price_no_tax = target.find_next("td")
            price_excluding_tax.append(
                price_no_tax.get_text()
            )
        # recupere le prix avec taxe
        if target.get_text() == "Price (incl. tax)":
            price_tax = target.find_next("td")
            price_including_tax.append(
                price_tax.get_text()
            )
        # recupere le nombre disponible d'exemplaire
        if target.get_text() == "Availability":
            available = target.find_next("td")
            number_available.append(
                available.get_text()
            )

for i in soup.find_all("div", class_="col-sm-6 product_main"):
    #recupere le titre 
    for title_book in i.find_all("h1"):
        title.append(title_book.get_text())
    # recupere la note
    one_star = i.find("p", class_="star-rating One")
    two_star = i.find("p", class_="star-rating Two")
    three_star = i.find("p", class_="star-rating Three")
    four_star = i.find("p", class_="star-rating Four")
    five_star = i.find("p", class_="star-rating Five")
    if one_star:
        review_rating.append("1 étoile")
    elif two_star:
        review_rating.append("2 étoiles")
    elif three_star:
        review_rating.append("3 étoiles")
    elif four_star:
        review_rating.append("4 étoiles")
    elif five_star:
        review_rating.append("5 étoiles")
    else:
        print("Not rating found")

# recupere la description
for i in soup.find_all("div", id="product_description"):
    description = i.find_next("p")
    product_description.append(description.get_text())

# recupere l'image url
for i in soup.find_all("div", class_="item active"):
    for img in i.find_all("img"):
        img_url = img["src"]
        final_url = urljoin(base_url, img_url)
        image_url.append(final_url)

# Recupere la categorie
for i in soup.find_all("li", class_="active"):
    for prev in i.find_previous("a"):
        categorie = prev.get_text()
        category.append(categorie)

# etablissement des en tetes pour le fichier csv
en_tete = [
    "product_page_url",
    "universal_product_code (upc)",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
]

# extraction des données dans un fichier csv
with open("data.csv", "w", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(en_tete)
    for (
        page_produit_url,
        code_produit,
        titre,
        price_with_tax,
        price_without_tax,
        nbr_dispo,
        prod_description,
        categories,
        notation,
        image
    ) in zip(
        product_page_url,
        universal_product_code,
        title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        product_description,
        category,
        review_rating,
        image_url
    ):
        writer.writerow([
            page_produit_url,
            code_produit,
            titre,
            price_with_tax,
            price_without_tax,
            nbr_dispo,
            prod_description,
            categories,
            notation,
            image
        ])