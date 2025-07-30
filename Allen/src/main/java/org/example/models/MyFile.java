package org.example.models;

import java.util.List;

public class MyFile {
    Inode inode;
    List<Block> blockList;

    public MyFile(String pathname, String inputFileType) {
        this.inode = new Inode(pathname, inputFileType);
    }

    public void setBlocksList(List<Block> blockList) {
        this.blockList = blockList;
    }


}
