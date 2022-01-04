from datetime import date
import requests
import pandas as pd
from parameters import ACCESS_TOKEN, URL, COUNTRIES, DTYPES


def get_top_songs_playlist(country):
    """
    Get songs by country by Spotify Api and return DataFrame.
    :param country: str
    :return: pd.DataFrame
    """
    track_name = []
    artists_names = []
    popularity = []
    explicit = []
    solo_or_feat = []

    response = requests.get(
        URL.format(COUNTRIES[country]),
        headers={
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
    )

    items = response.json()['items']
    for item in items:
        track = item['track']
        track_name.append(track['name'])
        popularity.append(track['popularity'])
        explicit.append(track['explicit'])
        artists = []
        for artist in track['artists']:
            artists.append(artist['name'])
        solo_or_feat.append('solo' if len(artists) == 1 else 'feat')
        artists_names.append(', '.join(artists))

    data = {
        'rating': list(range(1, 51)),
        'track_name': track_name,
        'artists_names': artists_names,
        'popularity': popularity,
        'explicit': explicit,
        'solo_or_feat': solo_or_feat,
        'country': country,
        'date_of_playlist': pd.to_datetime(date.today().strftime('%d-%b-%y'))
    }

    return pd.DataFrame(data)


def validate_data(df):
    """
    Validate DataFrame checking shape, NA values, data types
    :param df:
    :return: None
    """
    assert df.shape == (len(COUNTRIES) * 50, 8)
    assert not df.isna().values.any()
    assert (DTYPES == df.dtypes).sum() == 8
