from pymongo import MongoClient
from Site import Site


class Main(object):

    def __init__(self, site, num_beds):
        self.__site = site
        self.__num_beds = num_beds

    def connect_db(self):
        print("Establishing connection...")
        client = MongoClient()
        db = client.apt_db
        if self.__num_beds == 1:
            coll = db.one_beds
        elif self.__num_beds == 2:
            coll = db.two_beds
        elif self.__num_beds == 3:
            coll = db.three_beds
        elif self.__num_beds == 4:
            coll = db.four_up_beds
        else:
            coll = db.other
        coll.delete_many({})
        print("Generating DF...")
        df = self.__site.append_dfs()
        coll.insert_many(df.to_dict('records'))
        print("Insertion Finished!")


one_bed = Site("boston", "ma", "1", "1", "0", "100000")
two_bed = Site("boston", "ma", "2", "1", "0", "100000")
three_bed = Site("boston", "ma", "3", "1", "0", "100000")
four_bed = Site("boston", "ma", "4", "1", "0", "100000")
print("Starting Process...")

#main1 = Main(one_bed, 1)
#main2 = Main(two_bed, 2)
#main3 = Main(three_bed, 3)
main4 = Main(four_bed, 4)

#main1.connect_db()
#main2.connect_db()
#main3.connect_db()
main4.connect_db()



