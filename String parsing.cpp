#include <iostream>
using namespace std;

typedef const DELIM "|" 
class Node {
    char c;
    Node * left;
    Node * right;
    Node * next;
    bool endOfString;
}

class Mapper() {
        
    map<string, int> datamap;
    Mapper() {
        datamap["one"] = 1;
        datamap["minus"] = -1;
    }
}
class Trie {
 
    Node *root;
    
    Node * newNode() {
        
    }   
    
    void insert() {
    
    }
    
    int isPresent() {
        // 0 if not Present
        // length of string if present
    }

    
}


int decipher( vector<string> & words ) {
    Mapper m;
    int result = 0;
    int size = words.size();
    
    // [ "one", "|", "two", "three", "|", "minus", "seven" ]
    // [ 1 , | , 2  ,3, |, -1, 7]
    int i = 0;
    while( i < size ) {
        string word = words[ i ]; 
        if( word == DELIM ) {
            i++;
            isNegative = false;
            coninue; 
        } else {
            total_num = 0;
            while( words[ i ] != DELIM ) {
                word = words[ i ];
                int curr_num = m.datamap[ word ];
                if( curr_num == -1 ) {
                    isNegative = true;
                } else {
                    total_num = total_num * 10 + curr_num; // 1
                }
                i++;
            }
            if( isNegative ) {
                result -= total_num; 
                isNegative = false;
            } else {
                result += total_num;
            }
        }
    }
    
    return result;
}

void populate( vector<string> & words ) {
    Trie t;
    int index = 0;
    int lastIndex = -1;
    int result = 0;
    bool isNegative;
    int count = 0;
    while( index < l ) {
        
        int num = 0, curr_num = 0;
        
        int size = t.isPresent( &s[ index ] );
        
        if( size > 0 ) {
            string word = s.substring( index, index + size );
            
            v.push_back( word );
            index += size;

        } else {
            if( count > 0 && v[ count - 1 ] != "|" ) {
                v.push_back( "|" );
                count++;
            }
            index++;
            isNegative = false;
        }
    }
    // "one", "|", "two", "three", "|", "minus", "seven"
}
int main() {
    /*
    
    xyzonekjhfdstwothreekjkjfdminussevenkjfdkd
    1 + 23 + (-7) = 17
    */

    string s = "xyz one kjhfds twothree kjkjfd minus khjfs sevenkjfdkd";
    int l = s.length();
    
    vector<string> words;
    populate( &words );
    decipher( &words );

	return 0;
}
