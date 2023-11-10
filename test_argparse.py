import argparse, sys, datetime

def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Spotify music fairy')

    # Add positional argument
    parser.add_argument('--report', help='Generate daily report', nargs=1)

    # Add optional arguments
    #parser.add_argument('--output', '-o', help='Path to the output file')
    #parser.add_argument('--output', '-o', help='Path to the output file')
    #parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose mode')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the values using the attribute notation
    report_type = args.report
    report_day = ''

    try:
        report_day = datetime.datetime.strptime(report_type[0], "%Y-%m-%d").date()
    except ValueError:
        print("Sorry, just accepting days in %Y-%m-%d format right now.")

    # Your program logic goes here
    print(f'Report arg: {report_day.strftime("%a %b %d %Y")}')

if __name__ == '__main__':
    main()
