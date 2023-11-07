# export a function to make a report for days here
# call as python musicfairy.py report day 20YY-MM-DD

import sqlite3, sys

#def test_report to test that streams table was populated with data
def test_report(dbhandle):
    test_select = """
        SELECT ts, conn_country

        FROM streams
        WHERE track_name = 'Lone Star'
        ORDER BY ts ASC;
    """
    connection = sqlite3.connect(dbhandle)
    cursor = connection.cursor()
    result = cursor.execute(test_select)
    output = result.fetchall()
    connection.close()
    return output

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