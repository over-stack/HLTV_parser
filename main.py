import requests
from bs4 import BeautifulSoup


class Match:
    def __init__(self, team1, score1, team2, score2, map):
        self.team1 = team1
        self.score1 = score1
        self.team2 = team2
        self.score2 = score2
        self.map = map


startDate = "2020-05-01"
endDate = "2020-06-20"

teams = dict.fromkeys(["AVANT", "Paradox"], "none") #, "Legacy", "CLG", "Tempo Storm", "eXtatus", "Crowns", "Kings"

file = open("tests.txt", "w")

maps = {"Inferno":"inf", "Overpass":"ovp", "Cobblestone":"cbl", "Cache":"cch", "Train":"trn", "Mirage":"mrg", "Dust2":"d2", "Nuke":"nuke"}

search_url = "https://www.hltv.org/search?"

for team in teams:
    search_params = {
        "query":team
    }
    search_response = requests.get(url=search_url, params=search_params)
    search_html_doc = search_response.text.encode("utf-8")
    search_soup = BeautifulSoup(search_html_doc, "html.parser")

    search_tables = search_soup.findAll("table", {"class": "table"})
    for search_table in search_tables:
        search_header = search_table.find("td", {"class": "table-header"})
        if search_header.text == "Team":
            try:
                team_id = search_table.find("a").get("href").split("/")[2]
                teams[team] = team_id
            except:
                pass
            break

results = []
results_url = "https://www.hltv.org/results?"
results_params = {
    "team":teams.values(),
    "startDate":startDate,
    "endDate":endDate
}
results_response = requests.get(url=results_url, params=results_params)
results_html_doc = results_response.text.encode("utf-8")
results_soup = BeautifulSoup(results_html_doc, "html.parser")
#print(results_soup)
results_tables = results_soup.findAll("div", {"class":"results-sublist"})
for result_table in results_tables:
    match_tables = result_table.findAll("div", {"class":"result-con"})
    #print(match_tables)
    for match_table in match_tables:
        team_names = match_table.findAll("td", {"class":"team-cell"})
        if (team_names[0].text.strip() in teams.keys()) and (team_names[1].text.strip() in teams.keys()): #strip #and (team_names[1].text.strip() in teams.keys())
            team_scores = match_table.find("td", {"class":"result-score"}).findAll("span", {})
            map = match_table.find("div", {"class": "map-text"}).text
            if int(team_scores[0].text)+int(team_scores[1].text) > 5:
                results.append(Match(team_names[0].text.strip(), int(team_scores[0].text),
                                     team_names[1].text.strip(), int(team_scores[1].text), map))
            elif map != "-":
                match_ref = match_table.find("a", {}).get("href")
                match_url = "https://www.hltv.org"+match_ref
                match_response = requests.get(url=match_url)
                match_html_doc = match_response.text.encode("utf-8")
                match_soup = BeautifulSoup(match_html_doc, "html.parser")
                match_games = match_soup.findAll("div", {"class":"mapholder"})
                for match_game in match_games:
                    team_names = match_game.findAll("div", {"class":"results-teamname text-ellipsis"})
                    team_scores = match_game.findAll("div", {"class":"results-team-score"})
                    map = match_game.find("div", {"class":"mapname"}).text
                    try:
                        results.append(Match(team_names[0].text.strip(), int(team_scores[0].text),
                                             team_names[1].text.strip(), int(team_scores[1].text), maps[map]))
                    except:
                        pass

results.reverse()
for result in results:
    print(result.team1, result.score1, result.team2, result.score2, result.map)
    file.write(result.team1+" "+str(result.score1)+" "+result.team2+" "+str(result.score2)+" "+result.map+"\n")