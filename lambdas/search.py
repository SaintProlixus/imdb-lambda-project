from imdb import IMDb

API = IMDb()

def get_search_results(title):
    results = API.search_movie(title)
    data = {}
    for result in results:
        if "series" in result.data["kind"]:
            data[result.movieID] = result["title"], result["year"], result["kind"]
    return data
