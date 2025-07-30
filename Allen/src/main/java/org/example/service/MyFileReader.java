package org.example.service;


import org.example.models.Block;
import org.example.models.MyFile;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.Lock;

public class MyFileReader extends Thread {
    private final int BLOCK_SIZE = 2;
    Lock writeLock;
    InputStream inputStream;
    MyFile myFile;

    public MyFileReader(File file, Lock writeLock) {
        this.writeLock = writeLock;
        try {
            inputStream = new FileInputStream(file);
        } catch (FileNotFoundException e) {
            throw new RuntimeException("File not found at the path: " + file.getName());
        }
        myFile = new MyFile(file.getName(), "CSV");
    }

    public MyFile getMyFile() {
        return myFile;
    }

    @Override
    public void run() {
        writeLock.lock();

        System.out.println("Starting reading ...");

        try (BufferedReader br = new BufferedReader(new InputStreamReader(inputStream))) {
            String line;
            int count = 0;

            List<Block> blockList = new ArrayList<>();
            List<String> rawRecords = new ArrayList<>();
            while ((line = br.readLine()) != null) {
                rawRecords.add(line);
                System.out.println("Read line: " + line);
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
            throw new RuntimeException("Unable to read file", e);
        }
        writeLock.unlock();
    }

}