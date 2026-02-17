"""
batcast.py

MSP 19 May 2024 First version.

"""

import pandas as pd
from datetime import datetime, timedelta

class Batcast:
    """
    A class to fetch and improve baseball statistics from Baseball Savant.

    Methods
    -------
    get_season_stats()
        Returns the statistics from the current season.

    get_daily_stats(date_string)
        Returns the statistics for a specific date.

    Example usage
    -------------
    import batcast as bc

    batcast = bc.Batcast()

    # Get season stats
    season_stats = batcast.get_season_stats()
    print(season_stats.head())

    # Get daily stats for a specific date
    daily_stats = batcast.get_daily_stats('2024-05-18')
    print(daily_stats.head())

    # get all stats by day for this season
    season_daily_stats = batcast.get_season_daily_stats()
    print(season_daily_stats.head())

    # see all Kyle Schwarber's games:
    kyleschwarber = season_daily_stats.loc[season_daily_stats['name']=="Schwarber, Kyle"]

    # who had the most swings in a game?
    season_daily_stats.loc[season_daily_stats['swings'].idxmax()]

    # most whiffs?
    season_daily_stats.loc[season_daily_stats['whiffs'].astype('int').idxmax()]

    """

    def __init__(self):
        """
        Initializes the Batcast class with a custom user agent to bypass basic firewalls.
        """
        self.storage_options = {'User-Agent': 'Mozilla/5.0'}

    def _improve_df(self, df):
        """
        Adds some commonly used values to the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the original statistics.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with added 'swings' column.
        """
        df['swings'] = (df['swings_competitive'] / df['percent_swings_competitive']).astype('int')
        return df

    def get_season_stats(self):
        """
        Fetches and returns the statistics from the current season.

        Returns
        -------
        pandas.DataFrame
            The DataFrame containing the current season statistics. Columns are
            ['id', 'name', 'swings_competitive', 'percent_swings_competitive',
            'contact', 'avg_bat_speed', 'hard_swing_rate',
            'squared_up_per_bat_contact', 'squared_up_per_swing',
            'blast_per_bat_contact', 'blast_per_swing', 'swing_length', 'swords',
            'batter_run_value', 'whiffs', 'whiff_per_swing', 'batted_ball_events',
            'batted_ball_event_per_swing']
        """
        now = datetime.now()
        year = now.strftime("%Y")
        baseurl = (
            "https://baseballsavant.mlb.com/leaderboard/bat-tracking?"
            "attackZone=&batSide=&contactType=&count=&dateStart={0}&dateEnd={1}"
            "&gameType=&groupBy=&isHardHit=&minSwings=q&minGroupSwings=1"
            "&pitchHand=&pitchType=&seasonStart=&seasonEnd=&team=&type=batter"
            "&sortColumn=swords&sortDirection=desc&csv=true"
        ).format(f"{year}-01-01", now.strftime("%Y-%m-%d"))

        return self._improve_df(pd.read_csv(baseurl, storage_options=self.storage_options))
    
    def get_season_daily_stats(self):
        """
        Retrieves batting statistics for each day of the current season.

        Returns
        -------
        pandas.DataFrame
            The DataFrame containing daily batting statistics for the current season.
        """
        # Define the opening day of the season
        opening_day = datetime.strptime("2024-03-27", "%Y-%m-%d")
        
        # Initialize the DataFrame with stats from the opening day
        alldf = self.get_daily_stats(opening_day.strftime("%Y-%m-%d"))
        alldf['date'] = opening_day.strftime("%Y-%m-%d")
        current_day = opening_day + timedelta(days=1)

        # Loop through each day until the current date
        while current_day.strftime("%Y-%m-%d") != datetime.now().strftime("%Y-%m-%d"):
            df = self.get_daily_stats(current_day.strftime("%Y-%m-%d"))
            df['date'] = current_day.strftime("%Y-%m-%d")
            current_day += timedelta(days=1)
            alldf = pd.concat([alldf, df], ignore_index=True)

        return alldf
    
    def get_daily_stats(self, date_string):
        """
        Fetches and returns the statistics for a specific date.

        Parameters
        ----------
        date_string : str
            The date in 'YYYY-MM-DD' format for which the statistics are required.

        Returns
        -------
        pandas.DataFrame
            The DataFrame containing the statistics for the specified date. Columns are
            ['id', 'name', 'swings_competitive', 'percent_swings_competitive',
            'contact', 'avg_bat_speed', 'hard_swing_rate',
            'squared_up_per_bat_contact', 'squared_up_per_swing',
            'blast_per_bat_contact', 'blast_per_swing', 'swing_length', 'swords',
            'batter_run_value', 'whiffs', 'whiff_per_swing', 'batted_ball_events',
            'batted_ball_event_per_swing']
        """
        try:
            date_object = datetime.strptime(date_string, "%Y-%m-%d")
            print("Date Object:", date_object)
        except ValueError as e:
            print("Error:", e)
            return pd.DataFrame()  # Return an empty DataFrame in case of an error

        date_object_plus_one = date_object + timedelta(days=1)
        baseurl = (
            "https://baseballsavant.mlb.com/leaderboard/bat-tracking?"
            "attackZone=&batSide=&contactType=&count=&dateStart={0}&dateEnd={1}"
            "&gameType=&groupBy=&isHardHit=&minSwings=q&minGroupSwings=1"
            "&pitchHand=&pitchType=&seasonStart=&seasonEnd=&team=&type=batter"
            "&sortColumn=swords&sortDirection=desc&csv=true"
        ).format(date_object.strftime("%Y-%m-%d"), date_object_plus_one.strftime("%Y-%m-%d"))

        return self._improve_df(pd.read_csv(baseurl, storage_options=self.storage_options))
