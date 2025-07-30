# cook your dish here

'''
hello sshantanu
olleh unatnahss
'''

def deliminatorList():
    return [ ' ', '.', '!' ]

def reverse( s ):
    # O (n)
    l = len(s) # "hello unatnahss"
    numIters = l/2
    
    for i in range( numIters ):
        tmp = s[ i ]
        s[ i ] = s[ l - i - 1 ]
        s[ l - i - 1 ] = tmp


def split(s):
    # O(n)
    l = len(s)
    words = []
    start = 0
    for i in range(l):
        if i in deliminatorList()  or i == l - l:
            words.append( s[ start : i+1 ] )
            start = i + 1


def reverseWords( words ):
    # O(n)
    l = len( words )
    numIters = l/2
    for i in range( numIters ): # 3/2 = 1  -> [ 0 ]: i = 0, l - i - 1 = 3 - 0 - 1 - 2
        tmp = words[ i ]
        words[ i ] = words[ l - i - 1 ]
        words[ l - i - 1 ] = tmp
    
'''
main():
    # O( n )
    s = "Hello Sshantanu"
    # reverse whole string
    reverse(s) # unatnahss olleh 
    
    #Split it into words`
    listOfWords = split(s) #[ "unatnahss", "olleh" ], 
    
    # reverse the order of words
    reverseWords( listOfWords ) #[ "olleh", "unatnahss" ]
    
    print( ' '.join( listOfWords ) )
'''


main():
    # O( n )
    s = "Hello Sshantanu"
    # reverse whole string
    reverse(s) # unatnahss olleh 
    
    #Split it into words`
    listOfWords = split( s ) #[ "unatnahss", "olleh" ], 
    
    # reverse the order of words
    reverseWords( listOfWords ) #[ "olleh", "unatnahss" ]
    
    print( ' '.join( listOfWords ) )