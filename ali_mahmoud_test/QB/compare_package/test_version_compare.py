from . import version_compare as ver
import unittest

'''
This module contains all the unit tests
'''

class TestComparor(unittest.TestCase):
    def test_smaller_1(self):
        #test when first less than second
        self.assertEqual(ver.version_compare('1.1.2', '1.1.3'), -1)
    
    def test_smaller_2(self):
        #test when first is less than second, but varying length
        self.assertEqual(ver.version_compare('2.3.1', '2.3.1.6'), -1)
    
    def test_empty(self):
        #pass an empty string as one of the arguments, should raise an error
        self.assertRaises(ValueError, ver.version_compare, '', '0.0')
    
    def test_greater_1(self):
        #test when first greater than second
        self.assertEqual(ver.version_compare('2.1', '1.2'), 1)  

    def test_greater_2(self):
        #test when first greater than second
        self.assertEqual(ver.version_compare('2.1.6', '2.1.3.4.5.9'), 1)        

    def test_same_1(self):
        #test when they are the same
        self.assertEqual(ver.version_compare('4.5.6', '4.5.6'), 0)  
    

    def test_same_2(self):
        #test when they are the same
        #we add padding just to make sure it knows to ignore it
        self.assertEqual(ver.version_compare('2.1.1', '2.1.1.0.0.0'), 0)   

    
    '''we'll test the helper functions below as well'''


    def test_verify_1(self):
        #check that our verifier works when input is incorrect, two dots here
        self.assertFalse(ver.verify_input('1.3..4'))

    def test_verify_2(self):
        #check verifier, string has a character not numeric
        self.assertFalse(ver.verify_input('1.3.j4'))

    def test_has_padding_1(self):
        #verify that our function recognizes when there is padding at a certain point, i.e. just a bunch of zeroes 
        #This function doesn't take a string but a list of numbers (as strings)      
        # starting index is 3 here         
        self.assertTrue(ver.has_padding(3, '1.2.3.0.0.0.0.0'.split('.')))

    def test_has_padding_2(self):
        #verify that our function recognizes when there is padding at a certain point, i.e. just a bunch of zeroes 
        #This function doesn't take a string but a list of numbers (as strings)      
        # starting index is 3 here         
        self.assertFalse(ver.has_padding(2, '1.2.3'.split('.')))    

