import argparse, sys, datetime

from fairy.load import create_table_streams, drop_table_streams, load_spotify_json_data, parse_json_data
from fairy.report import test_report

def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Spotify music fairy')

    # Add main arguments, mutually exclusive
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--initialize', action='store_true', help='Initialize database from data/')
    group.add_argument('-r', '--report', help='Generate daily report')


    # Parse the command-line arguments
    args = parser.parse_args()

    if args.initialize:
        dbhandle = "./data/streaming.db"
        drop_table_streams(dbhandle)
        create_table_streams(dbhandle)
        parse_json_data("./data/", dbhandle)
    elif args.report:
        # Access the values using the attribute notation
        report_type = args.report
        report_day = ''
        try:
            report_day = datetime.datetime.strptime(report_type[0], "%Y-%m-%d").date()
            print(f'Report arg: {report_day.strftime("%a %b %d %Y")}')
        except ValueError:
            print("Sorry, for reports, I'm just accepting days in %Y-%m-%d format right now.")


if __name__ == '__main__':
    main()