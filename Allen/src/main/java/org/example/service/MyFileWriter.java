package org.example.service;

import org.example.models.Block;
import org.example.models.MyFile;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.Lock;

public class MyFileWriter extends Thread {
    private static final String LINE_DELIMITER = "\n";
    private final int BLOCK_SIZE = 5;
    Lock readLock;
    OutputStream outputStream;
    MyFile myFile;
    String data;
    public MyFileWriter(File file, Lock readLock, String data) {
        this.readLock = readLock;
        this.data = data;
        try {
            outputStream = new FileOutputStream(file.getName(), true);
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
        myFile = new MyFile(file.getName(), "CSV");
    }

    public MyFile getMyFile() {
        return myFile;
    }

    public void run() {
        readLock.lock();

        System.out.println("Starting write ...");

        List<String> lines = List.of(data.split(LINE_DELIMITER));


        List<String> rawRecords = new ArrayList<>();
        List<Block> blockList = new ArrayList<>();

        try (OutputStreamWriter outputStreamWriter = new OutputStreamWriter(outputStream)) {
            int count = 0;
            for (String line : lines) {
                rawRecords.add(line);
                outputStreamWriter.write(line + "\n");
                System.out.println("Wrote line: " + line);

                count++;

                if (count == BLOCK_SIZE) {
                    Block block = new Block(List.copyOf(rawRecords));
                    blockList.add(block);

                    rawRecords.clear();
                    count = 0;
                }
            }
            myFile.setBlocksList(blockList);
        } catch (IOException e) {
            throw new RuntimeException("Unable to write the file", e);
        }
        readLock.unlock();
    }
}
