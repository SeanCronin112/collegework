import java.math.BigInteger;

public class verification {

    static Assignment2 a = new Assignment2();

    public static String K(BigInteger k, BigInteger p){
        if(k.compareTo(BigInteger.ONE) >= 0){
            if(p.subtract(BigInteger.ONE).compareTo(k) >= 1){
                if(a.calculateGCD(k, p.subtract(BigInteger.ONE)).equals(BigInteger.ONE)){
                    return "1 < k < p-1, and gcd(k, p - 1) == 1";
                }
            }
        }
        return "This is not a valid K. Please change.";
    }

    public static String X(BigInteger x, BigInteger p){
        if(x.compareTo(BigInteger.ZERO) >= 0){
            if(p.subtract(BigInteger.ONE).compareTo(x) >= 0){
                return "X is valid.";
            }
        }
        return "X is invalid.";
    }

    public static String R(BigInteger r, BigInteger k, BigInteger p){
        if(r.compareTo(BigInteger.ONE) == 1){
            if(p.subtract(BigInteger.ONE).compareTo(r) == 1){
                return "1 < r < p-1, and gcd(1, p - 1) == 1";
            }
        }
        return "R is invalid.";
    }

    public static String S(BigInteger s, BigInteger p) {
        BigInteger two = new BigInteger("2");
        if(s.compareTo(BigInteger.ONE) >= 1){
            if(p.subtract(two).compareTo(s) >= 1){
                return "1 < r < p-1, and gcd(1, p - 1) == 1";
            }
        }
        return "R is invalid.";
    }


    public static void completeVerification(BigInteger g, BigInteger m, BigInteger p, BigInteger y, BigInteger r, BigInteger s){
        if((BigInteger.ZERO.compareTo(r) == -1) && (r.compareTo(p) == -1)){
            System.out.println("R is within the range 1 to p - 1.");
        } else {
            System.out.println("R is not within the range 1 to p - 1");
        }
        if((BigInteger.ZERO.compareTo(s) == -1) && (s.compareTo(p.subtract(BigInteger.ONE)) == -1)){
            System.out.println("S is within the range of 1 to p - 2");
        } else {
            System.out.println("S is not within the range of 1 to p - 2");
        }
        System.out.println("g^{h(m)} (mod p) == y^r * r^s (mod p): " + verifyElGamal(g, m, p, y, r, s));
    }

    public static boolean verifyElGamal(BigInteger g, BigInteger m, BigInteger p, BigInteger y, BigInteger r, BigInteger s){
        BigInteger LHS = g.modPow(m, p);
        BigInteger RHS = y.modPow(r, p).multiply(r.modPow(s,p)).mod(p);
        return LHS.equals(RHS);
    }}  