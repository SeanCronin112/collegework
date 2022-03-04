import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.*;
import java.io.*;
import java.math.BigInteger;
import java.util.Base64;
import java.security.*;
import java.util.Scanner;
import java.util.Random;
import java.util.Arrays;
import javax.crypto.*;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import javax.xml.namespace.QName;

public class Assignment1 implements Assignment1Interface{

    public static byte[] encodePassword(String password){
        byte[] encodedPassword = password.getBytes(StandardCharsets.UTF_8);
        return encodedPassword;
    }

    public static String convertByteToHex (byte[] byteArray){
        String hexString = "";
        for (byte by : byteArray){
            hexString += String.format("%02X", by);
        }
        return hexString;
    };


    //generateSalt and generateIV functions instantiate byte arrays of length 16, fills them with random bytes, outputs it to the salt.txt/IV.txt files, and returns them to the user. 
    public static byte[] generateSalt() throws FileNotFoundException, IOException {
        byte[] saltBytes = new byte[16];
        Random random = new SecureRandom();
        random.nextBytes(saltBytes);
        BufferedWriter saltToFile = new BufferedWriter(new FileWriter("salt.txt"));
        saltToFile.write(convertByteToHex(saltBytes));
        saltToFile.close();
        return saltBytes;
    }

    public static byte[] generateIV() throws FileNotFoundException, IOException{
        byte[] IVbytes = new byte[16];
        Random random = new SecureRandom();
        random.nextBytes(IVbytes);
        BufferedWriter IVToFile = new BufferedWriter(new FileWriter("IV.txt"));
        IVToFile.write(convertByteToHex(IVbytes));
        IVToFile.close();
        return IVbytes;
    };

    //GenerateKey function combines the password and salt into one byte array, combinedPasswordAndSalt.
    //It then hashes this byte array 200 times with SHA-256, and returns this hash value to the user. 
    public byte[] generateKey(byte[] password, byte[] salt){
        byte[] combinedPasswordAndSalt = new byte[(password.length + salt.length)];
        System.arraycopy(password, 0, combinedPasswordAndSalt, 0, password.length);
        System.arraycopy(salt, 0, combinedPasswordAndSalt, password.length, salt.length);

        MessageDigest mDigest = null;
        byte[] hashedPasswordAndSalt = combinedPasswordAndSalt;
        try {
            mDigest = MessageDigest.getInstance("SHA-256");
            int i = 0;
            while(i < 200) {
                hashedPasswordAndSalt = mDigest.digest(hashedPasswordAndSalt);
                i++;
            }
        } catch (Exception e) {
            System.out.print(e.getCause());
        }
        return hashedPasswordAndSalt;
    }

    /*PadInput function determines the length of the files with all full block sizes, and the difference between this value and the length of the input. 
    It then adds onto the input by filling it with padding, initially byte -128, which is (1000-0000), and then the rest zeroes to fill it up.
    Given that we're dealing in bytes and not bits, it's not necessary to do the padding at a bit level. 
    The padded input is then returned to the user.
    */
    public static byte[] padInput(byte[] stringBytes){
        int correctLengthOfBytes = stringBytes.length + (16 - (stringBytes.length % 16));
        byte[] paddedInput = new byte[correctLengthOfBytes];
        System.arraycopy(stringBytes, 0, paddedInput, 0, stringBytes.length);
        paddedInput[stringBytes.length] = (byte) -128;
        int i = stringBytes.length + 1;
        while(i < correctLengthOfBytes){
            paddedInput[i] = (byte) 0;
            i++;
        }
        
        return paddedInput;
    }
    
    //RemovePadding looks at the last bytes of the text, and kind of removes the padding.
    //IT will still be there, but the '1000-0000' will be replaced with '0000-0000', making it useless.
    public static byte[] removePadding(byte[] plainTextBytes){
        int i = plainTextBytes.length - 1;
        while (i > 0){
            if(plainTextBytes[i] == (byte) -128){
                plainTextBytes[i] = (byte) 0;
                break;
            }
            i--;
        }
        return plainTextBytes;
    }

    /*
    EncryptAES initally calls on the padInput function to pad the input, then creates IVParameterSpec and SecretKey which are needed for AES encryption. 
    It creates IVParameterSpec IV and SecretKey which are needed for AES Encryption. Finally, it carries out the encryption using the Java library for it. 
    */
    public  byte[] encryptAES(byte[] plaintext, byte[] iv, byte[] secretkey) {
        byte[] paddedMessage = padInput(plaintext);
        try {
            IvParameterSpec IV = new IvParameterSpec(iv);
            SecretKey key = new SecretKeySpec(secretkey, "AES");
            Cipher encryptor = Cipher.getInstance("AES/CBC/NoPadding");
            encryptor.init(Cipher.ENCRYPT_MODE, key, IV);

            byte[] cipherBytes = encryptor.doFinal(paddedMessage);
            return cipherBytes;
        } catch (Exception e) {
            System.out.println(e.getLocalizedMessage());
            return plaintext;
        }
    }

    //decryptAES operates in a very similar manner then encrypting in AES, the same parameters are used, but instead of padding at the start, it 'removes' the padding at the end.
    public byte[] decryptAES(byte[] ciphertext, byte[] iv, byte[] key)  {
        try {    
            IvParameterSpec IV = new IvParameterSpec(iv);
            SecretKeySpec aesKey = new SecretKeySpec(key, "AES");
            Cipher decryptor = Cipher.getInstance("AES/CBC/NoPadding");
            decryptor.init(Cipher.DECRYPT_MODE, aesKey, IV);
            
            byte[] plainTextBytes = decryptor.doFinal(ciphertext);
            byte[] plainTextBytesNoPadding = removePadding(plainTextBytes);
            return plainTextBytes;
        } catch (Exception e) {
            System.out.println(e.getLocalizedMessage());
            return ciphertext;
        }
    }
    
    //encryptRSA takes an unencrypted password, and carries out RSA encryption, using the modExp function I created below. 
    //It returns the encrypted byte array to the user. 
    public byte[] encryptRSA(byte[] plaintext, BigInteger exponent, BigInteger modulus){
        byte[] encryptedRSA = null;
        BigInteger plainTextBigInteger = new BigInteger(plaintext);
        BigInteger completedModExp = modExp(plainTextBigInteger, exponent, modulus);
        encryptedRSA = completedModExp.toByteArray();

        return encryptedRSA;
    }


    //ModExp works with the SquareToMultiply algorithm to carry out modular exponentiation on the plaintext, to the power of the exponent (65537 in this case) and the modulus of public key. 
    public BigInteger modExp(BigInteger plainText, BigInteger exponent, BigInteger modulus){
        BigInteger currentValue = new BigInteger("1");
        int i = 0;
        while (i < exponent.bitLength()){
            if (exponent.testBit(i)){
                currentValue = currentValue.multiply(plainText).mod(modulus);
            }
            plainText = plainText.multiply(plainText).mod(modulus);
            i++;
        }
        return plainText;
    }

    public static void main(String[] args) throws GeneralSecurityException, IOException{
        Assignment1 assignment = new Assignment1();

        BigInteger exponent = new BigInteger("65537");
        BigInteger modulus = new BigInteger("c406136c12640a665900a9df4df63a84fc855927b729a3a106fb3f379e8e4190ebba442f67b93402e535b18a5777e6490e67dbee954bb02175e43b6481e7563d3f9ff338f07950d1553ee6c343d3f8148f71b4d2df8da7efb39f846ac07c865201fbb35ea4d71dc5f858d9d41aaa856d50dc2d2732582f80e7d38c32aba87ba9", 16);

        byte[] salt = generateSalt();
        byte[] IV = generateIV();

        String password = "E:#supp7cuYUA,ED";
        byte[] encodedPassword = encodePassword(password);

        byte[] encryptedPassword = assignment.encryptRSA(encodedPassword, exponent, modulus);

        String encryptedPasswordString = convertByteToHex(encryptedPassword);

        byte[] key = assignment.generateKey(encryptedPassword, salt);

        BufferedWriter passwordToFile = new BufferedWriter(new FileWriter("Password.txt"));
        System.out.println(encryptedPasswordString);
        passwordToFile.write(encryptedPasswordString);
        passwordToFile.close();

        try {
            String encryptedFile = args[0];
            Path path = Paths.get(System.getProperty("user.dir") + "/" + encryptedFile);
            byte[] fileBytes = Files.readAllBytes(path);
            byte[] encryptedText = assignment.encryptAES(fileBytes, IV, key);
            byte[] decryptedText = assignment.decryptAES(encryptedText, IV, key);

            String encryptedTextString = new String(encryptedText, StandardCharsets.UTF_8);
            String decryptedTextString = new String(decryptedText, StandardCharsets.UTF_8);

            System.out.println(convertByteToHex(encryptedText));

        } catch (Exception e) {
            System.out.println("Error reading file.");
        }
    }
}