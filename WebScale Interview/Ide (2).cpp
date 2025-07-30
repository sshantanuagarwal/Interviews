class Node {
    int data;
    Node *left;
    Node *right;
}

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
    
    findPaths( root->left, &sum, &num, &numPaths );
    findPaths( root->right, &sum, &num, &numPaths );
}

int findNumPaths( Node *root, int num ) {
    if( !root )
        return 0;
    int sum = 0;
    int numPaths = 0;
    findNumPaths( root, &sum, &num, &numPaths );
    cout << "There are: " << numPaths << " with sum: " << num;
}