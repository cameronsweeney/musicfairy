from fairy.report import test_report

def main():
    dbhandle = "./fairy/streaming.db"
    print(test_report(dbhandle))

if __name__ == '__main__':
    main()