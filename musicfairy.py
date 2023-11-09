import sys, re, sqlite3, pprint
from fairy.report import report_artist

dbhandle = './fairy/streaming.db'

# called with 0 or 1 arguments
if len(sys.argv) <= 2:
    print("Not enough arguments provided. Call this script as > python musicfairy.py report 20YY-MM")
    sys.exit()
if sys.argv[1] == 'test':
    report_artist(dbhandle, sys.argv[2])
    sys.exit()
elif not sys.argv[1] == 'report':
    print("Please enter a recognizeable command. Right now it's just report 20YY-MM")
    sys.exit()

match = re.match("(\d\d\d\d)-(\d\d)", sys.argv[2])
if match is None:
    print("Support for year/month pairs only right now, in format YYYY-MM.")
    sys.exit()

year = match.group(1)
month = match.group(2)
# sqlite3 treats dates as midnights of those dates
first_day = f"{year}-{month}-01"
if month == '12':
    month = '00'
last_day = f"{year}-{str(int(month)+1).zfill(2)}-01"
print(first_day)
print(last_day)

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
#print(output)
with open(f"./reports/{sys.argv[2]}.txt", "w+", encoding='utf8') as file:
    for line in output:
        file.write(str(line))
        file.write('\n')
connection.close()