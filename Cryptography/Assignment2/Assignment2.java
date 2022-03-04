import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.math.BigInteger;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class Assignment2 implements Assignment2Interface{
    
    public BigInteger p = new BigInteger("b59dd79568817b4b9f6789822d22594f376e6a9abc0241846de426e5dd8f6eddef00b465f38f509b2b18351064704fe75f012fa346c5e2c442d7c99eac79b2bc8a202c98327b96816cb8042698ed3734643c4c05164e739cb72fba24f6156b6f47a7300ef778c378ea301e1141a6b25d48f1924268c62ee8dd3134745cdf7323", 16);
    public BigInteger g = new BigInteger("44ec9d52c8f9189e49cd7c70253c2eb3154dd4f08467a64a0267c9defe4119f2e373388cfa350a4e66e432d638ccdc58eb703e31d4c84e50398f9f91677e88641a2d2f6157e2f4ec538088dcf5940b053c622e53bab0b4e84b1465f5738f549664bd7430961d3e5a2e7bceb62418db747386a58ff267a9939833beefb7a6fd68", 16);
    public BigInteger x = new BigInteger("13d04bc3ffde59d45824ef4c27b0ab6b74c45261ac2c94498d3e349e36951e3e4399f295e97d4dc5206c1ffdfff29487e57a628c1ab05d15314c31e52bec5baa4c7b2a8e1e12dcb7233ec838ab1e8d21b113c1b8f855a75b6e9c4b19fb27c1757f8d1277b27848a0b3504ff5aba9af13928661497dc441df1015546c1a922c11", 16);
    public BigInteger k = new BigInteger("afe2f717bda5fda7cf6e56ad9f12a5234f0566565f5eeca23c25e018be4063d83d7ed0a40a2e879513bd5be1eba0bb9b8026866fd7432a9c2a87b62abafca61b1fb751b6f470bb6a1e0a24c6ff58fdc03a5f534b523c2be335a623d817d304b3a80e319e08a0277b01288c613c3b8bb1938e72bb35deb714c9fc569dd7128341", 16);

    public BigInteger generateY(BigInteger generator, BigInteger secretKey, BigInteger modulus){
       
        BigInteger y = generator.modPow(secretKey, modulus);
        try {
            FileWriter writerY = new FileWriter("y.txt");
            writerY.write(y.toString(16));
            writerY.close();
        } catch (IOException e) {
            System.out.println("File not found");
        }
        return y;
    }


    public BigInteger generateR(BigInteger generator, BigInteger k, BigInteger modulus){
        BigInteger r = generator.modPow(k, modulus);
        
        try {
            FileWriter writerR = new FileWriter("r.txt");
            writerR.write(r.toString(16));
            writerR.close();
        } catch (IOException e) {
            System.out.println("File not found.");
        }

        return r;
    }

    public BigInteger generateS(byte[] plaintext, BigInteger secretKey, BigInteger r, BigInteger k, BigInteger modulus){
        //xr

        BigInteger m = hashMessageBigInt(plaintext);
        BigInteger xr = secretKey.multiply(r);
        //H(m)
        //Initial Bracket = (h(m) - xr) mod p - 1

        BigInteger initialBracket = m.subtract(xr);
        BigInteger mulInverse = calculateInverse(k, modulus.subtract(BigInteger.ONE));
        BigInteger finalValues = (initialBracket.multiply(mulInverse)).mod(modulus.subtract(BigInteger.ONE));

        try {
            FileWriter writerS = new FileWriter("s.txt");
            writerS.write(finalValues.toString(16));
            writerS.close();
        } catch (IOException e) {
            System.out.println("File not found.");
        }
        return finalValues;

    }

    public BigInteger calculateGCD(BigInteger x, BigInteger y) {
    
        BigInteger xModY = x.mod(y);
        if (xModY.equals(BigInteger.ZERO)){
            return y;
        }
        return calculateGCD(y, xModY);
    }

    //calculateInverse calls upon a recursive function, which returns a list of three numbers. Then, the modular value of the middle item in this list is returned,
    // which is equal to the modular inverse. For demonstration, take the example of trying to find the multiplicative inverse of 67 mod 119. 
    public BigInteger calculateInverse(BigInteger val, BigInteger modulus){
        return calculateInverseRecursive(val, modulus)[0].mod(modulus);
    }

    //This recursive function takes in the two initial values, val and modulus. 
    public static BigInteger[] calculateInverseRecursive(BigInteger val, BigInteger modulus){
        //If the modulus is equal to zero, then it means that the base case has been reached. In the example, the value would be 1, because the step before 
        //this would be 1 (mod 7) = 0, so the list would be {1,1,0}
        if(modulus.equals(BigInteger.ZERO)){
            return new BigInteger[] {BigInteger.ONE, BigInteger.ZERO};
        }

        //Working up recursively, the list would go: {1,0}, {0,1}, {1,-2}, {-2,7}, {7,-9}, {-9, 16}, until we get to the end where 16 is the multiplicative inverse
        //of 67 mod 119. 
        BigInteger[] currentValues = calculateInverseRecursive(modulus, val.mod(modulus));
        BigInteger a = currentValues[0];
        BigInteger b = currentValues[1];
        //The value [1] (or the right hand side) of the list is moved to the left, and the right hand side becomes the number that 67 is multiplied by different
        //steps during the extended Euclidean GCD. This process can be found in the notes, at https://loop.dcu.ie/pluginfile.php/3737947/mod_resource/content/3/1.7.html
        currentValues[0] = b;
        BigInteger smallest = val.divide(modulus).multiply(b);
        currentValues[1] = a.subtract(smallest);
        return currentValues;
    }

    //Helper Function to convert InputFile into Bytes
    public static byte[] convertInputFileToBytes(String input) throws IOException {
        byte[] fileBytes = new byte[0];
        try {
            Path inputFile = Paths.get(input);
            fileBytes = Files.readAllBytes(inputFile);
        } catch (FileNotFoundException e) {
            System.out.println("File not found.");
        }
        return fileBytes;
    }

    //Helper Function to convert a Byte Array into a hashed byte array, and then return a BigInteger of this value
    public static BigInteger hashMessageBigInt(byte[] inputFile){
		byte[] messageBytes = new byte[0];
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
			messageBytes = md.digest(inputFile);
        } catch (NoSuchAlgorithmException e) {
            System.out.println("No such algorithm.");
        }
			return new BigInteger(messageBytes);

	}
    public static void main(String [] args) throws NoSuchAlgorithmException, IOException {

        Assignment2 a = new Assignment2();
        
        BigInteger p = a.p;
        BigInteger g = a.g;
        BigInteger x = a.x;
        BigInteger k = a.k;        
        try {

            String encryptedFile = args[0];
            Path path = Paths.get(System.getProperty("user.dir") + "/" + encryptedFile);
            byte[] fileBytes = Files.readAllBytes(path);

            BigInteger hashedFileBigInt = hashMessageBigInt(fileBytes);
            BigInteger y = a.generateY(g, x, p);
            BigInteger r = a.generateR(g, k, p);
            BigInteger s = a.generateS(fileBytes, x, r, k, p);
            
            verification.completeVerification(g, hashedFileBigInt, p, y, r, s);
        } catch (Exception e) {
            System.out.println("Error reading file.");
        }  
    }
}