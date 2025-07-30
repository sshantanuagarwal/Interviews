package org.codedesign.ops;

import junit.framework.TestCase;

import javax.naming.directory.InvalidAttributesException;

public class SnakeGameTest extends TestCase {

    public void testName() throws Exception {
        SnakeGame snakeGame = new SnakeGame(10,10, 3);

        snakeGame.moveSnake("right");
        snakeGame.moveSnake("right");
        snakeGame.moveSnake("right");

        snakeGame.moveSnake("right");
        snakeGame.moveSnake("right");
    }
}