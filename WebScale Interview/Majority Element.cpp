#include <bits/stdc++.h>
using namespace std;

void findMajority( vector<int> & arr ) {
	int len = arr.size(); 

	//int len = arr.size();
	if( len <= 0 ) {
	    cout << "No elements present\n\n";
	    return;
	}
	
	unordered_map< int, int > m;
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
	cout << endl << "Maximum occurring element is: " <<  maxElement <<  " occurring for " << max <<
	        " time in array of size "<< len << endl << endl; 
	
}
int main() {
	vector< int > arr;
	
    // NULL case 
    cout  << "NULL case " << endl;
	findMajority( arr );
	
	// Known case
	arr = {1,2,12,12,13,4,5,2,1,1,1,2,2,3,3,4,2,1};
	cout  << "Known case " << endl;
	findMajority( arr );
	
	// Normal case
	arr.clear();
    cout  << "Normal case " << endl;
	for( int i = 0; i < 10; i++ ) {
	    int element = rand() % 10;
	    arr.push_back( element );
	    cout << element << " ";
	}
	findMajority( arr );
	
	
	// Stress case
    cout  << "Stress case " << endl;
	for( int i = 0; i < 9990; i++ ) {
	    int element = rand() % 1000 ;
	    arr.push_back( element );
	    cout << element << " ";
	}
	findMajority( arr );
	return 0;
}
