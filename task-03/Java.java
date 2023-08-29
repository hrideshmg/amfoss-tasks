import java.util.Scanner;

class HelloWorld {
    // args is an array of strings containing the command line arguments passed to the program.
    public static void main(String[] args) {
        Scanner myScanner = new Scanner(System.in);
        System.out.print("Enter number upto which you want to find primes for: ");
        int limit = Integer.parseInt(myScanner.nextLine());
        
        for (int number = 2; number <= limit; number++)
        {
            // Assume number is prime until it is proved that it isn't
            boolean prime = true;
            
            for (int check = 2; check < number; check++)
            {
                if (number % check == 0)
                {
                    prime = false;
                    break;
                }
            }
            
            if (prime) System.out.println(number);
        }
    }
}
