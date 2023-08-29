fn main() {
    // mut implies that the  variable is mutable
    let mut limit = String::new();
    
    println!("Enter number upto which you want primes for: ");
    std::io::stdin().read_line(&mut limit);
    
    // limit: i32 signifies that the datatype of the variable is a 32 bit signed integer
    // trim() is required to remove any trailing or leading characters
    // parse() converts string to integer, it returns a result enum with either T or E (success or fail)
    // expect extracts the data from result if its a success else prints the custom error message
    let limit: i32 = limit.trim().parse().expect("Enter valid number");
    
    for number in 2..limit+1
    {
        // Assume number is prime until it is proved that it isnt.
        let mut prime = true;
    
        for check in 2..number
        {
            if number % check == 0
            {
                prime = false;
                break;
            }
        }
    
        if prime
        {
            println!("{}", number.to_string())
        }
    }
}
