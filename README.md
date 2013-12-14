## UIUC Undergrad Senior Thesis: Fantasy Baseball Trade Suggester
###Setup:
1. Run excel_to_mongo.py to get data into MongoDB datacase
2. Run score_league.py to assign points to all players based on scoring_settings.json
3. Run init_league to read teams.json into database
4. Run analyze_league.py to figure out starting lineups and identify excess positions and need positions