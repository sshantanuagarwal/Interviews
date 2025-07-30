# cook your dish here


arr = [ 10, 20, 30, 40, 11, 50 ]
s = 70
# O(n^2)
l = len( arr )
count = 0
for i in range( 1, l ):
    for j in range( i ):
        tmpSum = sum(arr[ j:i ] )
        if( tmpSum == s ):
            count += 1
            
#O(n)
start = 0
curr = arr[ start ]
count = 0
while( i < l ):
    '''
            10, 20, 30, 40, 20, 50
    curr  = 10  30  60  100 90  70 40 20 110 70 
    counnt                       1
    
    
    
            10, 20, 30, 40, 30, 20, 50
    curr  = 10  30  60  100 90  70 100 70 
    count                        1      2
    
    '''
    #Case 1        
    while( curr > s and start < i  ):
        curr -= arr[ start ]
        start += 1
    

    #Case 2
    if( curr == s ):
        count += 1
        curr -= arr[ start ]
        start += 1
        
    #Case 3
    if( i < l ):
        curr += arr[ i ]
    
    i += 1
        
if not count:
    print( "No such sub-arrays possible." )
else:
    print( count, "sub arrays exist with sum =", s)