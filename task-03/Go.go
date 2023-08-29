package main
import "fmt"

func main() {
  var limit int
  
  fmt.Print("Enter number upto which you want to calculate primes for: ")
  fmt.Scan(&limit)
  
  for number := 2; number <= limit; number++ {
    // Assume number is prime until it is proved that it isn't
    var prime bool = true  
    
        for check := 2; check < number; check++ {
            if number % check == 0 {
                prime = false
                break
            }
        }
        
        if prime {
            println(number)
        }
  }
}
