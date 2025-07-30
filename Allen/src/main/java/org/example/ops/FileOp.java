package org.example.ops;

import org.example.service.FileService;
import org.example.service.MyFileReader;
import org.example.service.MyFileWriter;

import java.io.File;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class FileOp implements AutoCloseable {
    File file;
    FileService fileService;
    Lock readLock = new ReentrantLock();
    Lock writeLock = new ReentrantLock();

    public FileOp() {
        fileService = new FileService();
    }

    private void fopen(String pathname) {
        file = new File(pathname);
        fileService.createMetadata(pathname);
    }


    public MyFileReader fread(String pathname) throws InterruptedException {
        fopen(pathname);

        return new MyFileReader(file, writeLock);

    }


    public MyFileWriter fwrite(String pathname, String data) throws InterruptedException {
        fopen(pathname);


        return new MyFileWriter(file, readLock, data);

    }


    private void fclose() {
        try {
            close();
        } catch (Exception e) {
            throw new RuntimeException("Unable to close file", e);
        }

    }

    @Override
    public void close() throws Exception {
    }
}
