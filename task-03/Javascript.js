let limit = parseInt(prompt("Enter number upto which you want to find primes for: "));

for (let number = 2; number <= limit; number++) 
{
    // Assume number is prime until its proved that it isn't
    let prime = true;
    
    for (let check = 2; check < number; check++)
    {
        if (number % check == 0)
        {
            prime = false;
            break;
        }
    }
    
    if (prime)
    {
        console.log(number);
    }
}
