package kaesl;

import java.security.*;
import javax.crypto.*;
import javax.crypto.spec.*;

import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
import javax.swing.filechooser.FileFilter;

import java.util.Arrays;
import java.io.*;
import java.util.concurrent.*;

import java.nio.file.*;
import java.nio.charset.StandardCharsets;

class bytearray { // 2GB 보다 작은 바이트 어레이
    byte[] data;
    public bytearray(){} // 인자 없는 생성

    public bytearray(int bytelen){ // 임의의 길이만큼 0으로 초기화
        this.data = new byte[bytelen];
        Arrays.fill(this.data, (byte) 0);
    }

    public bytearray(String strin){ // 문자열에서 utf-8 인코딩
        this.data = strin.getBytes(StandardCharsets.UTF_8);
    }

    void fromString(String strin){ // 문자열에서 utf-8 인코딩
        this.data = strin.getBytes(StandardCharsets.UTF_8);
    }

    void initByte(int bytelen){ // 임의의 길이만큼 0으로 초기화
        this.data = new byte[bytelen];
        Arrays.fill(this.data, (byte) 0);
    }

    void randByte(int bytelen){ // 임의의 길이만큼 난수로 초기화
        SecureRandom s = new SecureRandom();
        this.data = new byte[bytelen];
        s.nextBytes(this.data);
    }

    void addByteFront(byte[] bytein){ // 앞쪽에 바이트 배열 추가
        byte[] temp = new byte[this.data.length + bytein.length];
        System.arraycopy(bytein, 0, temp, 0, bytein.length);
        System.arraycopy(this.data, 0, temp, bytein.length, this.data.length);
        this.data = temp;
    }

    void addByteBack(byte[] bytein){ // 뒤쪽에 바이트 배열 추가
        byte[] temp = new byte[this.data.length + bytein.length];
        System.arraycopy(this.data, 0, temp, 0, this.data.length);
        System.arraycopy(bytein, 0, temp, this.data.length, bytein.length);
        this.data = temp;
    }

    String readData(){ // 바이트 에레이를 16진법으로 출력
        String temp = "";
        for (int i = 0; i < this.data.length; i++){
            temp = temp + String.format("%02X ", data[i]);
        }
        return temp;
    }
}

class engine{
    // padding, unpadding
    private byte[] padding(byte[] data) {
        int paddingLength = 16 - (data.length % 16);
        byte paddingByte = (byte) paddingLength;

        byte[] paddedData = new byte[data.length + paddingLength];
        System.arraycopy(data, 0, paddedData, 0, data.length);
        for (int i = data.length; i < paddedData.length; i++) {
            paddedData[i] = paddingByte;
        }

        return paddedData;
    }
    private byte[] unpadding(byte[] paddedData) {
        int paddingLength = paddedData[paddedData.length - 1] & 0xFF;
        byte[] unpaddedData = new byte[paddedData.length - paddingLength];
        System.arraycopy(paddedData, 0, unpaddedData, 0, unpaddedData.length);

        return unpaddedData;
    }

    // delete file
    public void delete (String target, int mode) throws Exception{ // target : file path, mode : int
        Path fpath = Paths.get(target);
        long fsize = Files.size(fpath); // file size

        if (mode == 0){ // normal delete
            long num0 = fsize / 1048576;
            long num1 = fsize % 1048576;

            FileOutputStream f = new FileOutputStream(target);
            bytearray temp = new bytearray(1048576);
            for (long i = 0; i < num0; i++){
                f.write( temp.data );
                if (i % 10 == 0){
                    test374.mygui.statuslbl.setText( String.format("<html>deleting<br>%d/%d</html>",i,num0) );
                }
            }

            temp.initByte( (int) num1 );
            f.write( temp.data );
            test374.mygui.statuslbl.setText( String.format("<html>deleting<br>%d/%d</html>",num0,num0) );
            f.close();
            Files.delete(fpath);
        }
        else{ // secure delete
            long num0 = fsize / 1024;
            long num1 = fsize % 1024;

            FileOutputStream f = new FileOutputStream(target);
            bytearray temp = new bytearray();
            for (long i = 0; i < (num0 / 100); i++){
                temp.randByte(1024);
                for (int j = 0; j < 100; j++){
                    f.write(temp.data);
                }
                if (i % 100 == 0){
                    test374.mygui.statuslbl.setText( String.format("<html>deleting<br>%d/%d</html>",i * 100,num0) );
                }
            }

            temp.randByte(1024);
            for (long i = 0; i < (num0 % 100); i++){
                f.write(temp.data);
            }

            temp.randByte( (int) num1 );
            f.write(temp.data);
            f.close();
            test374.mygui.statuslbl.setText( String.format("<html>deleting<br>%d/%d</html>",num0,num0) );
            Files.delete(fpath);
        }
    }

    // files -> tempkaesl
    public void dozip(String[] targets) throws Exception{
        int num = targets.length;
        FileOutputStream f = new FileOutputStream("./tempkaesl");
        f.write( new byte[] { (byte) (num % 256), (byte) (num / 256) } );

        for (int i = 0; i < num; i++){
            String fname = targets[i];
            String tempname = fname.replaceAll("\\\\","/");
            tempname = tempname.substring( tempname.lastIndexOf("/") + 1 ); // file name
            bytearray namebyte = new bytearray(tempname);
            int tempnum = namebyte.data.length; // file name size
            f.write( new byte[] { (byte) (tempnum % 256), (byte) (tempnum / 256) } );
            f.write(namebyte.data);

            File file = new File(fname);
            long fsize = file.length(); // file size
            long tempsize = fsize;
            byte[] tempbyte = new byte[8];
            for (int j = 0; j < 8; j++) {
                tempbyte[j] = (byte) (tempsize % 256);
                tempsize = tempsize / 256;
            }
            f.write(tempbyte);

            long num0 = fsize / 1048576;
            long num1 = fsize % 1048576;
            FileInputStream t = new FileInputStream(fname);
            byte[] buffer = new byte[1048576];
            for (long j = 0; j < num0; j++){
                t.read(buffer);
                f.write(buffer);
            }
            buffer = new byte[ (int) num1 ];
            t.read(buffer);
            f.write(buffer);
            t.close();
            test374.mygui.statuslbl.setText( String.format("<html>zipping<br>%d/%d</html>",i+1,num) );
        }

        f.close();
    }
    
    // tempkaesl -> path + files
    public void unzip(String path) throws Exception{ // path : folder path
        path = path.replaceAll("\\\\", "/");
        if ( path.equals("") ){
            path = "./";
        } else{
            if (path.substring(path.length() - 1) != "/"){
                path = path + "/";
            }
        }

        FileInputStream f = new FileInputStream("tempkaesl");
        byte[] buffer = new byte[2];
        f.read(buffer);
        int num = (buffer[0] & 0xFF) + (buffer[1] & 0xFF) * 256;

        for (int i = 0; i < num; i++){
            buffer = new byte[2];
            f.read(buffer);
            int namelen = (buffer[0] & 0xFF) + (buffer[1] & 0xFF) * 256;
            buffer = new byte[namelen];
            f.read(buffer);
            String namestr = new String(buffer, StandardCharsets.UTF_8);

            long filesize = 0;
            long multi = 1;
            buffer = new byte[8];
            f.read(buffer);
            for (int j = 0; j < 8; j++){
                filesize = filesize + ( (buffer[j] & 0xFF) * multi );
                if (j != 7){
                    multi = multi * 256;
                }
            }

            long num0 = filesize / 1048576;
            long num1 = filesize % 1048576;
            FileOutputStream t = new FileOutputStream(path + namestr);
            buffer = new byte[1048576];
            for (long j = 0; j < num0; j++){
                f.read(buffer);
                t.write(buffer);
            }
            buffer = new byte[ (int) num1 ];
            f.read(buffer);
            t.write(buffer);

            t.close();
            test374.mygui.statuslbl.setText( String.format("<html>unzipping<br>%d/%d</html>",i+1,num) );
        }

        f.close();
    }

    // key expand inline
    public bytearray inline0(bytearray pre, bytearray sub) throws Exception{
        MessageDigest digest = MessageDigest.getInstance("SHA3-256");
        for (int i = 0; i < 10000; i++){
            sub.addByteFront(pre.data);
            sub.data = digest.digest(sub.data);
        }
        return sub;
    }

    // key expand function
    public bytearray[] expandkey(bytearray ckey) throws Exception{ // ckey : bytearray
        bytearray[] order = new bytearray[16];
        bytearray[] out = new bytearray[32];
        ExecutorService ex = Executors.newFixedThreadPool(16);

        for (int i = 0; i < 16; i++){
            bytearray pre = new bytearray();
            bytearray sub = new bytearray();
            int temp = (7 * i) % 16; // round st point
            if (temp > 8){
                pre.data = Arrays.copyOfRange(ckey.data, 8*temp-64, 8*temp);
                sub.data = Arrays.copyOfRange(ckey.data, 8*temp, ckey.data.length);
                sub.addByteBack( Arrays.copyOfRange(ckey.data, 0, 8*temp-64) );
            } else{
                pre.data = Arrays.copyOfRange(ckey.data, 8*temp+64, ckey.data.length);
                pre.addByteBack( Arrays.copyOfRange(ckey.data, 0, 8*temp) );
                sub.data = Arrays.copyOfRange(ckey.data, 8*temp, 8*temp+64);
            }
            order[i] = ex.submit( () -> inline0(pre, sub) ).get();
        }
        ex.shutdown();

        for (int i = 0; i < 16; i++){
            bytearray temp = order[i];
            bytearray hash0 = new bytearray();
            bytearray hash1 = new bytearray();
            hash0.data = Arrays.copyOfRange(temp.data, 0, 16);
            hash1.data = Arrays.copyOfRange(temp.data, 16, 32);
            out[i] = hash0;
            out[i + 16] = hash1;
        }
        return out;
    }

    // short encryption no padding, 16B * n
    public bytearray inline1(bytearray key, bytearray iv, bytearray indata) throws Exception{ // key : bytearray, iv : bytearray, data : bytearray
        Cipher cipher = Cipher.getInstance("AES/CBC/NoPadding");
        SecretKeySpec secretKey = new SecretKeySpec(key.data, "AES");
        IvParameterSpec ivSpec = new IvParameterSpec(iv.data);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, ivSpec);
        bytearray out = new bytearray();
        out.data = cipher.doFinal(indata.data);
        return out;
    }

    // enc, dec common class var
    int count;
    ExecutorService ex = Executors.newFixedThreadPool(1);

    // encrypt(tempkaesl) -> move to path, 32 process
    public void encrypt32(String hint, String pw, String path) throws Exception{ // hint : str, pw : str, path : file path
        bytearray salt = new bytearray();
        salt.randByte(32); // salt bytearray

        bytearray ckey = new bytearray();
        ckey.randByte(128); // content key bytearray

        bytearray iv = new bytearray();
        iv.randByte(16); // iv bytearray

        MessageDigest digest = MessageDigest.getInstance("SHA3-256");
        bytearray pwhash = new bytearray(pw); // pwh bytearray
        for (int i = 0; i < 100000; i++){
            pwhash.addByteFront(salt.data);
            pwhash.data = digest.digest(pwhash.data);
        }
        bytearray mkey = new bytearray(pw); // master key bytearray
        for (int i = 0; i < 10000; i++){
            mkey.addByteBack(salt.data);
            mkey.data = digest.digest(mkey.data);
        }

        bytearray hintbyte = new bytearray(hint); // hint bytearray
        int hintsize = hintbyte.data.length;

        bytearray enckey = new bytearray();
        bytearray enciv = new bytearray();
        enckey.data = Arrays.copyOfRange(mkey.data, 16, 32);
        enciv.data = Arrays.copyOfRange(mkey.data, 0, 16);
        bytearray ckeydata = inline1(enckey, enciv, ckey);

        bytearray header = new bytearray("OTE1"); // header bytearray
        header.addByteBack( new byte[] { (byte) (hintsize % 256), (byte) (hintsize / 256) } );
        header.addByteBack(hintbyte.data);
        header.addByteBack(salt.data);
        header.addByteBack(pwhash.data);
        header.addByteBack(ckeydata.data);
        header.addByteBack(iv.data);

        bytearray[] keys = expandkey(ckey); // 16B * 32 keys bytearray[]
        bytearray[] ivs = new bytearray[32];
        Arrays.fill(ivs, iv); // 16B * 32 ivs bytearray[]
        File file = new File("tempkaesl");
        long filesize = file.length(); // target size
        long chunknum0 = filesize / 131072; // chunk num
        long chunknum1 = filesize % 131072; // left size

        FileOutputStream f = new FileOutputStream(path);
        FileInputStream t = new FileInputStream("tempkaesl");

        f.write(header.data);
        test374.mygui.statuslbl.setText("<html>encrypting<br>header</html>");
        // bytearray[] order = new bytearray[32];
        bytearray[] write = new bytearray[32];
        ex = Executors.newFixedThreadPool(32);
        count = 0; // iv, key position
        bytearray voidarray = new bytearray(0);

        byte[] buffer = new byte[131072];
        byte[] tempwrite = new byte[4194304];
        for (long i = 0; i < chunknum0; i++){
            t.read(buffer); // 128kb
            if ( (i + 1) % 100 == 0 ){
                test374.mygui.statuslbl.setText( String.format("<html>encrypting<br>%d/%d</html>", i + 1, chunknum0 + 1) );
            }
            bytearray tempdata = new bytearray();
            tempdata.data = buffer;
            write[count] = ex.submit( () -> inline1(keys[count], ivs[count], tempdata) ).get(); // order[count]

            if (count == 31){
                ex.shutdown();
                ex = Executors.newFixedThreadPool(32);
                for (int j = 0; j < 32; j++){
                    // write[j] = order[j];
                    bytearray tempiv = new bytearray();
                    tempiv.data = Arrays.copyOfRange(write[j].data, 131056, 131072);
                    ivs[j] = tempiv;
                    System.arraycopy(write[j].data, 0, tempwrite, 131072 * j, 131072);
                }
                f.write(tempwrite);
                count = -1;
                // Arrays.fill(order, voidarray);
                Arrays.fill(write, voidarray);
            }
            count = count + 1;
        }

        if (chunknum0 % 32 != 0){
            ex.shutdown();
            tempwrite = new byte[ 131072 * ( (int) chunknum0 % 32) ];
            for (int i = 0; i < chunknum0 % 32; i++){
                // write[i] = order[i];
                bytearray tempiv = new bytearray();
                tempiv.data = Arrays.copyOfRange(write[i].data, 131056, 131072);
                ivs[i] = tempiv;
                System.arraycopy(write[i].data, 0, tempwrite, 131072 * i, 131072);
            }
            f.write(tempwrite);
        }
        // f.write(tempwrite);

        buffer = new byte[ (int) chunknum1 ];
        t.read(buffer);
        bytearray lastwrite = new bytearray();
        lastwrite.data = padding(buffer);
        lastwrite = inline1(keys[count], ivs[count], lastwrite);
        f.write(lastwrite.data);
        test374.mygui.statuslbl.setText( String.format("<html>encrypting<br>%d/%d</html>", chunknum0 + 1, chunknum0 + 1) );

        t.close();
        f.close();
    }

    // encrypt(tempkaesl) -> move to path, n process
    public void encryptn(String hint, String pw, String path, int core) throws Exception{ // hint : str, pw : str, path : file path, core : int
        bytearray salt = new bytearray();
        salt.randByte(32); // salt bytearray

        bytearray ckey = new bytearray();
        ckey.randByte(128); // content key bytearray

        bytearray iv = new bytearray();
        iv.randByte(16); // iv bytearray

        MessageDigest digest = MessageDigest.getInstance("SHA3-256");
        bytearray pwhash = new bytearray(pw); // pwh bytearray
        for (int i = 0; i < 100000; i++){
            pwhash.addByteFront(salt.data);
            pwhash.data = digest.digest(pwhash.data);
        }
        bytearray mkey = new bytearray(pw); // master key bytearray
        for (int i = 0; i < 10000; i++){
            mkey.addByteBack(salt.data);
            mkey.data = digest.digest(mkey.data);
        }

        bytearray hintbyte = new bytearray(hint); // hint bytearray
        int hintsize = hintbyte.data.length;

        bytearray enckey = new bytearray();
        bytearray enciv = new bytearray();
        enckey.data = Arrays.copyOfRange(mkey.data, 16, 32);
        enciv.data = Arrays.copyOfRange(mkey.data, 0, 16);
        bytearray ckeydata = inline1(enckey, enciv, ckey);

        bytearray header = new bytearray("OTE1"); // header bytearray
        header.addByteBack( new byte[] { (byte) (hintsize % 256), (byte) (hintsize / 256) } );
        header.addByteBack(hintbyte.data);
        header.addByteBack(salt.data);
        header.addByteBack(pwhash.data);
        header.addByteBack(ckeydata.data);
        header.addByteBack(iv.data);

        bytearray[] keys = expandkey(ckey); // 16B * 32 keys bytearray[]
        bytearray[] ivs = new bytearray[32];
        Arrays.fill(ivs, iv); // 16B * 32 ivs bytearray[]
        File file = new File("tempkaesl");
        long filesize = file.length(); // target size
        long chunknum0 = filesize / 131072; // chunk num
        long chunknum1 = filesize % 131072; // left size

        FileOutputStream f = new FileOutputStream(path);
        FileInputStream t = new FileInputStream("tempkaesl");

        f.write(header.data);
        test374.mygui.statuslbl.setText("<html>encrypting<br>header</html>");
        bytearray[] order = new bytearray[core];
        bytearray[] write = new bytearray[32];
        ex = Executors.newFixedThreadPool(core);
        count = 0; // iv, key position
        bytearray voidarray = new bytearray(0);
        Arrays.fill(order, voidarray);
        Arrays.fill(write, voidarray);

        byte[] buffer = new byte[131072];
        byte[] tempwrite = new byte[4194304];
        for (long i = 0; i < chunknum0; i++){
            t.read(buffer); // 128kb
            if ( (i + 1) % 100 == 0 ){
                test374.mygui.statuslbl.setText( String.format("<html>encrypting<br>%d/%d</html>", i + 1, chunknum0 + 1) );
            }
            bytearray tempdata = new bytearray();
            tempdata.data = buffer;
            order[count % core] = ex.submit( () -> inline1(keys[count], ivs[count], tempdata) ).get(); // order[count]

            if (count % core == core - 1){
                ex.shutdown();
                ex = Executors.newFixedThreadPool(core);
                for (int j = 0; j < core; j++){
                    write[count - core + 1 + j] = order[j];
                    bytearray tempiv = new bytearray();
                    tempiv.data = Arrays.copyOfRange(write[count - core + 1 + j].data, 131056, 131072);
                    ivs[count - core + 1 + j] = tempiv;
                }
            }
            
            if (count == 31){
                for (int j = 0; j < 32; j++){
                    System.arraycopy(write[j].data, 0, tempwrite, 131072 * j, 131072);
                }
                f.write(tempwrite);
                count = -1;
                Arrays.fill(order, voidarray);
                Arrays.fill(write, voidarray);
            }
            count = count + 1;
        }

        if (chunknum0 % core != 0){
            ex.shutdown();
            for (int i = 0; i < chunknum0 % core; i++){
                write[ (int) (count - (chunknum0 % core) + i) ] = order[i];
                bytearray tempiv = new bytearray();
                tempiv.data = Arrays.copyOfRange(write[ (int) (count - (chunknum0 % core) + i) ].data, 131056, 131072);
                ivs[ (int) (count - (chunknum0 % core) + i) ] = tempiv;
            }
        }
        if (chunknum0 % 32 != 0){
            bytearray tempdata = new bytearray(0);
            tempdata.data = write[0].data;
            for (int i = 1; i < 32; i++){
                if (write[i].data != null){
                    tempdata.addByteBack(write[i].data);
                }
            }
            f.write(tempdata.data);
        }

        buffer = new byte[ (int) chunknum1 ];
        t.read(buffer);
        bytearray lastwrite = new bytearray();
        lastwrite.data = padding(buffer);
        lastwrite = inline1(keys[count], ivs[count], lastwrite);
        f.write(lastwrite.data);
        test374.mygui.statuslbl.setText( String.format("<html>encrypting<br>%d/%d</html>", chunknum0 + 1, chunknum0 + 1) );

        t.close();
        f.close();
    }

    // short decryption no padding, 16B * n
    public bytearray inline2(bytearray key, bytearray iv, bytearray indata) throws Exception{ // key : bytearray, iv : bytearray, data : bytearray
        Cipher cipher = Cipher.getInstance("AES/CBC/NoPadding");
        SecretKeySpec secretKey = new SecretKeySpec(key.data, "AES");
        IvParameterSpec ivSpec = new IvParameterSpec(iv.data);
        cipher.init(Cipher.DECRYPT_MODE, secretKey, ivSpec);
        bytearray out = new bytearray();
        out.data = cipher.doFinal(indata.data);
        return out;
    }

    // decrypt(file) -> tempkaesl, 32 process
    public void decrypt32(String target, String pw) throws Exception{ //target : file path, pw : str
        FileInputStream f = new FileInputStream(target);
        byte[] buffer = new byte[4];
        f.read(buffer);
        buffer = new byte[2];
        f.read(buffer);
        int hintnum = (buffer[0] & 0xFF) + (buffer[1] & 0xFF) * 256;
        byte[] hintbyte = new byte[hintnum];
        f.read(hintbyte);
        buffer = new byte[32];
        f.read(buffer);
        bytearray saltbyte = new bytearray();
        saltbyte.data = buffer; // salt bytearray 32B
        buffer = new byte[32];
        f.read(buffer);
        bytearray pwhash = new bytearray();
        pwhash.data = buffer; // pwhash bytearray 32B
        buffer = new byte[128];
        f.read(buffer);
        bytearray ckeydata = new bytearray();
        ckeydata.data = buffer; // ckeydata bytearray 128B
        buffer = new byte[16];
        f.read(buffer);
        bytearray iv = new bytearray();
        iv.data = buffer; // iv bytearray 128B

        MessageDigest digest = MessageDigest.getInstance("SHA3-256");
        bytearray mkey = new bytearray(pw); // master key bytearray
        for (int i = 0; i < 10000; i++){
            mkey.addByteBack(saltbyte.data);
            mkey.data = digest.digest(mkey.data);
        }

        bytearray enckey = new bytearray();
        bytearray enciv = new bytearray();
        enckey.data = Arrays.copyOfRange(mkey.data, 16, 32);
        enciv.data = Arrays.copyOfRange(mkey.data, 0, 16);
        bytearray ckey = inline2(enckey, enciv, ckeydata); // content key bytearray

        bytearray[] keys = expandkey(ckey); // 16B * 32 keys bytearray[]
        bytearray[] ivs = new bytearray[32];
        Arrays.fill(ivs, iv); // 16B * 32 ivs bytearray[]
        File file = new File(target);
        long filesize = file.length() - hintnum - 214; // actual file size
        long chunknum0 = filesize / 131072; // chunk num
        long chunknum1 = filesize % 131072; // left size
        if (chunknum1 == 0){
            chunknum0 = chunknum0 - 1;
            chunknum1 = 131072;
        }

        FileOutputStream t = new FileOutputStream("tempkaesl");
        test374.mygui.statuslbl.setText("<html>decrypting<br>header</html>");
        // bytearray[] order = new bytearray[32];
        bytearray[] write = new bytearray[32];
        ex = Executors.newFixedThreadPool(32);
        count = 0; // iv, key position
        bytearray voidarray = new bytearray(0);

        buffer = new byte[131072];
        byte[] tempwrite = new byte[4194304];
        for (long i = 0; i < chunknum0; i++){
            f.read(buffer); // 128kb
            if ( (i + 1) % 100 == 0 ){
                test374.mygui.statuslbl.setText( String.format("<html>decrypting<br>%d/%d</html>", i + 1, chunknum0 + 1) );
            }
            bytearray tempdata = new bytearray();
            tempdata.data = buffer;
            write[count] = ex.submit( () -> inline2(keys[count], ivs[count], tempdata) ).get(); // order[count]
            bytearray tempiv = new bytearray();
            tempiv.data = Arrays.copyOfRange(tempdata.data, 131056, 131072);
            ivs[count] = tempiv;

            if (count == 31){
                ex.shutdown();
                ex = Executors.newFixedThreadPool(32);
                for (int j = 0; j < 32; j++){
                    // write[j] = order[j];
                    System.arraycopy(write[j].data, 0, tempwrite, 131072 * j, 131072);
                }
                t.write(tempwrite);
                count = -1;
                // Arrays.fill(order, voidarray);
                Arrays.fill(write, voidarray);
            }
            count = count + 1;
        }

        if (chunknum0 % 32 != 0){
            ex.shutdown();
            tempwrite = new byte[ 131072 * ( (int) chunknum0 % 32) ];
            for (int i = 0; i < chunknum0 % 32; i++){
                // write[i] = order[i];
                System.arraycopy(write[i].data, 0, tempwrite, 131072 * i, 131072);
            }
            t.write(tempwrite);
        }
        // f.write(tempwrite);

        buffer = new byte[ (int) chunknum1 ];
        f.read(buffer);
        bytearray lastwrite = new bytearray();
        lastwrite.data = buffer;
        lastwrite = inline2(keys[count], ivs[count], lastwrite);
        lastwrite.data = unpadding(lastwrite.data);
        t.write(lastwrite.data);
        test374.mygui.statuslbl.setText( String.format("<html>decrypting<br>%d/%d</html>", chunknum0 + 1, chunknum0 + 1) );

        t.close();
        f.close();
    }

    // decrypt(file) -> tempkaesl, n process
    public void decryptn(String target, String pw, int core) throws Exception{ //target : file path, pw : str
        FileInputStream f = new FileInputStream(target);
        byte[] buffer = new byte[4];
        f.read(buffer);
        buffer = new byte[2];
        f.read(buffer);
        int hintnum = (buffer[0] & 0xFF) + (buffer[1] & 0xFF) * 256;
        byte[] hintbyte = new byte[hintnum];
        f.read(hintbyte);
        buffer = new byte[32];
        f.read(buffer);
        bytearray saltbyte = new bytearray();
        saltbyte.data = buffer; // salt bytearray 32B
        buffer = new byte[32];
        f.read(buffer);
        bytearray pwhash = new bytearray();
        pwhash.data = buffer; // pwhash bytearray 32B
        buffer = new byte[128];
        f.read(buffer);
        bytearray ckeydata = new bytearray();
        ckeydata.data = buffer; // ckeydata bytearray 128B
        buffer = new byte[16];
        f.read(buffer);
        bytearray iv = new bytearray();
        iv.data = buffer; // iv bytearray 128B

        MessageDigest digest = MessageDigest.getInstance("SHA3-256");
        bytearray mkey = new bytearray(pw); // master key bytearray
        for (int i = 0; i < 10000; i++){
            mkey.addByteBack(saltbyte.data);
            mkey.data = digest.digest(mkey.data);
        }

        bytearray enckey = new bytearray();
        bytearray enciv = new bytearray();
        enckey.data = Arrays.copyOfRange(mkey.data, 16, 32);
        enciv.data = Arrays.copyOfRange(mkey.data, 0, 16);
        bytearray ckey = inline2(enckey, enciv, ckeydata); // content key bytearray

        bytearray[] keys = expandkey(ckey); // 16B * 32 keys bytearray[]
        bytearray[] ivs = new bytearray[32];
        Arrays.fill(ivs, iv); // 16B * 32 ivs bytearray[]
        File file = new File(target);
        long filesize = file.length() - hintnum - 214; // actual file size
        long chunknum0 = filesize / 131072; // chunk num
        long chunknum1 = filesize % 131072; // left size
        if (chunknum1 == 0){
            chunknum0 = chunknum0 - 1;
            chunknum1 = 131072;
        }

        FileOutputStream t = new FileOutputStream("tempkaesl");
        test374.mygui.statuslbl.setText("<html>decrypting<br>header</html>");
        bytearray[] order = new bytearray[core];
        bytearray[] write = new bytearray[32];
        ex = Executors.newFixedThreadPool(core);
        count = 0; // iv, key position
        bytearray voidarray = new bytearray(0);
        Arrays.fill(order, voidarray);
        Arrays.fill(write, voidarray);

        buffer = new byte[131072];
        byte[] tempwrite = new byte[4194304];
        for (long i = 0; i < chunknum0; i++){
            f.read(buffer); // 128kb
            if ( (i + 1) % 100 == 0 ){
                test374.mygui.statuslbl.setText( String.format("<html>decrypting<br>%d/%d</html>", i + 1, chunknum0 + 1) );
            }
            bytearray tempdata = new bytearray();
            tempdata.data = buffer;
            order[count % core] = ex.submit( () -> inline2(keys[count], ivs[count], tempdata) ).get(); // order[count]
            bytearray tempiv = new bytearray();
            tempiv.data = Arrays.copyOfRange(tempdata.data, 131056, 131072);
            ivs[count] = tempiv;

            if (count % core == core - 1){
                ex.shutdown();
                ex = Executors.newFixedThreadPool(core);
                for (int j = 0; j < core; j++){
                    write[count - core + 1 + j] = order[j];
                }
            }
            
            if (count == 31){
                for (int j = 0; j < 32; j++){
                    System.arraycopy(write[j].data, 0, tempwrite, 131072 * j, 131072);
                }
                t.write(tempwrite);
                count = -1;
                Arrays.fill(order, voidarray);
                Arrays.fill(write, voidarray);
            }
            count = count + 1;
        }

        if (chunknum0 % core != 0){
            ex.shutdown();
            for (int i = 0; i < chunknum0 % core; i++){
                write[ (int) (count - (chunknum0 % core) + i) ] = order[i];
            }
        }
        if (chunknum0 % 32 != 0){
            bytearray tempdata = new bytearray(0);
            tempdata.data = write[0].data;
            for (int i = 1; i < 32; i++){
                if (write[i].data != null){
                    tempdata.addByteBack(write[i].data);
                }
            }
            t.write(tempdata.data);
        }

        buffer = new byte[ (int) chunknum1 ];
        f.read(buffer);
        bytearray lastwrite = new bytearray();
        lastwrite.data = buffer;
        lastwrite = inline2(keys[count], ivs[count], lastwrite);
        lastwrite.data = unpadding(lastwrite.data);
        t.write(lastwrite.data);
        test374.mygui.statuslbl.setText( String.format("<html>decrypting<br>%d/%d</html>", chunknum0 + 1, chunknum0 + 1) );

        t.close();
        f.close();
    }

    // valid pw check
    public boolean check(byte[] salt, String pw, byte[] pwhash) throws Exception{ // salt : byte[], pw : str, pwhash : byte[]
        MessageDigest digest = MessageDigest.getInstance("SHA3-256");
        bytearray newhash = new bytearray(pw); // new pwh bytearray
        for (int i = 0; i < 100000; i++){
            newhash.addByteFront(salt);
            newhash.data = digest.digest(newhash.data);
        }
        return Arrays.equals(pwhash, newhash.data);
    }

    // valid file check, get pwhs
    public bytearray[] view(String target) throws Exception{ // target : file path
        bytearray[] out = new bytearray[4];
        FileInputStream f = new FileInputStream(target);
        byte[] buffer = new byte[4];
        f.read(buffer);
        if ( Arrays.equals( buffer, new byte[] {79, 84, 69, 49} ) ){
            bytearray b0 = new bytearray();
            b0.data = new byte[] {0};
            out[0] = b0;

            buffer = new byte[2];
            f.read(buffer);
            int hintnum = (buffer[0] & 0xFF) + (buffer[1] & 0xFF) * 256;
            buffer = new byte[hintnum];
            f.read(buffer);
            bytearray b1 = new bytearray();
            b1.data = buffer;
            out[1] = b1;

            buffer = new byte[32];
            f.read(buffer);
            bytearray b2 = new bytearray();
            b2.data = buffer; // salt bytearray 32B
            out[2] = b2;

            buffer = new byte[32];
            f.read(buffer);
            bytearray b3 = new bytearray();
            b3.data = buffer; // pwhash bytearray 32B
            out[3] = b3;

        } else{
            bytearray b0 = new bytearray();
            b0.data = new byte[] {1};
            out[0] = b0;
        }
        f.close();
        return out;
    }

    // main engine
    public String mainengine(String[] enfiles, String defile, String hint, String pw0, String pw1, int core, boolean del0, boolean del1) throws Exception{
        String stout = "complete";
        String outpath = "./"; // 출력 폴더
        int delmode = 0; // 삭제 모드
        if (del1){
            delmode = 1;
        }

        if (enfiles.length != 0){
            if ( pw0.equals(pw1) ){
                String name = String.valueOf( (int)(Math.random()*9000) + 1000 );
                name = outpath + "kaesl" + name + ".ote";
                dozip(enfiles);
                if (core == 32){
                    encrypt32(hint, pw0, name);
                } else{
                    encryptn(hint, pw0, name, core);
                }
                delete("./tempkaesl", delmode);
                if (del0){
                    for (int i = 0; i < enfiles.length; i++){
                        delete(enfiles[i], delmode);
                    }
                }
                stout = "complete : " + name;
            } else{
                stout = "complete : PW not match";
            }

        } else{
            if (defile.length() != 0){
                bytearray[] res = view(defile);
                if (res[0].data[0] == 0){
                    if ( check(res[2].data, pw0, res[3].data) ){
                        if (core == 32){
                            decrypt32(defile, pw0);
                        } else{
                            decryptn(defile, pw0, core);
                        }
                        String name = String.valueOf( (int)(Math.random()*9000) + 1000 );
                        name = outpath + "kaesl" + name + "/";
                        File Folder = new File(name);
                        if ( !Folder.exists() ){
                            Folder.mkdir();
                        }
                        unzip(name); // 새 폴더가 생성됨 주의
                        delete("./tempkaesl", delmode);
                        if (del0){
                            delete(defile, delmode);
                        }
                        stout = "complete : " + name;
                    } else{
                        stout = "complete : Not Valid PW";
                    }
                } else{
                    stout = "complete : Not Valid OTE";
                }

            } else{
                stout = "complete : Nothing";
            }
        }
        return stout;
    }
}

public class test374 {
    static String[] enfiles = new String[] {}; // 파일들
    static String defile = ""; // 파일
    static String status = "idle"; // 현재 상태
    static boolean isworking = false; // 작업 진행중?

    static class FileExtensionFilter extends FileFilter {
        private String description;
        private String extension;

        public FileExtensionFilter(String description, String extension) {
            this.description = description;
            this.extension = extension;
        }

        @Override
        public boolean accept(File file) {
            if (file.isDirectory()) {
                return true;
            }
            String fileExtension = getFileExtension(file);
            return fileExtension != null && fileExtension.equalsIgnoreCase(extension);
        }

        @Override
        public String getDescription() {
            return description + " (*." + extension + ")";
        }

        private String getFileExtension(File file) {
            String fileName = file.getName();
            int dotIndex = fileName.lastIndexOf('.');
            if (dotIndex > 0 && dotIndex < fileName.length() - 1) {
                return fileName.substring(dotIndex + 1).toLowerCase();
            }
            return null;
        }
    }

    static class mygui extends JFrame{
        static JLabel lbl0;
        static JLabel lbl1;
        static JLabel hintlbl;
        static JLabel statuslbl;

        mygui(){
            setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            setTitle("test434");
            this.setLayout(null);
            setSize(400,600);

            JButton btn0 = new JButton("EN"); // 파일들 가져오기
            btn0.setFont( new Font("consolas", Font.BOLD, 20) );
            btn0.addActionListener( new ActionListener() {
                public void actionPerformed(ActionEvent arg0){

                    JFileChooser fileChooser = new JFileChooser(); // 파일 선택창
                    fileChooser.setMultiSelectionEnabled(true);
                    fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
                    int result = fileChooser.showOpenDialog(btn0);

                    if (result == JFileChooser.APPROVE_OPTION) { // 선택 완료시
                        enfiles = new String[fileChooser.getSelectedFiles().length];
                        int i = 0;
                        for ( java.io.File file : fileChooser.getSelectedFiles() ) {
                            enfiles[i] = ( file.getAbsolutePath() );
                            i = i + 1;
                        }
                        lbl0.setText( String.format("(%d) %s", i, enfiles[0]) );
                        defile = "";
                        lbl1.setText("(0) -");
                        hintlbl.setText("");
                    }

                }
            } );
            btn0.setBounds(5, 10, 70, 30);
            this.add(btn0);

            JButton btn1 = new JButton("DE"); // 파일 가져오기
            btn1.setFont( new Font("consolas", Font.BOLD, 20) );
            btn1.addActionListener( new ActionListener() {
                public void actionPerformed(ActionEvent arg0){
                    
                    JFileChooser fileChooser = new JFileChooser(); // 파일 선택창
                    fileChooser.setMultiSelectionEnabled(false);
                    fileChooser.setFileFilter( new FileExtensionFilter("OTE Files", "ote") );
                    fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
                    int result = fileChooser.showOpenDialog(btn1);

                    if (result == JFileChooser.APPROVE_OPTION) { // 선택 완료시
                        defile = fileChooser.getSelectedFile().getAbsolutePath();
                        lbl1.setText( String.format("(%d) %s", 1, defile) );
                        enfiles = new String[] {};
                        lbl0.setText("(0) -");

                        engine work = new engine();
                        try{
                            bytearray[] res = work.view(defile);
                            if (res[0].data[0] == 0){
                                hintlbl.setText( new String(res[1].data) );
                            } else{
                                hintlbl.setText("Warning : Not Valid OTE File");
                            }
                        } catch (Exception e){
                            // System.out.println(e); for debuging
                            StringWriter sw = new StringWriter();
                            e.printStackTrace( new PrintWriter(sw) );
                            String exstr = sw.toString().replace("\\n", "");
                            String output = "<html>";
                            int line = 1;
                            int count = 0;
                            while( (line < 4) & ( count < exstr.length() ) ){
                                output = output + exstr.substring(count, count + 1);
                                count = count + 1;
                                if (count % 25 == 0){
                                    output = output + "<br>";
                                    line = line + 1;
                                }
                            }
                            output = output + "</html>";
                            statuslbl.setText(output);
                            hintlbl.setText("");
                        }
                    }

                }
            } );
            btn1.setBounds(5, 50, 70, 30);
            this.add(btn1);

            lbl0 = new JLabel("(0) -"); // en files
            lbl0.setFont( new Font("Arial Unicode MS", Font.BOLD, 20) );
            lbl0.setBounds(80, 0, 300, 50);
            this.add(lbl0);

            lbl1 = new JLabel("(0) -"); // de file
            lbl1.setFont( new Font("Arial Unicode MS", Font.BOLD, 20) );
            lbl1.setBounds(80, 40, 300, 50);
            this.add(lbl1);

            JPanel panel0 = new JPanel( new GridLayout(1, 0) );
            JLabel lbl2 = new JLabel("core");
            lbl2.setFont( new Font("consolas", Font.BOLD, 20) );
            panel0.add(lbl2);
            JRadioButton rbtn0 = new JRadioButton("4");
            JRadioButton rbtn1 = new JRadioButton("8");
            JRadioButton rbtn2 = new JRadioButton("16");
            JRadioButton rbtn3 = new JRadioButton("32");
            ButtonGroup rbtng = new ButtonGroup();
            rbtn0.setFont( new Font("consolas", Font.BOLD, 20) );
            rbtn1.setFont( new Font("consolas", Font.BOLD, 20) );
            rbtn2.setFont( new Font("consolas", Font.BOLD, 20) );
            rbtn3.setFont( new Font("consolas", Font.BOLD, 20) );
            rbtng.add(rbtn0);
            rbtng.add(rbtn1);
            rbtng.add(rbtn2);
            rbtng.add(rbtn3);
            panel0.add(rbtn0);
            panel0.add(rbtn1);
            panel0.add(rbtn2);
            panel0.add(rbtn3);
            rbtn1.setSelected(true);
            panel0.setBounds(5, 100, 370, 50);
            this.add(panel0);

            JLabel lbl3 = new JLabel("hint");
            lbl3.setFont( new Font("consolas", Font.BOLD, 20) );
            lbl3.setBounds(5, 160, 50, 30);
            this.add(lbl3);
            JLabel lbl4 = new JLabel("hint");
            lbl4.setFont( new Font("consolas", Font.BOLD, 20) );
            lbl4.setBounds(5, 200, 50, 30);
            this.add(lbl4);

            hintlbl = new JLabel("-");
            hintlbl.setFont( new Font("Arial Unicode MS", Font.BOLD, 18) );
            hintlbl.setBounds(60, 155, 340, 30);
            this.add(hintlbl);

            JTextField hintin = new JTextField(); // 힌트 입력 텍스트창
            hintin.setFont( new Font("Arial Unicode MS", Font.PLAIN, 18) );
            hintin.setBounds(60, 200, 320, 30);
            this.add(hintin);

            JLabel lbl5 = new JLabel(" pw ");
            lbl5.setFont( new Font("consolas", Font.BOLD, 20) );
            lbl5.setBounds(5, 260, 50, 30);
            this.add(lbl5);
            JLabel lbl6 = new JLabel(" pw ");
            lbl6.setFont( new Font("consolas", Font.BOLD, 20) );
            lbl6.setBounds(5, 300, 50, 30);
            this.add(lbl6);

            JPasswordField pwin0 = new JPasswordField();
            pwin0.setFont( new Font("Arial Unicode MS", Font.PLAIN, 18) );
            pwin0.setBounds(60, 260, 320, 30);
            this.add(pwin0);
            JPasswordField pwin1 = new JPasswordField();
            pwin1.setFont( new Font("Arial Unicode MS", Font.PLAIN, 18) );
            pwin1.setBounds(60, 300, 320, 30);
            this.add(pwin1);

            JCheckBox chk0 = new JCheckBox("원본 삭제"); // 원본 삭제 여부 체크
            chk0.setFont( new Font("Arial Unicode MS", Font.BOLD, 20) );
            chk0.setBounds(5, 350, 110, 50);
            this.add(chk0);
            JCheckBox chk1 = new JCheckBox("고급 삭제"); // 고급 삭제 여부 체크
            chk1.setFont( new Font("Arial Unicode MS", Font.BOLD, 20) );
            chk1.setBounds(130, 350, 110, 50);
            this.add(chk1);

            JButton btn2 = new JButton("G O"); // 변환 진행 버튼
            btn2.setFont( new Font("consolas", Font.BOLD, 20) );
            btn2.addActionListener( new ActionListener() {
                public void actionPerformed(ActionEvent arg0){

                    engine work = new engine();
                    try{
                        if (! isworking){
                            isworking = true;
                            int core = 32;
                            if ( rbtn0.isSelected() ){
                                core = 4;
                            }
                            if ( rbtn1.isSelected() ){
                                core = 8;
                            }
                            if ( rbtn2.isSelected() ){
                                core = 16;
                            }
                            String str0 = String.valueOf( pwin0.getPassword() );
                            String str1 = String.valueOf( pwin1.getPassword() );
                            statuslbl.setText( work.mainengine(enfiles, defile, hintin.getText(), str0, str1, core, chk0.isSelected(), chk1.isSelected() ) );
                            str0 = "";
                            str1 = "";
                            if ( chk0.isSelected() ){
                                enfiles = new String[] {};
                                lbl0.setText("(0) -");
                                defile = "";
                                lbl1.setText("(0) -");
                            }
                        }
                    }
                    catch(Exception e){
                        // System.out.println(e); for debuging
                        StringWriter sw = new StringWriter();
                        e.printStackTrace( new PrintWriter(sw) );
                        String exstr = sw.toString().replace("\\n", "");
                        String output = "<html>";
                        int line = 1;
                        int count = 0;
                        while( (line < 4) & ( count < exstr.length() ) ){
                            output = output + exstr.substring(count, count + 1);
                            count = count + 1;
                            if (count % 25 == 0){
                                output = output + "<br>";
                                line = line + 1;
                            }
                        }
                        output = output + "</html>";
                        statuslbl.setText(output);
                    }
                    isworking = false;

                }
            } );
            btn2.setBounds(280, 360, 70, 30);
            this.add(btn2);

            statuslbl = new JLabel("idle"); // status label
            statuslbl.setFont( new Font("consolas", Font.BOLD, 20) );
            statuslbl.setBounds(5, 390, 290, 150);
            this.add(statuslbl); // 여러줄 표현은 <html>Line 1<br>Line 2<br>Line 3</html>

            setVisible(true);
        }
    }
    public static void main(String[] args) throws Exception {
        File file = new File("./tempkaesl");
        if ( file.exists() ){
            Files.delete( Paths.get("./tempkaesl") );
        }
        new mygui();
        if ( file.exists() ){
            Files.delete( Paths.get("./tempkaesl") );
        }
    }
}
