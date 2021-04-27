'''
This class simulates a server in a certain location
The server will have a given location that will also be associated with a certain cache
This is implemented as a dicitonary, key is the address and value is the actual item at the address
A server would be much slower than the cache
Server has a limit, if we go over the limit an error will be raised
This specific class doesn't do much, it is just for the sake of simulation
'''

class Server:

    def __init__(self, limit=100):
        self.items = {}    #this represents the server
        self.limit = limit
        
    def add(self, x): #add item to server
        for k,v in self.items.items():
            #find the first empty slot
            if(v == None):
                #empty address
                self.items[k] = x
                return k
        #otherwise create a new slot
        if(len(self.items) == 0):
            i = 0
        else:    
            i = max(list(self.items.keys())) + 1
        if(i > self.limit):
            #server is already full
            raise IndexError(f'Server is already full, could not add item. Server limit: {self.limit}')
        self.items[i] = x
        return i
    
    def clear(self):
        self.items.clear()
    
    def add_at_index(self, i, x): #add item at an index, will overwrite previous item if it exists
        previous = self.items[i]
        self.items[i] = x #add the item to the server
        return previous    # return the old item for convenience

    def remove_item(self, x): #remove item from server
        for k, v in self.items.items():
            if v == x:
                self.items[k] = None 
                return k #address of item
        return -1 #item not found
    
    def clear_index(self, i):
        if i in self.items.keys:
            x = self.item[i]
            self.items[i] = None
            return x
        return None    
            
    
    def exists(self, x): #check if it is there
        return x in list(self.items.values())      

    def occupied(self, i):
        #return if index exists and contains item
        return i < self.limit and (i in self.items) and self.items[i] != None

    def get(self, i):
        if(self.occupied(i)):
            return self.items[i]
        raise ValueError(f'Address {i} empty in the server')
        
    def get_index(self, x): #if an item exists get its index
        for k,v in self.items.items():
            if(v == x):
                return k
        return -1 #doesn't exist 
        
