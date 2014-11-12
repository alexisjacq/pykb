#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import unittest
import time
import kb
from minimalkb import __version__

from Queue import Empty

REASONING_DELAY = 0.2

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.kb = kb.KB()
        self.kb.clear()

    def tearDown(self):
        self.kb.close()

    def test_basics(self):

        self.kb.hello()

        with self.assertRaises(kb.KbError):
            self.kb.add()
        with self.assertRaises(kb.KbError):
            self.kb.add("toto")


    def test_existence(self):


        with self.kb.active_models(['alexis','robot']):
            self.kb += ["glass_2 rdf:type Glass","glass_2 isOn desktop"]
        with self.kb.active_models(['robot']):
            self.kb += ["glass_1 rdf:type Glass","glass_1 isOn desktop"]

        with self.kb.active_models(['alexis']):
            self.assertTrue( "glass_2" in self.kb)
            self.assertFalse( "glass_1" in self.kb)

        with self.kb.active_models(['robot']):
            self.assertTrue( "glass_1" in self.kb)
            self.assertTrue( "glass_1" in self.kb)
        
        with self.kb.active_models(['alexis','robot']):
            self.assertTrue( "glass_2" in self.kb)
            self.assertTrue( "glass_1" in self.kb)
            


def version():
    print("minimalKB tests %s" % __version__)

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Test suite for minimalKB.')
    parser.add_argument('-v', '--version', action='version',
                       version=version(), help='returns minimalKB version')
    parser.add_argument('-f', '--failfast', action='store_true',
                                help='stops at first failed test')

    args = parser.parse_args()


    kblogger = logging.getLogger("kb")
    console = logging.StreamHandler()
    kblogger.setLevel(logging.DEBUG)
    kblogger.addHandler(console)
    
    unittest.main(failfast=args.failfast)
