package org.codedesign.models;

import java.util.ArrayList;
import java.util.List;

public class Board {
    // m*n size
    List<List<Integer>> board; // Deprecate
    int numRows;
    int numCols;

    public Board(int m, int n) {
        /*
        [0,0
         0,0]
         */
        this.numRows = m;
        this.numCols = n;
        this.board = new ArrayList<>();
        for(int i = 0; i < m; i++) {
            List<Integer> row = new ArrayList<>();
            for (int j = 0; j < n; j++) {
                row.add(0);
            }
            board.add(row);
        }
    }


    public List<List<Integer>> getBoard() {
        return board;
    }

    public void setBoard(List<List<Integer>> board) {
        this.board = board;
    }

    public int getNumRow() {
        return this.numRows;
    }
    public int getNumCols() {
        return this.numCols;
    }
}
