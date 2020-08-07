A football results simulation engine, which has potential to evolve into a game.

# tournament_simulator
This is a 16-team tournament simulation, which:
* defines starting teams and their strengths
* sorts those teams randomly into 4 groups of 4 teams
* creates a league table for each group
* creates a home/away set of fixtures between every team in a group
* simulates the outcome of each match, taking into account:
  * home advantage
  * strength of each team
  * recent form (last 5 games)
  * previous result
  * random factor
* updates the league table and team stats after each result, sorting teams by:
  * points
  * then goal difference
  * then team strength (weakest first)
  * then alphabetically
* carries the top 2 teams from each group through to a knock-out format
* simulates the outcome of knockout games, adding penalty shootout logic:
  * 5 penalties each, then sudden death
  * penalty conversion is based on random chance
* declares a final winner
* calculates tournament performance for each team using a coefficient system:
  * teams awarded points for positive results, as well as goals
  * more weighting given to higher profile fixtures
* awards prize money to teams based on tournament performance
* updates the strength of each team based on available money in the bank
  * teams retain a buffer to help them cope with bad seasons
  * any money available above and beyond the buffer can be used to strengthen the team
  * negative bank balances result in teams having to sell players
* loops through multiple seasons of the tournament
* provides a list of historical tournament winners and match stats

To-do:
* improve result simulator with additional logic (e.g. factor in current league position of each team)
* improve table sorting logic (add more sort criteria following actual European league rules)
* improve coefficient calculation with additional logic (e.g. Elo-style scoring system)
* tidy up code

Long-term:
* turn into an interactive game, accepting user inputs and decisions
