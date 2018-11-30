# import packages
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import numpy as np

apt1 = "https://www.apartments.com/lantera-at-boston-landing-boston-ma/k7pdq3b/"
apt2 = "https://www.apartments.com/164-newton-st-boston-ma/90hfjx6/"
apt3 = "https://www.apartments.com/forbes-building-over-age-62-and-or-disabled-jamaica-plain-ma/tl3qvdc/"
apt4 = "https://www.apartments.com/amy-lowell-apartments-boston-ma/1hp80c5/"
apt5 = "https://www.apartments.com/64-1-2-day-st-boston-ma-unit-1/g9fvkvw/"
apt6 = "https://www.apartments.com/119-browne-st-brookline-ma/2hv9szc/"


# UTILITY FUNCTIONS:

# returns a list of all indices where the given element occurs at in the given list
# from: https://stackoverflow.com/questions/6294179/how-to-find-all-occurrences-of-an-element-in-a-list
def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return result
        result.append(offset)


# finds indexes at which values are of NoneType
def find_bad_cols(lst):
    bad_cols = indices(lst, None)
    return bad_cols


# cleans any bad characters out of the given list
def clean_list(lst):
    new_list = []
    for item in lst:
        if item is not None:
            new_item = item.replace("\r\n", "")
            new_item = new_item.replace(" ", "")
            new_item = new_item.replace("$", "")
            new_item = new_item.replace("MonthLease", "")
            new_list.append(new_item)
        else:
            new_list.append(item)
    return new_list


# Class representing a single apartment page
class Page(object):
    # the class name to be used to find the proper table in the page html
    className = 'availabilityTable basic oneRental'

    def __init__(self, given_url):
        self.__given_url = given_url

    # pulls the url given to the class in using the urllib.request package
    def pull_url(self):
        print(self.__given_url)
        req = Request(self.__given_url)
        apt_page = urlopen(req)
        soup = BeautifulSoup(apt_page, "html.parser")
        print(soup.prettify())
        return soup

    # identifies the table using the local className and returns its rows as a list
    def get_rows(self):
        soup = self.pull_url()
        table = soup.find('table', Page.className)
        all_rows = list(table.findAll("tr"))
        return all_rows

    # generates a list of the column names using the list of rows
    def gen_head(self):
        header = ["Address", "City", "State", "Zip"]
        rows = self.get_rows()[0:1]
        head_row = rows[0:1]
        for row in head_row:
            for h in row.findAll("th"):
                header.append(h.string)
        return header

    # removes the items from the given list where the head has NoneType values
    def clean_bad_list(self, lst):
        bad_cols = find_bad_cols(self.gen_head())
        clean_cols = np.delete(lst, bad_cols).tolist()
        return clean_cols

    # finds the property address, city, and state and returns that information
    def find_add(self):
        soup = self.pull_url()
        address = soup.find('meta', {'itemprop': 'streetAddress'}).get('content')
        city = soup.find('meta', {'itemprop': 'addressLocality'}).get('content')
        state = soup.find('meta', {'itemprop': 'addressRegion'}).get('content')
        zip = soup.find('meta', {'itemprop': 'postalCode'}).get('content')
        fullAdd = [address, city, state, zip]
        return fullAdd

    def backup_find_add(self):
        div = self.pull_url().find('div', {'class': 'propertyAddress'})
        spans = div.find_all('span')
        address = spans[0].string
        city = spans[1].string
        state = spans[2].string
        zip = spans[3].string
        fullAdd = [address, city, state, zip]
        return fullAdd

    # generates all of the data for each row that is not data
    def gen_data(self):
        allData = []
        rows = self.get_rows()
        data_rows = rows[1:len(rows)]
        for row in data_rows:
            beds = row.attrs['data-beds']
            baths = row.attrs['data-baths']
            rent = row.attrs['data-maxrent']
            try:
                data = self.find_add()
            except:
                data = self.backup_find_add()
            for d in row.findAll("td"):
                if d.attrs['class'][0] == "beds":
                    result = beds
                elif d.attrs['class'][0] == "baths":
                    result = baths
                elif d.attrs['class'][0] == "rent":
                    result = rent
                else:
                    result = d.string
                data.append(result)
            clean_data = self.clean_bad_list(data)
            allData.append(clean_data)
        return allData

    # merges the cleaned header and data columns and returns them as a DataFrame
    def get_df(self):
        head = clean_list(self.clean_bad_list(self.gen_head()))
        data = []
        for row in self.gen_data():
            data.append(clean_list(row))
        df = pd.DataFrame(data, columns=head)
        return df

    # determines if this page is for luxury apartment(s)
    def check_invalid(self):
        is_invalid = False
        try:
            self.get_rows()
        except AttributeError:
            is_invalid = True
        return is_invalid


p = Page(apt3)
print(p.get_df())

