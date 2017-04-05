#!/usr/bin/python3

import unittest
import bnstats
import os


class DataFile(unittest.TestCase):
    def test_downloading(self):
        if os.path.exists(bnstats.DATA_FILE):
            os.remove(bnstats.DATA_FILE)

        bnstats.download_data()
        self.assertTrue(os.path.exists(bnstats.DATA_FILE))

    def test_reading(self):
        nodes = bnstats.read_datafile()
        self.assertEqual(type(nodes), dict)
        self.assertNotEqual(int(nodes['total_nodes']), 0)


class Data(unittest.TestCase):
    def test_countries(self):
        countries = bnstats.node_counter(bnstats.read_datafile(), 7, 10)
        self.assertEqual(len(list(countries)), 10)

    def test_networks(self):
        networks = bnstats.node_counter(bnstats.read_datafile(), 12, 10)
        self.assertEqual(len(list(networks)), 10)

if __name__ == '__main__':
    unittest.main()
