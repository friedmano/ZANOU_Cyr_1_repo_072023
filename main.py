# This is a sample Python script.
import fonctions



# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "http://books.toscrape.com"

    #list_url_categ = fonctions.list_url_categ(url)
    #list_url_livre = fonctions.list_url_livre('http://books.toscrape.com/catalogue/category/books/classics_6/index.html')
    #list_infos_livre = fonctions.infos_livre('http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html')
    #list_dict_infos_livres = fonctions.list_dict_infos_livre('http://books.toscrape.com/catalogue/category/books/classics_6/index.html')
    #fonctions.creer_csv_par_categ(list_dict_infos_livres)
    fonctions.generer_fichier(url)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
