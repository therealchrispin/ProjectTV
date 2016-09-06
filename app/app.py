from flask import Flask, render_template, request, jsonify
import re
import urllib
import urllib2
import BeautifulSoup
import time
from seriesFinder import seriesFinder
from Serie import Serie
import requests, json
from difflib import SequenceMatcher

app = Flask(__name__)

serie = Serie()
seriesFinder = seriesFinder()
#seriesFinder.getAnimatedSeries()


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/all-series')
def all_series():
    return str(seriesFinder.serieList)


@app.route('/animated')
def getAnimated():

    datei = open('/Users/chris.als/Desktop/ProjectTV/app/static/images/textFiles/Animation.txt',"r").read()

    liste = []
    i = 2
    while i < len(datei):
        a = datei.find("]",i)
        liste.append(datei[i:a].replace("u'","").replace("',", " -").replace("'","").split(" - "))
        i = a+4


    return jsonify(ergebnis=liste)

@app.route('/comedy')
def getComedy():
    #seriesFinder.writeTextfiles('Comedy',str(seriesFinder.comedy))

    datei = open('/Users/chris.als/Desktop/ProjectTV/app/static/images/textFiles/Comedy.txt',"r").read()

    liste = []
    i = 2
    while i < len(datei):
        a = datei.find("]",i)
        liste.append(datei[i:a].replace("u'","").replace("',", " -").replace("'","").split(" - "))
        i = a+4

    return jsonify(ergebnis=liste)


@app.route('/drama')
def getDrama():
    #seriesFinder.writeTextfiles('Drama',str(seriesFinder.drama))

    datei = open('/Users/chris.als/Desktop/ProjectTV/app/static/images/textFiles/Drama.txt',"r").read()

    liste = []
    i = 2
    while i < len(datei):
        a = datei.find("]",i)
        liste.append(datei[i:a].replace("u'","").replace("',", " -").replace("'","").split(" - "))
        i = a+4

    return jsonify(ergebnis=liste)



@app.route('/get_serie_url')
def get_serie_url():
    print "get_serie started"
    result = ""
    serie = request.args.get('serie', 0, type=str)
    serie = "+".join(serie.split(" "))

    for key,value in seriesFinder.serieList.iteritems():
        if SequenceMatcher(None,serie.lower(),key.lower()).ratio()>0.7:
            result = [key, seriesFinder.serieList[key]]
            break
        else:
            result = "keine serie gefunden"

    return jsonify(ergebnis=result)


@app.route('/get_episodes')
def get_episodes():
    print "get_episodes gestartet"
    url = request.args.get('url', 0, type=str)
    season = request.args.get('season',0 , type=int)

    if season==0 or season is None or season == "":
        season = 1

    episode = request.args.get('episode', 0, type=int)

    if episode == 0 or episode is None or episode == "":
        episode = 1

    html = urllib2.urlopen(url+"/"+str(season)).read()
    soup = BeautifulSoup.BeautifulSoup(html)
    soupLinks = soup.findAll('a',title="Streamcloud")

    pattern = r'serie/(.+?)/' + re.escape(str(season)) + r'/' + re.escape(str(episode)) + r'-(.+?)/Streamcloud.[0-9]'
    episodeUrl = ""
    for tag in soupLinks:
        if re.search(pattern, str(tag)) is not None:
            episodeUrl = "https://bs.to/" + re.search(pattern, str(tag)).group()

    streamcloudUrl = getStreamcloudUrl(episodeUrl)
    episode = streamcloudparser(streamcloudUrl)

    return jsonify(ergebnis=episode)

def getStreamcloudUrl(bstoUrl):
    html = urllib2.urlopen(bstoUrl).read()
    soup = BeautifulSoup.BeautifulSoup(html)
    soupLinks = soup.findAll('a')

    streamcloudUrl = ""
    for tag in soupLinks:
        if re.search('http.+?(.html|.flv|.mp4|.mkv|.avi)',str(tag)) is not None:
            streamcloudUrl = re.search('http.+?(.html|.flv|.mp4|.mkv|.avi)',str(tag)).group()

    return streamcloudUrl

def streamcloudparser(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = response.read()

    form_values = {}
    for i in re.finditer(
            '<input.*?name="(.*?)".*?value="(.*?)">', content):
        form_values[i.group(1)] = i.group(2)

    # wait 11 seconds and update progress bar
    time.sleep(11)

    content = urllib2.urlopen(url=url, data=urllib.urlencode(form_values)).read()

    ri = re.search('file: (.+?),', content)
    r = re.search('http://(.+?)"', ri.group())

    if r is None:
        return "kein Video"
    else:
        return r.group()

@app.route('/get_poster')
def get_poster():
    print " getting Poster"
    poster = request.args.get('Poster', 0, type=str)
    Title = "_".join(request.args.get('Title', 0, type=str).split(" "))
    filename = Title + ".jpg"

    f = open('/Users/chris.als/Desktop/ProjectTV/app/static/images/' + filename, 'wb')
    f.write(requests.get(poster).content)
    f.close()

    result = [" ".join(Title.split("_")), 'http://127.0.0.1:5000/static/images/'+filename]

    return jsonify(ergebnis=result)

def countSeason(url):
    bsto = urllib2.urlopen(url=url).read()
    bs = BeautifulSoup.BeautifulSoup(bsto)

    seas = bs.find("ul", {"class": "pages"})
    children = seas.findAll("a")

    Liste = []
    for i in children:
        if '<a href="serie' in str(i):
            Liste.append(i)

    return len(Liste)

@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == "__main__":
    app.run()
 #app.run(host='192.168.0.12', port="5000")