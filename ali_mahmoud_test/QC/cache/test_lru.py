import unittest
from collections import deque
import time
from . import lru
from . import server
from . import handler
class TestLRU(unittest.TestCase):
    
    '''for the sake of simplicity we'll use one lru
    '''
    
    ser = server.Server()
    ser.add('Bob')
    ser.add('Ed')
    ser.add('Lloyd')        
    ser.add('Hank')
    

    def test_get(self):
        cache = lru.LRU(TestLRU.ser, size=2, expire=False)
        self.assertEqual(cache.get(0), 'Bob')
        self.assertEqual(cache.get(1), 'Ed')
        self.assertEqual(cache.get(2), 'Lloyd')
        self.assertEqual(len(cache.cache), 2)

    def test_fail_get(self):
        cache = lru.LRU(TestLRU.ser, size=2, expire=False)
        self.assertRaises(ValueError, cache.get, 10) #should raise an error as address does not exist in server

    def test_update(self):
        cache = lru.LRU(TestLRU.ser, size=2, expire=False)   
        cache.get(0)
        cache.get(3)
        self.assertEqual(cache.map[0], 1)
        self.assertEqual(cache.map[3], 0) #Hank should be in first place
        self.assertEqual(cache.cache[0], 'Hank') #this is the first item and where the cache will pop from
        self.assertEqual(cache.cache[1], 'Bob')
        cache.get(1) #call to get self.
        self.assertEqual(cache.map[1], 0)
        self.assertEqual(None, cache.map.get(0)) #Bob's value should now be gone
        self.assertEqual(cache.cache[0], 'Ed')
        self.assertEqual(cache.cache[1], 'Hank')

    def test_expiration(self): #now we will test time expiratioon
        cache = lru.LRU(TestLRU.ser, size=2, expiry=0.2, expire=True)
        cache.get(0)
        cache.get(1)
        time.sleep(0.2) #wait a few seconds, cache shoudl expire
        self.assertEqual(len(cache.map), 0)
        self.assertEqual(len(cache.cache), 0)
        cache.get(2)
        cache.get(3) #shouldn't be enough time to expire
        self.assertEqual(len(cache.map), 2)
        self.assertEqual(len(cache.cache), 2)

    #extra, just to check that such a geodistributed implementation would work properly
    #particularly with the use of a "handler" look up table 
    def test_handler(self):
        server1 = server.Server()
        server2 = server.Server()
        server1.add('Bob')
        server1.add('John')
        server2.add('Henry')
        server2.add('David')
        testing_handler = handler.Handler(num_locations=2, cache_expire=False, server_list=[server1, server2]) #this handler will have two caches
        #one with id 0 and the other with id 1
        self.assertEqual(testing_handler.request(0).get(0), 'Bob')
        self.assertEqual(testing_handler.request(1).get(1), 'David')
        self.assertEqual(testing_handler.request(0).get(1), 'John')
        self.assertRaises(ValueError, testing_handler.request, 2)





