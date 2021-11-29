
from bs4 import BeautifulSoup
import requests
import pandas as pd


def makeSoup(webpage):
    '''
    grab html from the specified webpage and format it into a beautiful
    soup object that is easily parsed
    '''
    soup = BeautifulSoup(webpage.content,"lxml")
    return soup


def pageListings(soup):
    '''
    parse html of page listings and extract the posting title,
    href link, published date, price, number of bedrooms and sqft of the home.
    convert data to a pandas data frame
    '''
    housing_list = []
    #find info/metrics of each post
    num_list = int(soup.find(class_="total").get_text())
    for row in soup.find_all(class_= "result-row"):
        #Try except to avoid null value errors
        num_br_sqft = []
        try:
            pid = row.get('data-pid') #posting id
            rtitle = row.find(class_="result-title hdrlnk").get_text()
            href = row.find(class_="result-title hdrlnk").get('href')
            date = row.find(class_="result-date").get('datetime')
            price = row.find(class_='result-price').text
            bed_size = row.find(class_='housing').get_text().split('\n')
            if "br" not in bed_size[1] and "ft" not in bed_size[1]:
                bed_size[1] = "N/A"
            elif "ft" in bed_size[1]:
                bed_size[2] = bed_size[1]
                bed_size[1] ="N/A"
            num_br_sqft.append([bed_size[1].replace(" ","").replace("-",""),bed_size[2].replace(" ","").replace("-","").replace("ft2"," sqft")])
            br = num_br_sqft[0][0]
            sqft = num_br_sqft[0][1]
            housing_list.append([pid,rtitle,price,br,sqft,date]+[href])
        except:
            pass

    df = pd.DataFrame(housing_list)
    df.columns=['post_id','title','price','num_br','sqft','post_date','url']

    return(df,num_list)

def allListings():
    '''
    loop through all listings by adjusting the web page to scrape
    each web page has a maximum of 120 listings but there can be up to 3000
    listings for a given region
    append to master dataframe after grabbing generating a dataframe for
    the given webpage
    '''
    tot_df = pd.DataFrame()
    webpage = requests.get('https://neworleans.craigslist.org/d/real-estate/search/rea')
    curr_df, num_list = pageListings(makeSoup(webpage))
    tot_df = tot_df.append(curr_df, ignore_index = True)
    for i in range(0,3000,120):
        if i >= num_list:
            break
        webpage = requests.get('https://neworleans.craigslist.org/d/real-estate/search/rea?s='+str(i))
        curr_df,num_list = pageListings(makeSoup(webpage))
        tot_df = tot_df.append(curr_df, ignore_index = True)

    return tot_df
