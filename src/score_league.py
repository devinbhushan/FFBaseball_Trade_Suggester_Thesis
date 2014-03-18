import json
from mongo_conn import get_client

# This script will look at scoring settings and accordingly input point values
# for every player, based on their stats, into the database

def score_player_set(players_collection, scoring):
	for player in players_collection.find():
		# get items back in pairs (ex: (first_name, Todd))
		plarfcdyer["points"] = 0
		for key, value in zip(player.keys(), player.values()):
			if key in scoring.keys():
				player["points"] += (float(value) * float(scoring[key]))
		players_collection.save(player)

def main():
	scoring_settings = json.load(open("../data/scoring_settings.json"))
	hitter_scoring = scoring_settings["hitters"]
	pitcher_scoring = scoring_settings["pitchers"]

	client = get_client()
	thesis_db = client.fbaseball_thesis
	players_collection = thesis_db.players
	pitchers_collection = thesis_db.pitchers

	score_player_set(players_collection, hitter_scoring)
	score_player_set(pitchers_collection, pitcher_scoring)

if __name__ == "__main__":
	main()