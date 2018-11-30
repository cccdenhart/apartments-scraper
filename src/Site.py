# import packages
from bs4 import BeautifulSoup
import urllib.request as url
from Page import Page

apts = "https://www.apartments.com/boston-ma/3-bedrooms-2-bathrooms-2600-to-2700/"


# represents a site consisting of all apartments for a given search
class Site(object):
    base_url = "https://www.apartments.com/"

    def __init__(self, city, state, beds, baths, min_rent, max_rent):
        self.__city = city
        self.__state = state
        self.__beds = beds
        self.__baths = baths
        self.__min_rent = min_rent
        self.__max_rent = max_rent

    # constructs a site url based on the given criteria
    def const_url(self):
        location = self.__city + "-" + self.__state + "/"
        size = self.__beds + "-bedrooms-" + self.__baths + "-bathrooms-"
        price = self.__min_rent + "-to-" + self.__max_rent + "/"
        new_url = Site.base_url + location + size + price
        return new_url

    # generates a BeautifulSoup version of the site pulled from the url
    def gen_site(self, given_url):
        apts_site = url.urlopen(given_url)
        soup = BeautifulSoup(apts_site, "html.parser")
        print(soup.prettify())
        return soup

    # identify the max number of pages on this site by generating a list of all page numbers
    def max_page(self):
        soup = self.gen_site(self.const_url())
        all_pages = []
        for link in soup.find_all('a'):
            if link.get('data-page') is not None:
                all_pages.append(link.get('data-page'))
        if all_pages == []:
            all_pages = [1]
        # generate a list of non NoneType apartments at this URL
        real_pages = []
        for var in all_pages:
            if var is not None:
                print(var)
                int_var = int(var)
                real_pages.append(int_var)
        max_page = max(real_pages)
        return max_page

    # retrieves the DataFrame of an apartment using the given url
    @staticmethod
    def get_apt_df(apt_url):
        page = Page(apt_url)
        df = page.get_df()
        return df

    # generates a list of links for all apartments on the given page
    def find_apt_urls(self, given_url):
        apt_links = self.gen_site(given_url).findAll('a', {'class': 'placardTitle js-placardTitle '})
        apt_urls = []
        for link in apt_links:
            gen_url = link.get('href')
            if not Page(gen_url).check_invalid():
                apt_urls.append(gen_url)
        # get unique urls by converting it to a set, then convert it back to a list
        apt_urls = list(set(apt_urls))
        return apt_urls

    # assemble a list of links for all apartments under the given search criteria
    def get_all_urls(self):
        base_url = self.const_url()
        all_apt_urls = []
        last = self.max_page()
        if last > 1:
            for i in range(1, last):
                page_url = base_url + str(i) + "/"
                page_apt_urls = self.find_apt_urls(page_url)
                all_apt_urls.extend(page_apt_urls)
        else:
            page_apt_urls = self.find_apt_urls(base_url)
            all_apt_urls.extend(page_apt_urls)
        # get unique urls by converting the list to a set, then convert it back to a list so it can be indexed
        all_apt_urls = list(set(all_apt_urls))
        return all_apt_urls

    # append the DataFrames for the given list of apartments
    def append_dfs(self):
        all_urls = self.get_all_urls()
        num_urls = len(all_urls)
        full_df = self.get_apt_df(all_urls[0])
        if num_urls > 1:
            for i in range(1, num_urls):
                next_url = all_urls[i]
                next_df = self.get_apt_df(next_url)
                full_df = full_df.append(next_df)
        return full_df

    # exports the DataFrame from this instance to a CSV file
    def export_csv(self, fp):
        df = self.append_dfs()
        df.to_csv(path_or_buf=fp)


site = Site("boston", "ma", "1", "", "", "")
print()
site.append_dfs()