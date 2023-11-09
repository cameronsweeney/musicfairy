import sys, sqlite3, json, os
from fairy.load import create_table_streams, drop_table_streams, load_spotify_json_data
from fairy.report import test_report


def parse_json_data(directory, dbhandle):
    print("Parsing raw JSON data from Spotify...")
    current_directory = os.getcwd()
    all_files = os.listdir(current_directory)
    files_to_check = [file for file in all_files if file.startswith('Streaming_History_Audio_') and file.endswith('.json')]
    for filehandle in files_to_check:
        print(f"    Parsing {filehandle}...")
        load_spotify_json_data(filehandle, dbhandle)

def main():
    dbhandle = "./fairy/streaming.db"
    drop_table_streams(dbhandle)
    create_table_streams(dbhandle)
    parse_json_data("./data/", dbhandle)
    print(test_report(dbhandle))

if __name__ == '__main__':
    main()