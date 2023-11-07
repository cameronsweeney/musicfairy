import sys, sqlite3, json
from fairy.load import create_table_streams, drop_table_streams, load_spotify_json_data
from fairy.report import test_report


def parse_json_data(directory, range_max, dbhandle):
    print("Parsing raw JSON data from Spotify...")
    for x in range(range_max+1):
        filehandle = f"./data/endsong_{x}.json"
        print(f"    Parsing {filehandle}...")
        load_spotify_json_data(filehandle, dbhandle)

def main():
    dbhandle = "./fairy/streaming.db"
    drop_table_streams(dbhandle)
    create_table_streams(dbhandle)
    parse_json_data("./data/", 21, dbhandle)
    print(test_report(dbhandle))

if __name__ == '__main__':
    main()