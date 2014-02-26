import json
from mongo_conn import get_client

def find_optimal_lineups(roster_settings, teams):
	""" Takes roster settings and goes through each team's roster and based on
	current performance, creates the optimal lineup and bench.

	"""
	league = {}

	for team in teams:
		optimal_team = {}
		# Set optimal lineup to empty based on roster settings
		for pos in roster_settings.keys():
			optimal_team[pos] = None
		
		# Go through each player and determine if worthy to be in opt lineup
		for player in team:
			# TODO
			# 
			# 
		
	pass

def main():
	client = get_client()
	thesis_db = client.fbaseball_thesis
	league_collection = thesis_db.teams

	roster_settings = json.load(open("../data/roster_settings.json"))
	optimal_lineups = find_optimal_lineups(roster_settings, league_collection["teams"])

	pass

if __name__ == "__main__":
	main()