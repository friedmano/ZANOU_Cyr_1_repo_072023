import csv
import os

import requests
from bs4 import BeautifulSoup

nom_rep_csv = "Fichier_csv"
nom_rep_image = "images"
def verif_status_code(url):
    """Prend en parametre une url, verifie son statut code et renvoie un objet BeautifulSoup si le status code = 200,
    None dans le cas contraire"""
    page = requests.get(url)
    if page.status_code == 200:
        return BeautifulSoup(page.content, "html.parser")
    else:
        return None

def list_url_categ(url_site):
    """Prend l'url du site en paramètre et renvoie une liste de dictionnaire.
    Chaque dictionnaire a comme clé le nom de la catégorie et comme valeur son url"""
    if verif_status_code(url_site) is not None:
        soup = verif_status_code(url_site)
        extract_div_content = soup.find('ul', {"class": "nav nav-list"})
        extract_a = extract_div_content.find('ul').find_all('a')
        list_dict_url_categ = list()
        dict_url_categ = dict()
        for lien in extract_a:
            dict_url_categ[lien.text.strip()] = url_site+"/"+lien.get('href')
            list_dict_url_categ.append(dict_url_categ)
            dict_url_categ = dict()
        return list_dict_url_categ
    else:
        print("Connexion echouée")

def list_url_livre(url_categ):
    """Prend en parametre l'url d'une catégorie de livre et renvoie une liste d'url de tous les livres de cette catégorie"""
    if verif_status_code(url_categ) is not None :
        list_url_livre = list()
        url_coupe = url_categ[0:len(url_categ) - 10]
        is_next = True
        while is_next:
            soup = verif_status_code(url_categ)
            extract_h3 = soup.find("ol", {'class': 'row'}).findAll("h3")
            for h3 in extract_h3:
                book_url = url_categ[0:36]+h3.findNext("a").get("href")[9:]
                list_url_livre.append(book_url)
            extract_next = soup.find("li", {"class": "next"})
            if extract_next is None:
                is_next = False
            else:
                url_categ = url_coupe + extract_next.find("a").get("href")
        return list_url_livre
    else:
        print("Connexion echouée")

def infos_livre(url_livre):
    """Prend en paramètre l'url d'un livre, extrait, transforme et renvoie toutes les informations sur un livre
    sous forme de dictionnaire"""
    if verif_status_code(url_livre) is not None :
        dict_infos_livre = dict()
        dict_infos_livre["product_page_url"] = url_livre
        rating = {"One":1,"Two":2, "Three":3, "Four":4, "Five":5}
        soup = verif_status_code(url_livre)

        extract_categ_book = soup.find("ul",{"class":"breadcrumb"}).findAll("li")[2].findNext("a").text
        extract_title = soup.find("h1").text
        if soup.find('div',{"id":"product_description"}) is not None:
            extract_product_desc = soup.find('div',{"id":"product_description"}).find_next_sibling("p").text
        else:
            extract_product_desc = ""
        extract_star_rating = soup.find("p",{"class":"star-rating"}).get("class")[1]
        extract_img_url = url_livre[0:26] + soup.find('div',{"id":"product_gallery"}).find("img").get("src")[6:]
        extrac_table = soup.find("table")
        extrac_th = extrac_table.findAll("th")
        extrac_td = extrac_table.findAll("td")
        dict_infos_livre["category"] = extract_categ_book
        dict_infos_livre["title"] = extract_title
        dict_infos_livre["product_description"] = extract_product_desc
        dict_infos_livre["review_rating"] = rating[extract_star_rating]
        dict_infos_livre["image_url"] = extract_img_url
        for th, td in zip(extrac_th, extrac_td):
            if th.text == "UPC" or th.text == "Price (excl. tax)" or th.text == "Price (incl. tax)" or th.text == "Availability":
                dict_infos_livre[th.text] = td.text
        dict_infos_livre["Price (excl. tax)"] = dict_infos_livre["Price (excl. tax)"][1:]
        dict_infos_livre["Price (incl. tax)"] = dict_infos_livre["Price (incl. tax)"][1:]
        dict_infos_livre["Availability"] = dict_infos_livre["Availability"].split()[2][1:]
        return dict_infos_livre
    else:
        print("Connexion echouée")

def list_dict_infos_livre(url_categ):
    """Prend en parametre l'url d'une catégorie et renvoie les informations relatives à chaque livre de cette catégorie
    sous forme d'une liste de dictionnaire. Un dictionnaire contient les informations d'un livre """
    list_livre = list_url_livre(url_categ)
    list_dict_infos_livre = list()
    for url_livre in list_livre:
        list_dict_infos_livre.append(infos_livre(url_livre))
    return list_dict_infos_livre

def charger_images(url_img, nom_fichier):
    """prend en parametre l'url de l'image du livre, un nom de fichier et charge l'image du livre dans le nom de fichier"""
    with open(nom_fichier, 'wb') as fichier_image:
        reponse = requests.get(url_img)
        fichier_image.write(reponse.content)

def creer_csv_par_categ(list_dict):
    """Prend en paramètre la liste des informations de tous les livres d'une catégorie, crée un fichier csv
    portant le nom de la catégorie. Ce fichier aura pour en-tete le titre des informations produit des livres.
     Elle charge aussi les images des livres de cette catégorie dans un dossier"""
    nom_fichier_categ = nom_rep_csv+"/"+list_dict[0]["category"]+".csv"
    with open(nom_fichier_categ, "w", encoding='utf-8') as fichier:
        fielnames = ['product_page_url','UPC', 'title', 'Price (incl. tax)', 'Price (excl. tax)', 'Availability', 'product_description', 'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(fichier, fieldnames=fielnames)
        writer.writeheader()
        for dict in list_dict:
            writer.writerow(dict)
            charger_images(dict["image_url"],nom_rep_image+"/"+dict["category"]+"/"+dict["UPC"]+".jpg")

def generer_fichier(url_site):
    """Prend en paramètre l'url du site. Cree les répertoires pour contenir les fichiers csv et les fichiers images.
     Appelle les fonctions pour la creation des fichiers csv et images
    chargement des images """
    list_dict_categ = list_url_categ(url_site)
    os.mkdir(nom_rep_csv)
    os.mkdir(nom_rep_image)
    for dict_categ in list_dict_categ:
        print("Categorie : ",list(dict_categ.keys())[0]," => Démarré")
        os.mkdir(nom_rep_image+"/"+list(dict_categ.keys())[0])
        creer_csv_par_categ(list_dict_infos_livre(list(dict_categ.values())[0]))
        print("Categorie : ", list(dict_categ.keys())[0], " => Enregistrement effectué avec succes\n")

