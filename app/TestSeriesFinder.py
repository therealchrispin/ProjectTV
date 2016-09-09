import unittest
from app import seriesFinder


class MyTestCase(unittest.TestCase):

    def test_find_all_series(self):
        self.assertIsInstance(seriesFinder.find_all_seires(),dict)

    def test_get_Poster(self):
        self.assertEqual(seriesFinder.get_poster("test","test"),'http://127.0.0.1:5000/static/images/test.jpg')

    # def test_getAnimatedSeries(self):
    #     firstList = seriesFinder.animatedSeries
    #
    #     seriesFinder.getAnimatedSeries()
    #     secondList = seriesFinder.animatedSeries
    #     self.assertGreater(len(secondList),len(firstList))






if __name__ == '__main__':
    unittest.main()
