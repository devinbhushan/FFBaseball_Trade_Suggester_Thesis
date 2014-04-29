import json, sys
from pprint import pprint
from mongo_conn import get_client
import munkres
from munkres import Munkres
import math

def _create_graph(team, team_graph_dict):
	"""
	Takes a team and team_graph_dict outline and returns a completed graph
	ready to input into Munkres.
	"""
	pos_list = team_graph_dict.keys()

	# Create graph of players from each team
	for player in team:
		for pos in pos_list:
			if pos in player["POS"]:
				team_graph_dict[pos].append(player)
			else:
				team_graph_dict[pos].append(0)

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
	    	if not col == 0:
	    		col = sys.maxsize - col
	        cost_row += [col]
	    cost_matrix += [cost_row]
	pprint(cost_matrix)
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
			print "NEW TEAM %s \n-------------------------" % i
			# Sort team lexicographically to ensure ordering for calculations
			team = sorted(team, key = lambda k: k["_id"])

			optimal_league[i] = {}
			optimal_team = {}
			team_graph_dict = {}

			# Set optimal lineup to empty based on roster settings
			for pos in sorted(roster_settings.keys()):
				if pos == 'P':
					continue
				optimal_team[pos] = None
				team_graph_dict[pos] = []

			# Get profit_matrix in form of dictionary mapped to positions
			team_graph_dict = _create_graph(team, team_graph_dict)

			# pprint(team_graph_dict)
			# Convert team_graph to profit_matrix
			profit_matrix = []
			for j, pos in enumerate(sorted(team_graph_dict.keys())):
				curr_row = []
				for curr_player in team_graph_dict[pos]:
					if curr_player == 0:
						curr_row.append(0)
					else:
						curr_row.append(int(curr_player["points"]))
				profit_matrix.append(curr_row)
			pprint("profit_matrix: %s" % profit_matrix)

			# Convert profit_matrix to cost_matrix
			cost_matrix = munkres.make_cost_matrix(profit_matrix, lambda cost: sys.maxsize - cost)# _create_cost_graph(profit_matrix)
			pprint("cost_matrix: %s" % cost_matrix)
			# Call munkres graph solve on cost_matrix
			m = Munkres()
			indexes = m.compute(cost_matrix)
			# pprint(indexes)

			for (x,y) in indexes:
				pprint("(%s, %s)" % (y, x))
				pprint("Optimal lineup %s" % profit_matrix[x][y])
			# print team_graph_dict.keys()



	return None

def main():
	client = get_client()
	thesis_db = client.fbaseball_thesis
	league_collection = thesis_db.teams

	roster_settings = json.load(open("../data/roster_settings.json"))
	optimal_lineups = find_optimal_lineups(roster_settings, league_collection.find({}))

if __name__ == "__main__":
	main()