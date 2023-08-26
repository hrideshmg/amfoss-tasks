// Online C++ compiler to run C++ program online
#include <iostream>
using namespace std;

int main() {
    int limit;
    
    cout << "Enter number upto which you want to find primes for: ";
    cin >> limit;
    
    for (int number = 2; number <= limit; number++)
    {
        // Assume number is prime until its proved that it isn't
        bool prime = true;
        
        for (int check = 2; check < number; check++)
        {
            
            if (number % check == 0)
            {
                prime = false;
                break;
            }
        }
        
        if (prime) cout << number << endl;
    }
    
    return 0;
}
