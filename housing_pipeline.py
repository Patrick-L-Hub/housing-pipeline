import sys
import os.path
import sqlite3
from scripts import craigslist_scrape

def main():

    df = craigslist_scrape.allListings()
    conn = sqlite3.connect("dbs/NO_housing_data.db")
    #creates a table named New_Orleans_listings of all the web scraping data
    df.to_sql(name='New_Orleans_listings',con = conn,schema=None, if_exists='replace')

if __name__=="__main__":
    main()
