import json
from mongo_conn import get_client

# takes roster settings and goes through each team's roster and based on current
# performance, creates the optimal lineup and bench.
def find_optimal_lineups(roster_settings):
	league = {}

	# Iterate through the settings one position at a time
	for pos in roster_settings.keys():
		pass
	pass

def main():
	client = get_client()
	thesis_db = client.fbaseball_thesis
	leagues_collection = thesis_db.teams

	roster_settings = json(open("../data/roster_settings.json"))
	optimal_lineups = find_optimal_lineups(roster_settings)

	pass

if __name__ == "__main__":
	main()