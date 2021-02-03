from imdb import IMDb
from collections import OrderedDict
from pprint import pprint

API = IMDb()

def analyze_series(series_id):
    series = API.get_movie(series_id)
    API.update(series, "episodes")
    data = {
        "title": series.data["title"],
        "years": series.data["series years"],
        "rating": series.data["rating"],
        "average_season_rating": 0,
        "average_episode_rating": 0,
        "plot": series.data["plot outline"],
        "kind": series.data["kind"],
        "complete": True,
        "seasons": OrderedDict(),
        "episodes": OrderedDict(),
    }
    if data["years"].endswith("-"):
        data["complete"] = False
    for season_num, season in series["episodes"].items():
        if season_num <= 0:
            continue
        analysis = analyze_season(season, data)
        if analysis:
            data["seasons"][season_num] = analysis
            data["average_season_rating"] += data["seasons"][season_num]["average_rating"]
    data["average_season_rating"] /= len(data["seasons"].keys())
    data["average_episode_rating"] /= len(data["episodes"].keys())
    return data

def analyze_season(season, series_data):
    average_rating = 0
    num_eps = 0
    data = {
        "high_ep": 0,
        "high_ep_rating": 0,
        "low_ep": 0,
        "low_ep_rating": 10,
        "average_rating": 0,
    }
    for episode_num, episode in season.items():
        ep_key = str(episode["season"]) + "-" + str(episode_num)
        rating = episode.get("rating")
        if rating is None:
            break
        average_rating += rating
        series_data["average_episode_rating"] += rating
        num_eps += 1
        if rating >= data["high_ep_rating"]:
            data["high_ep"] = episode_num
            data["high_ep_rating"] = rating
        if rating <= data["low_ep_rating"]:
            data["low_ep"] = episode_num
            data["low_ep_rating"] = rating
        series_data["episodes"][ep_key] = {
            "rating": rating,
            "title": episode["episode title"],
            "plot": episode["plot"]
        }
    if num_eps == 0:
        return None
    data["average_rating"] = average_rating / num_eps
    return data

def expand_analysis(data):
    if data["complete"]:
        data[""]


# pprint(analyze_series("3398228"))
# pprint(analyze_series("0303461"))
pprint(analyze_series("0903747"))
