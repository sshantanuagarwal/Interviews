package org.example.ops;


import org.example.models.MyFile;
import org.example.service.MyFileReader;
import org.example.service.MyFileWriter;
import org.junit.Test;

public class FileOpTest {
    FileOp fileOp = new FileOp();

    @Test
    public void testWrite() throws Exception {
        String data = "11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n";

        MyFile file = fileOp.fwrite("/Users/sshantanu/Downloads/myData.csv", data).getMyFile();

//      assert file.getBlocksList().size() == 5;

    }

    @Test
    public void testRead() throws Exception {

        MyFile file = fileOp.fread("/Users/sshantanu/Interviews/Allen/src/test/java/org/example/ops/myData.csv").getMyFile();
//       assert file.getBlocksList().size() == 5;

    }


    @Test
    public void testConcurrentAccess() throws Exception {
        MyFileReader read = fileOp.fread("myData.csv");
        String data = "11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n";
        MyFileWriter write = fileOp.fwrite("myData.csv", data);
        MyFileReader read2 = fileOp.fread("myData.csv");
        read.start();
        write.start();
        read2.start();

        read.join();
        write.join();
        read2.join();
    }


}
