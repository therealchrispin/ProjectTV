from seriesFinder import seriesFinder
class Serie:
    def __init__(self, name=""):
        self.finder = seriesFinder()
        self.root = "https://bs.to/"
        self.name = name
        self.staffel = None
        self.episode = []
        self.serien = self.all_series_name()
        self.url = ""

    def all_series_name(self):
        return self.finder.serieList

    def set_name(self, serie):
        serie = serie
        i = 0
        while i < len(self.serien) - 1:
            if serie.lower() in self.serien[i].lower():
                serie = self.serien[i]
                break
            i += 1
        self.name = serie

    def get_episodes(self):
        if self.name != "":
            self.get_serie_url()
            self.episode = self.finder.find_episodes(self.url)
            for i in range(len(self.episode)-1):
                self.episode[i] = self.root + self.episode[i]

            return self.episode

    def get_serie_url(self):
        if self.staffel is not None:
            self.url = self.root + self.name + str(self.staffel)
        else:
            self.url = self.root + self.name
