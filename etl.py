# etl.py
import os
import glob
import pandas as pd
import logging
from db import get_connection
from sql_queries import *
import psycopg2

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def process_song_file(cur, filepath):
    """Insert artist and song from a song JSON file."""
    try:
        series = pd.read_json(filepath, typ='series', convert_dates=False)
    except Exception:
        df = pd.read_json(filepath)
        series = df.iloc[0]

    artist_data = (
        series.get('artist_id'),
        series.get('artist_name'),
        series.get('artist_location'),
        series.get('artist_latitude'),
        series.get('artist_longitude')
    )
    cur.execute(artist_table_insert, artist_data)

    song_data = (
        series.get('song_id'),
        series.get('title'),
        series.get('artist_id'),
        series.get('year'),
        series.get('duration')
    )
    cur.execute(song_table_insert, song_data)
    logging.info("Inserted song/artist from %s", filepath)

def process_log_file(cur, filepath):
    """Process event log, insert time, users and songplays."""
    df = pd.read_json(filepath, lines=True)
    df = df[df['page'] == "NextSong"].copy()

    # convert ts (ms epoch) to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')

    time_df = pd.DataFrame({
        'start_time': df['ts'],
        'hour': df['ts'].dt.hour,
        'day': df['ts'].dt.day,
        'week': df['ts'].dt.isocalendar().week,
        'month': df['ts'].dt.month,
        'year': df['ts'].dt.year,
        'weekday': df['ts'].dt.day_name()
    }).drop_duplicates(subset=['start_time'])

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    user_df = df[['userId','firstName','lastName','gender','level']].drop_duplicates(subset=['userId'])
    for i, row in user_df.iterrows():
        try:
            user_id = int(row.userId)
        except Exception:
            user_id = None
        cur.execute(user_table_insert, (user_id, row.firstName, row.lastName, row.gender, row.level))

    for index, row in df.iterrows():
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        try:
            user_id = int(row.userId)
        except Exception:
            user_id = None

        songplay_data = (
            row.ts, user_id, row.level, songid, artistid,
            row.sessionId, row.location, row.userAgent
        )
        cur.execute(songplay_table_insert, songplay_data)
    logging.info("Processed log file %s", filepath)

def process_data(conn, filepath, func):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    logging.info("%d files found in %s", num_files, filepath)

    with conn:
        with conn.cursor() as cur:
            for i, datafile in enumerate(all_files, 1):
                func(cur, datafile)
                conn.commit()
                logging.info("%s/%s files processed.", i, num_files)

def main():
    conn = get_connection()
    try:
        process_data(conn, filepath='data/song_data', func=process_song_file)
        process_data(conn, filepath='data/log_data', func=process_log_file)
    finally:
        conn.close()
    logging.info("Finished processing!")

if __name__ == "__main__":
    main()
