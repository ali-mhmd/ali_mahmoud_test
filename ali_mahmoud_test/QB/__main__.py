'''
Ali Mahmoud
This is our main function and accepts two version strings from the command line
It will print which is newer
'''
from QB.compare_package.version_compare import version_compare
import argparse

def main():
    #accepts two version strings as input on command line and prints which is newer
    parser = argparse.ArgumentParser()
    parser.add_argument('string1')
    parser.add_argument('string2')
    string1 = parser.parse_args().string1
    string2 = parser.parse_args().string2
    comparision = version_compare(string1, string2) #compare the strings
    if comparision == -1:
        print(f'{string1} is older than {string2}')
    elif comparision == 1 :
        print(f'{string1} is newer than {string2}')
    else : #it's equal to 0
        print(f'{string1} and {string2} are the same version strings')        
    
    


if __name__ == '__main__':
    main()