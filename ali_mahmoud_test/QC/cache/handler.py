''' 
This is where all the requests are handled, the handler contains a list of geolocations 
Each geolocation has an lru cache and an associated server
The handler recieves a request with an id (no address)
It contains a list of caches and returns the address of the cache the user should use
based on their geolocation
The handler does not grab the item from the cache because it would not make sense with location based 
transfer speeds
The handler is a central lookup table essentially.
'''
from . import server as server
from . import lru as lru


class Handler:
    
    def __init__(self, num_locations=10, cache_size=10, cache_expiry=10, cache_expire=True, server_list=None):
        self.num_locations = num_locations
        self.caches = {}
        for i in range(num_locations):
            #for each location create an lru and assoociate it with a server
            #the cache and server don't need information on what their location actually is
            #this should be handeled seperately; i.e. in this class
            if server_list==None : #we will initialize new servers for each cache
                self.caches[i] = lru.LRU(server.Server(), size=cache_size, expiry=cache_expiry, expire=cache_expire)
            else:
                if len(server_list) != num_locations:
                    raise ValueError('Number of servers should be the same as number of locations.')
                self.caches = [lru.LRU(server_list[i], 
                size=cache_size, expiry=cache_expiry, expire=cache_expire) for i in range(num_locations)]    



    def request(self, id:int):
        '''
        This is where item requests are made
        Request with and id that contains information on location of request
        For simplicity's sake we assume the id to be the location number (0 - num_locations)
        Returns the cache where a get() should be made
        '''
        if(int(round(id)) > self.num_locations-1 or id < 0):
            raise ValueError(f'The given id is invalid because it is out of range. There exists {self.num_locations} locations.')
        location = int(round(id))  #in case the id is not exact
        #now it will try to get x from the cache, if it can't find it the cache will automatically request from its associated server 
        return self.caches[id]

