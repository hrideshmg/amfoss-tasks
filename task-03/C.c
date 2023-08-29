#include <stdio.h>
#include <stdbool.h>

int main() {
    int limit;
    
    printf("Enter the number upto which you want to find primes for: ");
    scanf("%d", &limit);
    
    for (int number = 2; number <= limit; number++)
    {
        // Assume number is prime until it is proved that it isn't
        bool prime = true;

        for (int check = 2; check < number; check++)
        {
            if (number % check == 0)
            {
                prime = false;
                break;
            }
        }
        
        if (prime) printf("%d\n", number);
    }
    
    
    return 0;
}
