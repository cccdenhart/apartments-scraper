from unittest import TestCase
from Site import Site
from Page import Page

apts = "https://www.apartments.com/boston-ma/3-bedrooms-2-bathrooms-2000-to-3000/"


class TestSite(TestCase):
    def test_const_url(self):
        s = Site("boston", "ma", "3", "2", "2000", "3000")
        self.assertEqual(apts, s.const_url())

    def test_max_page(self):
        s = Site("boston", "ma", "3", "2", "2000", "3000")
        self.assertEqual(21, s.max_page())

    def test_get_apt_df(self):
        s = Site("boston", "ma", "3", "2", "2000", "3000")
        p = Page(apts)
        self.assertEqual(p.get_df(), s.get_apt_df())