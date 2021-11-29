import sys
import os.path
import sqlite3
from scripts import craigslist_scrape




def main():
    #os.path.isfile('dbs/' + "test.db")
    df = craigslist_scrape.allListings()
    print(df.head(10))
    #connects to test.db or creates it if it does not already exist
    conn = sqlite3.connect("dbs/NO_housing_data.db")
    #creates a table named New_Orleans_listings of all the web scraping data
    df.to_sql(name='New_Orleans_listings',con = conn,schema=None, if_exists='replace')
    #cursor = conn.cursor()
    

if __name__=="__main__":
    main()
