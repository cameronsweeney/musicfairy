# Put functions to import here
# open an endsong_json file & read data
# put in sqlite db if not already stored there
import sqlite3, json, os

#def function to CREATE TABLE
def create_table_streams(dbhandle):
    print("Creating table 'streams'...")
    create_table = """
        CREATE TABLE streams(
            ts text,
            ms_played integer,
            conn_country text,
            track_name text,
            artist_name text,
            album_name text,
            spotify_track_uri text,
            episode_name text,
            episode_show_name text,
            reason_start text,
            reason_end text,
            shuffle text,
            skipped text,
            offline text,
            offline_timestamp integer,
            incognito_mode text
        );"""
    connection = sqlite3.connect(dbhandle)
    cursor = connection.cursor()
    result = cursor.execute(create_table)
    print(result.fetchone())
    connection.close()

#def function to DROP TABLE
def drop_table_streams(dbhandle):
    print("Dropping table 'streams'...")
    drop_table = """
        DROP TABLE streams;
    """
    connection = sqlite3.connect(dbhandle)
    cursor = connection.cursor()
    cursor.execute(drop_table)
    connection.close()

def load_spotify_json_data(filehandle, dbhandle):
    with open(filehandle, "r", encoding="utf8") as file:
        new_data = file.read()
        data_dict = json.loads(new_data)
    #for stream_data in data_dict.copy():
    #    del stream_data["username"]
    #    del stream_data["platform"]
    #    del stream_data["ip_addr_decrypted"]
    #    del stream_data["user_agent_decrypted"]
    connection = sqlite3.connect(dbhandle)
    cursor = connection.cursor()
    insert_stream = """
        INSERT INTO streams
        VALUES (:ts, :ms_played, :conn_country, :master_metadata_track_name, :master_metadata_album_artist_name, :master_metadata_album_album_name, :spotify_track_uri, :episode_name, :episode_show_name, :reason_start, :reason_end, :shuffle, :skipped, :offline, :offline_timestamp, :incognito_mode);
        """
    cursor.executemany(insert_stream, data_dict)
    connection.commit()
    # loop through songs
        # don't count plays below a certain threshold (30 secs?)
        # ensure that timestamp is globally unique
        # attempt to add to database
    connection.close()
    
def parse_json_data(directory, dbhandle):
    print("Parsing raw JSON data from Spotify...")
    current_directory = os.getcwd()
    all_files = os.listdir(directory)
    files_to_check = [file for file in all_files if file.startswith('Streaming_History_Audio_') and file.endswith('.json')]
    print(all_files)
    for filehandle in files_to_check:
        print(f"    Parsing {filehandle}...")
        load_spotify_json_data(directory+filehandle, dbhandle)