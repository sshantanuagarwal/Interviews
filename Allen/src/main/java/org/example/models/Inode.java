package org.example.models;


public class Inode {

    private final String fileName;
    private final InputFileType inputFileType;

    public Inode(String pathname, String inputFileType) {
        this.fileName = pathname;
        this.inputFileType = InputFileType.valueOf(String.valueOf(inputFileType));
    }
    enum InputFileType {
        Text,
        CSV
    }

}
