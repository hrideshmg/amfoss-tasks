defmodule Prime do
    def isPrime(number, check) do
        if number == 2 do True
        else
            if rem(number, check) == 0 do False
            else
                # number has no divisors since we have checked all previous values
                if check == (number-1) do
                    True
                # call a recursive function to check all values 
                else
                    isPrime(number, check+1)
                end
            end
        end
    end
    
    def countPrimes(number, limit) do
        # Print number and call recursively if number is prime
        if number <= limit do
            if isPrime(number, 2) == True do 
                IO.puts(number)
                countPrimes(number+1, limit)
            # If number isnt prime only call recursively
            else 
                countPrimes(number+1, limit)
            end
        end
    end
end

num_str = IO.gets("Enter number upto which you want to find primes for: ")
Prime.countPrimes(2, String.to_integer(String.trim(num_str))) # Trim is required to get rid of newline character
