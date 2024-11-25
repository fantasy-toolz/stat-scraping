# stat-scraping
## v2.0

Scraping capabilities for several major MLB and Fantasy MLB sources, consolidated under one interface.

## Fangraphs

As an example scraper,

```python
from src import statscraping as ss

HittingDF = ss.get_fangraphs_data('hitting',['2024'])
PitchingDF = ss.get_fangraphs_data('pitching',['2024'])
```

## FantasyPros

As an example scraper,

```python
from src import statscraping as ss

HittingDF = ss.get_fantasypros_projections(playertype,preseason=True)
```