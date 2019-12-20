from bs4 import BeautifulSoup
import requests

def getCont():
    url = "http://www.critifence.com/default-password-database/"
    resp = requests.get(url)
    with open("C:/Users/lovebear96/Desktop/scada.html", "w", encoding="utf8") as f:
        f.write(resp.text)

def parse():
    with open("C:/Users/lovebear96/Desktop/scada.html", "r", encoding="utf8") as f:
        cont = f.read()
    f = open("C:/Users/lovebear96/Desktop/table.md", "w", encoding="utf8")
    sp = BeautifulSoup(cont, "lxml")
    lines = sp.find_all("tr")
    titles = lines[0].find_all("th")
    tmp = map(lambda x: x.text, titles)
    f.write(" | ".join(tmp)+"\n")
    f.write("- |"+" - |"*(len(titles)-1)+"\n")
    for line in lines[1:]:
        items = line.find_all("td")
        tmp = map(lambda x: x.text, items)
        f.write(" | ".join(tmp)+"\n")

    f.close()

if __name__ == "__main__":
    parse()