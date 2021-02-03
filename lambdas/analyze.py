from imdb import IMDb
from statistics import mean, stdev, variance
from pprint import pprint

API = IMDb()
QUALITY = [
    (9, "exceptional"),
    (8.5, "excellent"),
    (8, "great"),
    (7.5, "good"),
    (7, "above average"),
    (6.5, "below average"),
    (6, "not good"),
    (5, "bad"),
    (4, "terrible"),
    (3, "horrendous"),
    (0, "the worst")
]
CONSISTENCY = [
    (0.05, "unreal"),
    (0.07, "fantastic"),
    (0.1, "very high"),
    (0.2, "high"),
    (0.4, "moderate"),
    (0.6, "low"),
    (0.8, "very low"),
    (1.0, "extremely low"),
    (1000, "all over the place")
]

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
        self.avg_sn_rating = mean(self.sn_ratings) if len(self.sn_ratings) > 0 else 0
        self.avg_ep_rating = mean(self.ep_ratings) if len(self.ep_ratings) > 0 else 0
        self.sn_stdev = stdev(self.sn_ratings) if len(self.sn_ratings) > 1 else 0
        self.ep_stdev = stdev(self.ep_ratings) if len(self.ep_ratings) > 1 else 0
        self.sn_var = variance(self.sn_ratings) if len(self.sn_ratings) > 1 else 0
        self.ep_var = variance(self.ep_ratings) if len(self.ep_ratings) > 1 else 0
    
    def __str__(self):
        return f"Title: {self.title}\n\
            Years: {self.years}\n\
            Rating: {self.rating}\n\
            Plot: {self.plot}\n\
            Kind: {self.kind}\n\
            Complete: {self.complete}\n\
            Avg. Season Rating: {self.avg_sn_rating}\n\
            Avg. Episode Rating: {self.avg_ep_rating}\n\
            Season Std. Dev: {self.sn_stdev}\n\
            Episode Std. Dev: {self.ep_stdev}\n\
            Season Variance: {self.sn_var}\n\
            Episode Variance: {self.ep_var}\n\
            Best Episode: {self.high_ep}\n\
            Worst Episde: {self.low_ep}\n\
            Latest: {self.get_finale()}\n"
    
    def __repr__(self):
        return self.__str__()
    
    def populate_seasons(self):
        for season_num, season in self.series["episodes"].items():
            if season_num > 0:
                season_obj = Season(self, season_num, season)
                if len(season_obj.episodes) > 0:
                    self.seasons[season_num] = season_obj

    def get_finale(self):
        final_season = self.seasons[max(self.seasons.keys())]
        return final_season.episodes[max(final_season.episodes.keys())]
        

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
        self.avg_ep_rating = mean(self.ratings) if len(self.ratings) > 0 else 0
        # print(self.avg_ep_rating)
        self.stdev = stdev(self.ratings) if len(self.ratings) > 1 else 0
        if len(self.episodes) > 0:
            self.series.sn_ratings.append(self.avg_ep_rating)
    
    def __str__(self):
        return f"Best Episode: {self.high_ep}\n\
            Worst Episode: {self.low_ep}\n\
            Avg. Episode Rating: {self.avg_ep_rating}\n\
            Std. Dev: {self.stdev}\n\
            Episodes: {self.episodes}\n"

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
        print(self.rating)
        self.title = episode["episode title"]
        self.plot = episode["plot"]
        self.season.ratings.append(self.rating)
        self.season.series.ep_ratings.append(self.rating)
        self.eval_rating()
    
    def __str__(self):
        return f"Title: {self.title}\n\
            Episode: {self.season.season_num}-{self.episode_num}\n\
            Rating: {self.rating}\n\
            Plot: {self.plot}\n"

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


# pprint(Series("3398228")) # BoJack Horseman
# pprint(Series("0303461")) # Firefly
# pprint(Series("0903747")) # Breaking Bad
# pprint(Series("0413573")) # Grey's Anatomy
pprint(Series("0944947")) # GoT
# pprint(Series("0813715")) # Heroes
# pprint(Series("0455275")) # Prison Break
# pprint(Series("1489428")) # Justified
# pprint(Series("0436992")) # Doctor Who
# pprint(Series("0773262")) # Dexter
# pprint(Series("0411008")) # Lost
# pprint(Series("2356777")) # True Detective
# pprint(Series("0934814")) # Chuck
# pprint(Series("0239195")) # Survivor

