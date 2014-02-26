import json
import sys
from mongo_conn import get_client

# This script will read teams.json into a database.
# Currently only players are needed, so it will go through each
# and look them all up and insert them into the team's document

def main():
	leagues = json.load(open("../data/teams.json"))
	
	client = get_client()
	thesis_db = client.fbaseball_thesis
	players_collection = thesis_db.players
	pitchers_collection = thesis_db.pitchers
	teams_collection = thesis_db.teams

	league = leagues["league"]
	league_name = league["name"]
	teams = league["teams"]
	league_obj = {"name": league_name}
	league_obj["teams"] = []

	for team in teams:
		team_obj = []
		for player in teams[team]["query"]["results"]["team"]["roster"]["players"]["player"]:
			try:
				db_match = players_collection.find({"first_name": player["name"]["ascii_first"], 
					"last_name": player["name"]["ascii_last"]})[0]
			except IndexError:
				try:
					db_match = pitchers_collection.find({"first_name": player["name"]["ascii_first"], 
						"last_name": player["name"]["ascii_last"]})[0]
				except IndexError:
					print "Player in teams.json does not match DB. Player", player["name"]["full"], "Skipping."
					continue
					# sys.exit(0)
			db_match["POS"] = player["eligible_positions"]["position"]

			# Append this player to the team list
			team_obj.append(db_match)
		league_obj["teams"].append(team_obj)
	
	teams_collection.save(league_obj)

if __name__ == "__main__":
	main()