# Ali Mahmoud
import argparse
import sys


def main():
    '''
    Most of the main function is just preprocessing and checking arguments
    These should be passed in as POSITIONAL arguments, x1 x2 x3 x4
    To form lines [x1, x2] and [x3, x4]
    For example in the terminal: $ python3 QA.py 1 2 3 4
    Here line1 is [1,2] and line2 is [3,4]
    Arguments must: be floats/int and must be valid lines (first number cannot be greater than second for each line)
    '''
    parser = argparse.ArgumentParser() #the lines will be passed in as positional arguments
    parser.add_argument('x1', type=float) 
    parser.add_argument('x2', type=float)
    parser.add_argument('x3', type=float)
    parser.add_argument('x4', type=float)
    if len(sys.argv) != 5:  #not the right number of arguments passed
        raise ValueError('Four numbers should be passed in as arguments')
    #lines will be [x1, x2] and [x3,x4]  
    x1 = float(parser.parse_args().x1)
    x2 = float(parser.parse_args().x2)
    x3 = float(parser.parse_args().x3)
    x4 = float(parser.parse_args().x4)
    if(x1 > x2 or x3 > x4):  #check that the lines are valid
        raise ValueError('The lines are not valid. For each line the first argument cannot be greater than the second.')
    overlap = check_overlap(x1, x2, x3, x4)
    if overlap:
        print(f'Lines ({x1}, {x2}) and ({x3}, {x4}) do overlap.')
    else:
        print(f'Lines ({x1}, {x2}) and ({x3}, {x4}) do not overlap.')


def check_overlap(x1, x2, x3, x4):
    '''
    This is where we compute the actual answer
    What we can check is if they do not overlap, this would be easier to do
    '''  
    if(x3 > x2 or x1 > x4): #if this is the case, then they don't overlap
        return False
    return True   
    



if __name__ == '__main__':
    main()    