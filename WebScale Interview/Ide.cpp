#include <iostream>
#include <bits/stdc++.h>
using namespace std;

int main() {
	vector<int> arr {1,2,12,12,13,4,5,2,1,1,1,2,2,3,3,4,2,1};
	
	int len = arr.size();
	if( len == 0 ) {
	    return 0;
	}
	
	map< int, int > m;
	int max = INT_MIN, maxElement = INT_MIN;
	
	// Populating the map.
	for( int i = 0; i < len; i++ ) {
	    m[ arr[ i ] ]++;
	    if( m[ arr[ i ] ] >= max ) {
	        max = m[ arr[ i ] ];
	    }
	}
	
	// To take the highest element in map in case of conflict for max.
	for( auto i : m ) {
	    if( i.second == max ) {
	        if( i.first > maxElement ) {
	            maxElement = i.first;
	        }
	    }
	}
	cout << "Maximum occurring element is: " <<  maxElement <<  " occurring for " << max << " time "; 
	
	return 0;
}
