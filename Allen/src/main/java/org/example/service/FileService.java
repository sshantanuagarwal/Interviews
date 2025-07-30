package org.example.service;

import org.example.models.MyFile;

import java.util.ArrayList;
import java.util.List;

public class FileService {
    List<MyFile> files;
    MyFile myFile;

    public void createMetadata(String path) {
        files = new ArrayList<>();
        myFile = new MyFile(path, "CSV");
        files.add(myFile);
    }
}
