package org.codedesign.models;

import java.util.ArrayList;
import java.util.List;

public class Snake {
    List<Coordinate> currentPosition;
    Coordinate head;

    /*
     * [
     * 
     * ---
     * 
     * ]
     */
    public Snake(int x, int y, int snakeSize) {
        currentPosition = new ArrayList<>();
        head = new Coordinate(x, y);
        currentPosition.add(head);

        for (int i = 1; i < snakeSize; i++) {
            currentPosition.add(new Coordinate(x - i, y));
        }
    }

    public List<Coordinate> getCurrentPosition() {
        return currentPosition;
    }

    public void setCurrentPosition(List<Coordinate> currentPosition) {
        this.currentPosition = currentPosition;
    }

    public Coordinate getHead() {
        return head;
    }

    public Boolean isValidMove(int numRows, int numCols, Coordinate newMove) {
        if (currentPosition.contains(newMove)) {
            return false;
        }
        if (newMove.getX() < 0 || newMove.getX() >= numRows || newMove.getY() < 0 || newMove.getY() >= numCols) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "Snake{" +
                "currentPosition=" + currentPosition +
                ", head=" + head +
                ", size= " + currentPosition.size() +
                '}';
    }

    public void setHead(Coordinate head1) {
        this.head = head1;
    }
}
