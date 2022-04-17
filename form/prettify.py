from bs4 import BeautifulSoup
fin = open("form.html", "r")
soup = BeautifulSoup(fin, 'html.parser')
fin.close()
fout = open("form.html", "w", encoding='utf-8')
fout.write(soup.prettify())
fout.close()
