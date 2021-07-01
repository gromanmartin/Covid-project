import pandas as pd
from loggerconfig import logger


def get_historical_data(start_date: pd.Timestamp = pd.Timestamp('2021-01-01'), end_date: pd.Timestamp = pd.Timestamp('2021-06-30')) -> pd.DataFrame:
    """Get the historical data from given start date up to given end date and save it in csv format.

    Args:
        start_date (pd.Timestamp, optional): Date from which the data gets saved into df. Defaults to pd.Timestamp('2021-01-01').
        end_date (pd.Timestamp, optional): Date up to which the data gets saved into df. Defaults to pd.Timestamp('2021-06-30').

    Returns:
        pd.DataFrame: Dataframe which holds downloaded data.
    """
    url = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv'
    df = pd.read_csv(url)
    df['datum'] = pd.to_datetime(df['datum'])
    df = df[(df['datum'] >= start_date) & (df['datum'] <= end_date)]
    df.to_csv('historical_data.csv', index=False)
    return df


def check_latest_date(df):
    latest_date = df['datum'].max()
    if latest_date < pd.Timestamp.today():
        #commence increment download
        logger.info('Updating csv file...')
        
        pass
    else:
        logger.info('No new data to be downloaded')


if __name__ == '__main__':
    historical_data_df = get_historical_data()
    check_latest_date(historical_data_df)