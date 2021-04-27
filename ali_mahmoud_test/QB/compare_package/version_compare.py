

def version_compare(string1, string2):
    '''
    Here is the function that we will use to compare strings
    It accepts two version strings and returns 1 if s1 > s2, -1 if s1 < s2 and 0 if they are equal
    These are version string, they are numbers seperated by dots, no alphabetic characters are legal here
    This function assumes that the numbers are not the same as decimals but act like integers wrapped in other integers
    A string with empty dots will fail: 1.2..3 for example is not legal, an empty string will also fail
    For example: 1.20 is a newer version than 1.3 unlike in floating point numbers
    '''
    if(not verify_input(string1) or not verify_input(string2)): #verify that our input is correct
        raise ValueError('Invalid input. Version string should be numbers seperated by dots.\nex: 1.5.3')
    version1 = string1.split('.')
    version2 = string2.split('.')
    
    #run for the length of the smaller sized one, in case one is longer
    for i in range(min(len(version1), len(version2))):
        #we will go through and compare each number, in order
        if(int(version1[i]) > int(version2[i])):
            return 1
        elif(int(version2[i]) > int(version1[i])):
            return -1    
    
    #Then, if one version is longer, it is necessarily newer
    #but only if the "extended" part is not all zeroes, which we check using has_padding
    #for example 1.1 and 1.1.0.0.0.0.0.0 , they are of course the same version
    if len(version1) > len(version2) :
        if not has_padding(len(version2), version1): #has_padding will return true if it is only padding at the end
            return 1
    elif len(version2) > len(version1):
        if not has_padding(len(version1), version2):
            return -1               
    return 0  #they're equal



def verify_input(input_string):
    '''
    helper
    verify that the input is correct
    should be numbers seperated by dots
    '''
    string = input_string.split('.') #split into a list
    #everything should be a number now, if not return false
    if False in [x.isdigit() for x in string]:
        return False
    return True              

    

def has_padding(index, string):
    ''' 
    helper
    this function verifies if the string is just made up of "padding" after a certain point
    '''
    for i in range(index, len(string)):
        if(string[i] != '0'):   #this part of the string is NOT just padding and actually has real values
            return False
    return True
