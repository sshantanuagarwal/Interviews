#include <bits/stdc++.h>
using namespace std;

class Node {
    public:
        int data;
        Node *left;
        Node *right;
        
    Node( int value ) {
        this->data = value;
        this->right = NULL;
        this->left = NULL;
        
    }
};

void findPaths( Node *root, int *sum, int *num, int *numPaths ) {
    if( !root ) {
        return;
    }
    *sum += root->data;
    // If leaf node
    if( !root->left && !root->right ) {
        if( *sum == *num ) {
            (*numPaths)++;
        }
    }
    
    findPaths( root->left, sum, num, numPaths );
    findPaths( root->right, sum, num, numPaths );
}

void findNumPaths( Node *root, int num ) {
    if( !root ) {
        
        cout << "The tree is empty." << endl;
        return;
    }
    int sum = 0;
    int numPaths = 0;
    findPaths( root, &sum, &num, &numPaths );
    
    cout << endl << "There are: " << numPaths << " with sum: " << num << endl << endl;
}

Node* insert(Node *root, int value) { 
    if( !root )
        return new Node( value ); 
  
    // Insert data. 
    if( value > root->data ) { 
        root->right = insert(root->right, value); 
    } else { 
        root->left = insert(root->left, value); 
    }
    return root; 
} 

int main() {
    Node *root = NULL;
    
    // NULL case 
    cout  << "NULL case " << endl;
    findNumPaths( root, 0 );
    
    // Normal length:
    cout  << "Normal case " << endl;
    for( int i = 0; i < 10; i++ ) {
        int element = rand() % 10;
        root = insert( root, element );
        cout << element << " ";
    }
    findNumPaths( root, rand() % 10 );
    
    // Stress case:
    cout  << "Stress case " << endl;
    for( int i = 0; i < 9990; i++ ) {
        int element = rand() % 10;
        root = insert( root, element );
        cout << element << " ";
    }
    findNumPaths( root, rand() % 10000 );
}