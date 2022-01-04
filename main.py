from get_and_check_data import *
from db_connection import *
import time


if __name__ == '__main__':
    start = time.perf_counter()

    all_dfs = []
    for country in COUNTRIES.keys():
        all_dfs.append(get_top_songs_playlist(country))
    df = pd.concat(all_dfs, ignore_index=True)

    try:
        validate_data(df)
    except AssertionError:
        raise AssertionError('Data is not valid(((')

    with get_oracle_conn() as connection:
        df.to_sql('spotify_data', connection, if_exists='append', index=False)

    print('время:', time.perf_counter() - start, 'сек.')
