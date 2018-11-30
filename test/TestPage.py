from unittest import TestCase
import pandas as pd
from Page import Page
from bs4 import BeautifulSoup
import urllib.request as url

# global variables for testing
apt = "https://www.apartments.com/32-fisher-ave-boston-ma/r1l4v40/"
lux_apt = "https://www.apartments.com/lantera-at-boston-landing-boston-ma/k7pdq3b/"
add_head = ['Address', 'City', 'State', 'Zip']
head = ['Beds', 'Baths', 'Rent', 'Deposit', None, 'Sq Ft', 'Lease Length', None, 'Available']
full_head = add_head + head
data = ['4', '1', '3800', '$3,800 ', '1,300 Sq Ft', '12 Month Lease', '\r\n                Sep 1\r\n            ']
clean_data = ["4", "1", "3800", "$3800", "1300SqFt", "12MonthLease", "Sep1"]
address = ["32 Fisher Ave", "Boston", "MA", "02120"]
full_address = address + clean_data


class TestPage(TestCase):
    def test_gen_head(self):
        p = Page(apt)
        h = add_head + head
        self.assertEqual(h, p.gen_head())

    def test_find_add(self):
        p = Page(apt)
        self.assertEqual(address, p.find_add())

    def test_check_invalid1(self):
        p = Page(apt)
        self.assertEqual(False, p.check_invalid())

    def test_check_invalid2(self):
        p = Page(lux_apt)
        self.assertEqual(True, p.check_invalid())


        