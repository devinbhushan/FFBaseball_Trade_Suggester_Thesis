import csv
from mongo_conn import get_client

client = get_client()
thesis_db = client.fbaseball_thesis
players_collection = thesis_db.players
pitchers_collection = thesis_db.pitchers

players_collection.remove()
pitchers_collection.remove()

stats_legend = None
files = ["2010_mlb_pitchers.csv", "2010_mlb_batters.csv"]
for curr in files:
	with open('../data/%s' % curr) as f:
		reader = csv.reader(f, delimiter=",")
		for i, row in enumerate(reader):
			if i is 0:
			 	# Ignore "PLAYER" field because we're splitting that up into first
			 	# and last names
			 	stats_legend = row[1:]
			else:
				new_player = {}
				try:
					last_name, first_name = [name.strip() for name in row[0].split(",")]
				except ValueError:
					break
				new_player["last_name"] = last_name
				new_player["first_name"] = first_name
				for i, field in enumerate(row[1:]):
					new_player[stats_legend[i]] = field

				# Add point field for later processing
				new_player["points"] = 0
				if "pitcher" in curr:
					pitchers_collection.insert(new_player)
				else:
					players_collection.insert(new_player)
