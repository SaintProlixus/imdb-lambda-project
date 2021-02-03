from imdb import IMDb
from statistics import mean, stdev
from pprint import pprint

API = IMDb()

class Series:
    def __init__(self, series_id):
        self.series = API.get_movie(series_id)
        API.update(self.series, "episodes")
        self.title = self.series.data["title"]
        self.years = self.series.data["series years"]
        self.rating = self.series.data["rating"]
        self.plot = self.series.data["plot outline"]
        self.kind = self.series.data["kind"]
        self.high_ep = None
        self.low_ep = None
        self.complete = True
        if self.years.endswith("-"):
            self.complete = False
        self.seasons = {}
        self.sn_ratings = []
        self.ep_ratings = []
        self.populate_seasons()
        self.avg_sn_rating = mean(self.sn_ratings)
        self.avg_ep_rating = mean(self.ep_ratings)
        self.sn_stdev = stdev(self.sn_ratings) if len(self.sn_ratings) > 1 else 0
        self.ep_stdev = stdev(self.ep_ratings)
    
    def __str__(self):
        return f"Title: {self.title}\n\
            Years: {self.years}\n\
            Rating: {self.rating}\n\
            Plot: {self.plot}\n\
            Kind: {self.kind}\n\
            Complete: {self.complete}\n\
            Best Episode: {self.high_ep}\n\
            Worst Episde: {self.low_ep}\n\
            Avg. Season Rating: {self.avg_sn_rating}\n\
            Avg. Episode Rating: {self.avg_ep_rating}\n\
            Season Std. Dev: {self.sn_stdev}\n\
            Episode Std. Dev: {self.ep_stdev}\n\
            Seasons: {self.seasons}"
    
    def __repr__(self):
        return self.__str__()
    
    def populate_seasons(self):
        for season_num, season in self.series["episodes"].items():
            self.seasons[season_num] = Season(self, season_num, season)
        

class Season:
    def __init__(self, series, season_num, season):
        self.series = series
        self.season_num = season_num
        self.season = season
        self.ratings = []
        self.high_ep = None
        self.low_ep = None
        self.avg_ep_rating = 0
        self.stdev = 0
        self.episodes = {}
        self.populate_episodes()
        self.avg_ep_rating = mean(self.ratings)
        self.stdev = stdev(self.ratings) if len(self.ratings) > 1 else 0
        self.series.sn_ratings.append(self.avg_ep_rating)
    
    def __str__(self):
        return f"Best Episode: {self.high_ep}\n\
            Worst Episode: {self.low_ep}\n\
            Avg. Episode Rating: {self.avg_ep_rating}\n\
            Std. Dev: {self.stdev}\n\
            Episodes: {self.episodes}"

    def __repr__(self):
        return self.__str__()
    
    def populate_episodes(self):
        for episode_num, episode in self.season.items():
            if episode.get("rating"):
                self.episodes[episode_num] = Episode(self, episode_num, episode)


class Episode:
    def __init__(self, season, episode_num, episode):
        self.season = season
        self.episode_num = episode_num
        self.episode = episode
        self.rating = episode["rating"]
        self.title = episode["episode title"]
        self.plot = episode["plot"]
        self.season.ratings.append(self.rating)
        self.season.series.ep_ratings.append(self.rating)
        self.eval_rating()
    
    def __str__(self):
        return f"Title: {self.title}\n\
            Rating: {self.rating}\n\
            Plot: {self.plot}"

    def __repr__(self):
        return self.__str__()
    
    def eval_rating(self):
        if self.season.high_ep:
            if self.rating >= self.season.high_ep.rating:
                self.season.high_ep = self
        else:
            self.season.high_ep = self
        if self.season.low_ep:
            if self.rating <= self.season.low_ep.rating:
                self.season.low_ep = self
        else:
            self.season.low_ep = self
        if self.season.series.high_ep:
            if self.rating >= self.season.series.high_ep.rating:
                self.season.series.high_ep = self
        else:
            self.season.series.high_ep = self
        if self.season.series.low_ep:
            if self.rating <= self.season.series.low_ep.rating:
                self.season.series.low_ep = self
        else:
            self.season.series.low_ep = self


# pprint(analyze_series("3398228"))
# pprint(analyze_series("0303461"))
# pprint(analyze_series("0903747"))

print(Series("0303461"))
