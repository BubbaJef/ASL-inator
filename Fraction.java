public class Fraction {
    //you must declare instance variables up here in the context of the class but before the constructor
    private int numerator;
    private int denominator;

    //constructor is called to create this instance of a fraction, but it's also used to initialize state(aka instance variables)
    public Fraction(){
        numerator = 0;
        denominator = 1;
    }

    public int getNumerator(){
        return numerator;
    }
    public void setNumerator(int n){
        numerator = n;
    }
    public int getDenominator(){
        return denominator;
    }
    public void setDenominator(int n){
        if(n!=0) {
            denominator = n;
        }
    }
    public String toString(){
        String s = "";
        s+=numerator+"/"+denominator;
        return s;
    }

    public void reduce(){
        int gcd = 1;
       if(numerator == denominator){
           gcd = 1;
           numerator = 1;
           denominator = 1;
       }
       else if(Math.abs(numerator) > Math.abs(denominator)){
            int i = 2;
            while(i <= Math.abs(denominator)){
                if(denominator % i == 0 & numerator % i == 0){
                    gcd = i;
                }
                i++;
            }

       }
       else if(Math.abs(numerator) < Math.abs(denominator)){
           int i = 2;
           while(i <= Math.abs(numerator)){
               if(numerator % i == 0 & denominator % i == 0){
                   gcd = i;
               }
               i++;
           }

       }
       numerator = numerator / gcd;
       denominator = denominator / gcd;
    }
    public static void main(String[] args){
        Fraction f = new Fraction(); // this is the right way to do it if you get 'cannot access non static method from static context" error
                                    // it means you need to create an instance of this class
        f.setNumerator(-5);
        f.setDenominator(10);
        f.reduce();
        System.out.print(f);
    }
}
