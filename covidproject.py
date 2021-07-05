import pandas as pd
from pandas._libs.tslibs.timedeltas import Timedelta
from pandas._libs.tslibs.timestamps import Timestamp
from loggerconfig import logger
import os


"""
Author: M. Groman

This script downloads covid related data and sends an email every day with the number of new cases. It keeps a csv file with historical data, which are ready for use, should
this new use case emerge. New data is downloaded every day and the csv file is with this data updated.
"""


def get_data(start_date: pd.Timestamp = pd.Timestamp('2020-12-31'), end_date: pd.Timestamp = pd.Timestamp('2021-06-30'), full_load: bool = True) -> pd.DataFrame:
    """Get the data from given start date up to given end date and save it in csv format.

    Args:
        start_date (pd.Timestamp, optional): Date from which the data gets saved into df. Defaults to pd.Timestamp('2021-01-01').
        end_date (pd.Timestamp, optional): Date up to which the data gets saved into df. Defaults to pd.Timestamp('2021-06-30').
        full_load (bool, optional): Whether or not you load the full dataset or just increment. Defaults to True.

    Returns:
        pd.DataFrame: Dataframe which holds downloaded data.
    """
    url = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv'
    df = pd.read_csv(url, parse_dates=['datum'])
    df = df[(df['datum'] > start_date) & (df['datum'] <= end_date)]
    data_path = os.path.join('data','data.csv')
    if full_load:
        df.to_csv(data_path, mode= 'w', index=False)      
    else:
        df.to_csv(data_path, mode= 'a', index=False, header=False)
    logger.info('Loaded the data from {} to {}'.format(start_date, end_date))
    return df


def update_data(df: pd.DataFrame):
    """ Update data up today. Appends missing data from the latest date up to todays date.

    Args:
        df (pd.Dataframe): Dataframe containing the historic data.

    Returns:
        pd.Dataframe: Dataframe with fresh new data.
    """
    latest_date = df['datum'].max()
    today = pd.Timestamp.today()
    if latest_date < today:
        # Refresh the dataset
        logger.info('Updating csv file...')
        new_data_df = get_data(latest_date, today, full_load=False)
    else:
        logger.info('No new data to be downloaded.')
    return new_data_df


def get_last_month_data(df: pd.DataFrame):
    """ Keep only date and increment daily cases and drop every other column. Work with data only 1 month old.

    Args:
        df (pd.DataFrame): Dataframe with all the columns.

    Returns:
        [pd.DataFrame]: Dataframe with only 2 mentioned columns.
    """
    df_temp = df[['datum', 'prirustkovy_pocet_nakazenych']]
    df_temp = df[(df['datum'] <= pd.Timestamp.today()) & (df['datum'] >= pd.Timestamp.today() - pd.Timedelta('31 days'))]
    df_temp = df_temp.reset_index(drop=True)
    return df_temp


def plot_graph(df: pd.DataFrame):
        
    pass


def main():

    if os.path.exists(os.path.join('data','data.csv')):
        data_df = pd.read_csv(os.path.join('data','data.csv'), parse_dates=['datum'])
        data_df = update_data(data_df)
    else:
        data_df = get_data()

    


if __name__ == '__main__':
    main()
    # data_df = pd.read_csv('data.csv', parse_dates=['datum'])
    # update_data(data_df)
    # get_last_month_data(data_df)