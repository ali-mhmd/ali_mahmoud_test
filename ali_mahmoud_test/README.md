# Ormuco Technical Test - Developer - Ali Mahmoud
All the questions were coded in Python3, running the programs may fail with an earlier version of Python.

## Question A:
> Your goal for this question is to write a program that accepts two lines (x1,x2) and (x3,x4) on the x-axis and returns whether they overlap. As an example, (1,5) and (2,6) overlaps but not (1,5) and (6,8).

I implemented this program in QA/scripts/QA.py
The program can be run using the following command:

` python3 QA/scripts/QA.py <x1> <x2> <x3> <x4> `

Where [x1, x2] represents the first line and [x3, x4] the second line.
The program will print whether the two lines overlap or not.

## Question B:
> The goal of this question is to write a software library that accepts 2 version strings as input and returns whether one is greater than, equal, or less than the other. As an example: “1.2” is greater than “1.1”. Please provide all test cases you could think of.

This is implemented in the library QB/compare_package/version_compare.py
The program can be run using the __main__.py included in the QB file. To run it the following command can be used:

` python3 -m QB <string1> <string2> `

Where string1 and string2 are the version strings to compare. The program will print whether the first string is older, newer or the same as the second one.
The actual function that compares the strings is in version_compare.py and returns 1, -1 or 0 depending on how the inputs compare to each other.
### Assumptions:
* Version strings consist of numbers seperated by dots. Example: 1.2.5
* Numbers are not treated like decimals but are treated literally. Example: 1.12.5 is newer than 1.2.5
* Padding is valid to add: 1.1.0.0.0.0.0 is the same as 1.1. Similarly, 1.1 is the same as 1.01
* Empty strings, strings with negative numbers or any string that does not follow these rules will cause a ValueError to be raised.

### Testing:
Tests should be run using the following command:

` python3 -m unittest `

When the user is located in the QB directory. 

Alternatively we can run:

`python3 -m unittest QB/compare_package/test_version_compare.py `

Testing was done using the unittest python library. All tests have been run and passed successfully.


## Question C:
> At Ormuco, we want to optimize every bits of software we write. Your goal is to write a new library that can be integrated to the Ormuco stack. Dealing with network issues everyday, latency is our biggest problem. Thus, your challenge is to write a new Geo Distributed LRU (Least Recently Used) cache with time expiration. This library will be used extensively by many of our services so it needs to meet the following criteria:

This library is implemented as QC/cache. lru.py has the actual implementation of the Least Recently Used Cache.
The way I interpreted this question is that we would have multiple servers at different locations, each with their own cache, and a user making a request for a certain item would want that request to be made from the nearest cache/server. 
To simulate this I implemented both the server.py and handler.py classes. The Server class represents a server object (unaware of its geolocation) and the Handler class is a sort of look-up table. When a user makes a request it is made to the handler. The user gives an "id" with information about their location, and the handler will find and return the most appropriate LRU cache. 
Initially, I implemented the handler to return the object without giving information on the cache, but the seemed to defeat the purpose of the user requesting from the nearest server, if the information has to go through a central lookup table anyway.

Now each LRU cache has its own server associated with it. In case of a hit, the LRU will return the item to the user, otherwise, in a miss, it will have to request the item from its assocaited server. Updates are made to the cache regularly of course. Note that this means a server can have multiple caches, but a cache can only have one server (in the current implementation). Additionally the server has no information on the caches that are associated with it.
The cache is implemented as a doubly-linked list (concretly a queue was used) and a hashmap representing which items are currently in the cache and at which index.
Finally time expiration is implemented using a "ticker", which is essentially a daemon thread that is created and begins keeping track of the time in the background when an LRU object is instantiated. At each n time steps (n is called expiry and can be set in __init__) the cache gets cleared; i.e. expires. Being a daemoin thread, it is automatically killed when the process dies (that is the main function ends execution).
But, again, the main implementation is lru.py; server.py and handler.py are really here for the sake of simulation and giving an idea of how this library can be used.

Finally I implemented a number of tests for this library in test_lru.py 
Similarely to QB, if the user is located in the QC directory, they can easily run:

` python3 -m unittest `

To test the cache library.
Testing was done using the unittest python library. All tests have been run and passed successfully.

