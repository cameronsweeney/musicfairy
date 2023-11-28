import argparse, sys, datetime, sqlite3, re

from fairy.load import create_table_streams, drop_table_streams, load_spotify_json_data, parse_json_data
from fairy.report import test_report

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
    with open(f"./reports/months-{song_title}.txt", "w+", encoding='utf8') as file:
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
    with open(f"./reports/months-{artist}.txt", "w+", encoding='utf8') as file:
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
    with open(f"./reports/{year_month}.txt", "w+", encoding='utf8') as file:
        for line in output:
            file.write(str(line))
            file.write('\n')
    connection.close()

report_switch_dict = {
    'artist': report_artist,
    'song': report_song,
    'month': report_month
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
        drop_table_streams(dbhandle)
        create_table_streams(dbhandle)
        parse_json_data("./data/", dbhandle)
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


#        report_day = ''
#        try:
#            report_day = datetime.datetime.strptime(report_type[0], "%Y-%m-%d").date()
#            print(f'Report arg: {report_day.strftime("%a %b %d %Y")}')
#        except ValueError:
#            print("Sorry, for reports, I'm just accepting days in %Y-%m-%d format right now.")

if __name__ == '__main__':
    main()