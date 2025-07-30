package org.codedesign.ops;

import org.codedesign.models.Board;
import org.codedesign.models.Coordinate;
import org.codedesign.models.Snake;

import javax.naming.directory.InvalidAttributesException;
import java.util.ArrayList;
import java.util.List;

public class SnakeGame {
    private Board board;
    private Snake snake;
    private Long movesCount;
    private boolean gameOver;

    public SnakeGame(int m, int n, int snakeSize) {
        board = new Board(m, n);
        snake = new Snake(m / 2, n / 2, snakeSize);
        movesCount = 0L;
        gameOver = false;
    }

    public boolean isGameOver() {
        return gameOver;
    }

    public void moveSnake(String direction) throws InvalidAttributesException {
        if (gameOver) {
            System.out.println("Game is already over!");
            return;
        }

        Coordinate delta = newMoveDelta(direction);
        movesCount = movesCount + 1;

        // Calculate new head position
        Coordinate newHead = snake.getHead().add(delta);

        // Check if move is valid
        if (!snake.isValidMove(board.getNumRow(), board.getNumCols(), newHead)) {
            gameOver = true;
            System.out.println("Invalid Move, Game over");
            return;
        }

        // Create new position list
        List<Coordinate> snakeNewPosition = new ArrayList<>();
        snakeNewPosition.add(newHead);

        // Add rest of body
        List<Coordinate> currentPosition = snake.getCurrentPosition();
        if (movesCount % 5 == 0) {
            // On growth turns, keep the tail
            snakeNewPosition.addAll(currentPosition);
        } else {
            // On normal turns, remove the tail
            for (int i = 0; i < currentPosition.size() - 1; i++) {
                snakeNewPosition.add(currentPosition.get(i));
            }
        }

        snake.setCurrentPosition(snakeNewPosition);
        snake.setHead(newHead);
        System.out.println(snake);
    }

    private Coordinate newMoveDelta(String direction) throws InvalidAttributesException {
        if (direction.equals("left")) {
            return new Coordinate(-1, 0);
        } else if (direction.equals("right")) {
            return new Coordinate(1, 0);
        } else if (direction.equals("up")) {
            return new Coordinate(0, -1);
        } else if (direction.equals("down")) {
            return new Coordinate(0, 1);
        } else {
            throw new InvalidAttributesException("Incorrect direction");
        }
    }

    public static void main(String[] args) {
        try {
            // Create a 10x10 board with initial snake size of 3
            SnakeGame game = new SnakeGame(10, 10, 3);

            // Test sequence of moves
            String[] moves = { "right", "right", "down", "down", "left", "up" };

            for (String move : moves) {
                System.out.println("\nMoving " + move);
                game.moveSnake(move);
                if (game.isGameOver()) {
                    break;
                }
            }

        } catch (InvalidAttributesException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
