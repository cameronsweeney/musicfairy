import argparse, sys, datetime, sqlite3, re, os

from fairy.load import initialize_database

def report_song(dbhandle, song_title):
    sql = """
        SELECT strftime('%Y', ts) AS "year", strftime('%m', ts) as "month",
        artist_name, COUNT(*) as frequency
         
        FROM streams
        WHERE track_name = ?
        GROUP BY year, month
        ORDER BY COUNT(*) DESC;
    """
    connection = sqlite3.connect(dbhandle)
    cursor = connection.cursor()
    result = cursor.execute(sql, (song_title,))
    output = result.fetchall()
    os.makedirs('./reports/songs/', exist_ok=True)
    with open(f"./reports/songs/months-{song_title}.txt", "w+", encoding='utf8') as file:
        for line in output:
            file.write(str(line))
            file.write('\n')
    connection.close()

def report_artist(dbhandle, artist):
    sql = """
    SELECT strftime('%Y', ts) AS "year", strftime('%m', ts) as "month",
    artist_name, COUNT(*) as frequency
     
    FROM streams
    WHERE artist_name = ?
    GROUP BY year, month
    ORDER BY COUNT(*) DESC;
    """
    connection = sqlite3.connect(dbhandle)
    cursor = connection.cursor()
    result = cursor.execute(sql, (artist,))
    output = result.fetchall()
    os.makedirs('./reports/artists/', exist_ok=True)
    with open(f"./reports/artists/months-{artist}.txt", "w+", encoding='utf8') as file:
        for line in output:
            file.write(str(line))
            file.write('\n')
    connection.close()

def report_month(dbhandle, year_month):
    match = re.match("(\d\d\d\d)-(\d\d)", year_month)
    if match is None:
        print("Support for year/month pairs only right now, in format YYYY-MM.")
        sys.exit()

    year = match.group(1)
    month = match.group(2)
    # sqlite3 treats dates as midnights of those dates
    first_day = f"{year}-{month}-01"
    if month == '12':
        month = '00'
        year = str(int(year) + 1).zfill(2)
    last_day = f"{year}-{str(int(month)+1).zfill(2)}-01"
    print(year)
    print(month)

    sql = """
        SELECT artist_name, track_name, spotify_track_uri, COUNT(*) as frequency
        FROM streams
        WHERE ts BETWEEN ? AND ?
        GROUP BY artist_name, track_name
        ORDER BY COUNT(*) DESC;
    """
    connection = sqlite3.connect(dbhandle)
    cursor = connection.cursor()
    result = cursor.execute(sql, (first_day, last_day))
    output = result.fetchall()
    os.makedirs('./reports/months/', exist_ok=True)
    with open(f"./reports/months/{year_month}.txt", "w+", encoding='utf8') as file:
        for line in output:
            file.write(str(line))
            file.write('\n')
    connection.close()

def report_day(dbhandle, year_month_day):
    try:
        date_object = datetime.datetime.strptime(year_month_day, '%Y-%m-%d')
    except ValueError:
        print("Please format your days in the form YYYY-MM-DD.")

    next_day = date_object + datetime.timedelta(days=1)
    next_day_string = next_day.strftime('%Y-%m-%d')

    sql = """
        SELECT artist_name, track_name, spotify_track_uri, COUNT(*) as frequency
        FROM streams
        WHERE ts BETWEEN ? AND ?
        GROUP BY artist_name, track_name
        ORDER BY COUNT(*) DESC;
    """
    connection = sqlite3.connect(dbhandle)
    cursor = connection.cursor()
    result = cursor.execute(sql, (year_month_day, next_day_string))
    output = result.fetchall()
    os.makedirs('./reports/day/', exist_ok=True)
    with open(f"./reports/day/{year_month_day}.txt", "w+", encoding='utf8') as file:
        for line in output:
            file.write(str(line))
            file.write('\n')
    connection.close()

def report_top_songs_all_time(dbhandle):
    sql = """
        SELECT artist_name, track_name, spotify_track_uri, COUNT(*) as frequency
        FROM streams
        GROUP BY artist_name, track_name
        ORDER BY COUNT(*) DESC;
    """
    connection = sqlite3.connect(dbhandle)
    cursor = connection.cursor()
    result = cursor.execute(sql)
    output = result.fetchall()
    os.makedirs('./reports/', exist_ok=True)
    with open(f"./reports/top_songs.txt", "w+", encoding='utf8') as file:
        for line in output:
            file.write(str(line))
            file.write('\n')
    connection.close()

def report_weekday(dbhandle, weekday):
    try:
        date_object = datetime.datetime.strptime(weekday, '%A')
    except ValueError:
        print("Please format your weekdays with a capital letter and full spelling.")
        exit()

    day_of_week_number = date_object.weekday()

    sql = """
        SELECT artist_name, track_name, spotify_track_uri, COUNT(*) as frequency
        FROM streams
        WHERE strftime('%w', ts) = ?
        GROUP BY artist_name, track_name
        ORDER BY COUNT(*) DESC;
    """
    connection = sqlite3.connect(dbhandle)
    cursor = connection.cursor()
    result = cursor.execute(sql, (day_of_week_number,))
    output = result.fetchall()
    os.makedirs('./reports/weekday/', exist_ok=True)
    with open(f"./reports/weekday/{weekday}.txt", "w+", encoding='utf8') as file:
        for line in output:
            file.write(str(line))
            file.write('\n')
    connection.close()

report_switch_dict = {
    'artist': report_artist,
    'song': report_song,
    'top_songs': report_top_songs_all_time,
    'month': report_month,
    'day': report_day,
    'weekday': report_weekday
}


def main():
    dbhandle = "./data/streaming.db"

    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Spotify music fairy')

    # Add main arguments, mutually exclusive
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--initialize', action='store_true', help='Initialize database from data/')
    group.add_argument('-r', '--report', help='Generate report from data', nargs='+')


    # Parse the command-line arguments
    args = parser.parse_args()

    if args.initialize:
        initialize_database(dbhandle, './data/')
    elif args.report:
        # Access the values using the attribute notation
        report_type = args.report[0]
        report_args = args.report[1:]
        
        # look up correct function, based on report_type
        try:
            report_function = report_switch_dict[report_type]
        except NameError:
            print("This type of report doesn't exist (yet?). Try again.")

        # call that function & feed it report_args
        try:
            report_function(dbhandle, *report_args)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print(report_args)


if __name__ == '__main__':
    main()