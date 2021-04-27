from collections import deque
from . import server
import random
import time
import threading

'''
This is LRU cache
It is associated with a certain server that must be passed in to init
The LRU is associated with the server of the same region it is associated with
The user requests are made to the handler (handler.py) that recieves both the item requested and an id
The id informs of the location, the handler then requests the item from the lru of that region
If there is a hit the item is returned,
otherwise the lru will request from its associated server and update the cache before returning the item
Thus actual implementation or regions is doen external to this class as it is a feature that is not specific to the cache itself
'''

class LRU:
    
    def __init__(self, server, size=10, expiry=10, expire=True):
        if(size < 0):
            raise ValueError('Cache cannot have a negative size.')
        if(expiry<0):
            raise ValueError('Expiry cannot be negative.')   
        
        self.server = server #a server associated with the cache to which it can make requests for items
        self.map = {}   #this will be our hashmap for the lru
        self.cache = deque(maxlen=size) #this is the cache, implemented as a double linked list (or a queue to be specific)
        self.size = size
        self.start_time = time.time()
        self.expiry = expiry
        '''
        When the cache is initialized a ticker begins and the cache will clear after self.expiry time has passed
        This ticker is run as a daemon thread in the background
        This is only if the expire parameter is True, otherwise the cache will not thread and will not expire 
        '''
        if(expire):
            self.run_ticker()

    def clear(self):
        #clears cache and map
        self.map.clear()
        self.cache.clear()
    
    def ticker(self):
        '''Implementation of expiration, this function contnuously "ticks" and clears the cache at self.expiry time steps'''
        while True:
            if(time.time() > self.start_time + self.expiry):
                #clear the cache and map
                self.clear()
                self.start_time = time.time() #restart the timer

    
    def run_ticker(self):
        #this begins ticking, being a daemon thread it will shut down automatically when the program stops
        thread = threading.Thread(target=self.ticker, daemon=True, name='Tick')
        thread.start()    


    def get(self, i):
        ''' request some item at ADDRESS i'''
        
        if(i in self.map.keys()): #hit! item is in the cache
            return self.move_up(i) #update its location in the queue and return it
        else:
            #miss! so we need to get it from the server and update it
            try:
                item = self.server.get(i) #get the item at adress i from the server
            except(ValueError): 
                #in the case that the address does not exist raise an error
                raise ValueError(f'An error occured when getting item at address {i}. Server limit: {self.server.limit}')
            self.update(i, item)
            return item


    def move_up(self, i):
        #No items get removed here, we just 'reshuffle' moving the item up
        index = self.map[i]
        item = self.cache.pop(index) # we will remove the item to put it in the front of the queue instead
        self.cache.appendleft(item) # will append the item now to the front of the queue (moving up)
        for k,v in self.map.items():
            self.map[k] += 1 #update indices in the map
        self.map[i] = 0    #the item now is at the front of the queue
        return item #return the item

    def update(self, i, item):
        #Recieves a new item from the server when there is a miss, we will update the cache
        if(len(self.cache) == self.size): #cache is currently full, we need to get rid of LRU
            del self.map[max(self.map, key=self.map.get)] #remove from the map the key with the highest value
            #as the value gives us the index in the queue, the lru will have the highest value
            
        for k,v in self.map.items(): #everything will get moved up so update the indices
            self.map[k] += 1
        self.map[i] = 0 #the new item will be put in front, most recently used
        self.cache.appendleft(item)    #add the item to the queue
        #since the queue has a max size the lru item will automatically be removed 

