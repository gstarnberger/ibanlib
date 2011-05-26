#!/usr/bin/env python

import unittest
from doctest import DocFileSuite, REPORT_ONLY_FIRST_FAILURE

def test_suite():
    suite = DocFileSuite('README.txt',
                         package='ibanlib',
                         optionflags = REPORT_ONLY_FIRST_FAILURE)
    return suite
    
if __name__ == '__main__':
    suite = test_suite()
    unittest.TextTestRunner().run(suite)
