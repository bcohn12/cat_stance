"""
This code tests endpoint calculations for a 3-limb, 3-DOF system
"""

import unittest
from endpoint_calculation import *
 
class TestUM(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_floatingpoint_endpt(self):
        self.assertEqual(endpoint_position(q=[0.882,15,10],L=[50,10,20]),
        	[26.726422123102726, 48.759316394365776, 25.881999999999998])
 
    def test_integer_endpt(self):
        self.assertEqual( endpoint_position(q=[0,0,0],L=[10,10,10]),
        	[30.0, 0.0, 0])

if __name__ == '__main__':
    unittest.main(exit=False)
if __name__ == '__main__':
    unittest.main(exit=False)