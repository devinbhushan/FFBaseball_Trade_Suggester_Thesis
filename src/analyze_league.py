import json, sys
from mongo_conn import get_client
from munkres import Munkres

def _create_graph(team, team_graph_dict):
	"""
	Takes a team and team_graph_dict outline and returns a completed graph
	ready to input into Munkres.
	"""
	# Create graph of players from each team
	for player in team:
		for pos in player["POS"]:
			if pos == 'P':
				continue
				#TODO Why doesn't this catch the P?
			team_graph_dict[pos].append(player["points"])

	return team_graph_dict

def _create_cost_graph(profit_graph):
	"""
	Converts a profit graph to a cost graph. AKA converts minimize values
	to be compatible with maximized values
	"""
	cost_matrix = []
	for row in profit_graph:
	    cost_row = []
	    for col in row:
	        cost_row += [sys.maxsize - col]
	    cost_matrix += [cost_row]

	return cost_matrix

def find_optimal_lineups(roster_settings, league):
	""" 
	Takes roster settings and goes through each team's roster and based on
	current performance, creates the optimal lineup and bench.

	"""

	while league.alive:
		curr_league = league.next()
		optimal_league = {}
		
		#Go through each team and find it's optimal lineup using _create_graph
		for i, team in enumerate(curr_league["teams"]):
			optimal_league[i] = {}
			optimal_team = {}
			team_graph_dict = {}

			# Set optimal lineup to empty based on roster settings
			for pos in roster_settings.keys():
				if pos == 'P':
					continue
				optimal_team[pos] = None
				team_graph_dict[pos] = []

			# Get profit_matrix in form of dictionary mapped to positions
			team_graph_dict = _create_graph(team, team_graph_dict)

			# Convert team_graph to profit_matrix
			profit_matrix = None

			# Convert profit_matrix to cost_matrix
			cost_matrix = _create_cost_graph(profit_matrix)

			# Call munkres graph solve on cost_matrix
			m = Munkres()
			indexes = m.compute(cost_matrix)


	return None

def main():
	client = get_client()
	thesis_db = client.fbaseball_thesis
	league_collection = thesis_db.teams

	roster_settings = json.load(open("../data/roster_settings.json"))
	optimal_lineups = find_optimal_lineups(roster_settings, league_collection.find({}))

if __name__ == "__main__":
	main()