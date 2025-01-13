# stat-scraping
## v2.0

Scraping capabilities for several major MLB and Fantasy MLB sources, consolidated under one interface.

## FantasyToolz


### Batting Orders
To scrape batting order statistics for a team,

```python
from src import statscraping as ss

year = '2024'
team = 'ATL'

ATL = ss.get_fantasytoolz_lineups(team,year)
AllPlayers = ss.get_fantasytoolz_lineup_summary(year)

date = '2024-08-31'
DateLineups = ss.get_fantasytoolz_date_lineups(date)

TeamLineups = ss.get_fantasytoolz_team_lineup(year,team)

AllLineups = ss.get_fantasytoolz_all_lineups(year)
```

### MLB Predictions

```python
from src import statscraping as ss

date = '2024-08-31'
Matchups = ss.get_fantasytoolz_date_matchups(date)
```

Cross-matching with the matchups:
```python 
from src import statscraping as ss
import pandas as pd

date = '2024-06-25'
Matchups = ss.get_fantasytoolz_date_matchups(date)
DateLineups = ss.get_fantasytoolz_date_lineups(date)

HomeLineups = pd.merge(Matchups,DateLineups,left_on="hometeam",right_on="team")
AwayLineups = pd.merge(Matchups,DateLineups,left_on="awayteam",right_on="team")

```


## Fangraphs

As an example scraper,

```python
from src import statscraping as ss

HittingDF = ss.get_fangraphs_data('hitting',['2024'])
PitchingDF = ss.get_fangraphs_data('pitching',['2024'])
```

Specific dates can also be scraped in a season, e.g. by
```python
HittingDF = ss.get_fangraphs_data('hitting',['2024'],'2024-04-01','2024-05-01')
```

## FantasyPros

As an example scraper,

```python
from src import statscraping as ss

HittingDF = ss.get_fantasypros_projections(playertype,preseason=True)
```