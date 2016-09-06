import urllib2, urllib
import re
import BeautifulSoup
import json
import threading
import requests

class seriesFinder:
    def __init__(self):
        self.url = ""
        self.serieList = self.find_all_seires()
        self.omdbUrlListe = self.setOmdbUrlListe()
        self.animatedSeries = []
        self.drama = []
        self.comedy = []


    def find_all_seires(self, url=""):
        list = []
        dict = {}

        if url == "":
            url = "https://bs.to/andere-serien"

        bst = urllib2.urlopen(url)
        bs = BeautifulSoup.BeautifulSoup(bst)

        for tag in bs.findAll('a', href=True):
                list.append(str(tag['href']))

        for serie in list:
            dict["+".join("".join(serie.split("serie/")).split("-")).lower()] = "https://bs.to/" + serie

        return dict

    def setOmdbUrlListe(self):
            liste = []

            for key, value in self.serieList.iteritems():
                liste.append('http://www.omdbapi.com/?t=' + key + '&y=&plot=short&r=json')

            return liste

    def getAnimatedSeries(self):

        for i in range(len(self.omdbUrlListe)-1):
            threading.Thread(self.getAninmated(self.omdbUrlListe[i]))
            print "Thread Nr." + str(i) + " gestartet"



    def getAninmated(self, url):
        response = urllib.urlopen(url)
        response = response.read().decode('utf-8')
        data = json.loads(response)
        try:
            if "Comedy" in data['Genre'] and "Animation" not in data['Genre'] and 'N/A' not in data['imdbRating']:
                if "USA" in data['Country'] and float(data['imdbRating']) >= 7.0:
                    self.comedy.append([data["Title"],self.get_poster(data["Title"],data['Poster'])])

            if "Drama" in data['Genre'] and "Animation" not in data['Genre'] and "Comedy" not in data['Genre'] and 'N/A' \
                    not in data['imdbRating']:
                if "USA" in data['Country'] and float(data['imdbRating']) >= 7.0:
                    self.drama.append([data["Title"],self.get_poster(data["Title"],data['Poster'])])

        except KeyError:
            pass

    def get_poster(self,Title,imgLocation):
        filename = "_".join(Title.split(" ")) + ".jpg"

        try:
            urllib.urlretrieve(imgLocation, '/Users/chris.als/Desktop/ProjectTV/app/static/images/' + filename)
        except IOError:
            pass

        result = 'http://127.0.0.1:5000/static/images/'+filename

        return result

    def writeTextfiles(self,Title ,liste):
        list = liste

        f = open('/Users/chris.als/Desktop/ProjectTV/app/static/images/textFiles/' + Title+'.txt', 'wb')
        f.write(list)
        f.close()

        f = open('/Users/chris.als/Desktop/ProjectTV/app/static/images/textFiles/' + Title+'.txt', 'r')
        return f.read()






    def get_all_episodes(self,season_url):
        liste = []
        season_html = BeautifulSoup.BeautifulSoup(urllib2.urlopen(season_url).read())
        all_links = season_html.findAll('a', title='Streamcloud')

        for link in all_links:
            liste.append("".join(re.search('serie(.+?)Streamcloud-*"', str(link)).group().split('"')))

        return liste

    def CountSeason(self,url):
        bsto = urllib2.urlopen(url).read()
        bs = BeautifulSoup.BeautifulSoup(bsto)

        seas = bs.find("ul", {"class": "pages"})
        children = seas.findAll("a")

        Liste = []
        for i in children:
            if '<a href="serie' in str(i):
                Liste.append(i)

        self.numberofSeason = len(Liste)

    def get_series(self):
        self.find_all_seires()
        return self.serieList





