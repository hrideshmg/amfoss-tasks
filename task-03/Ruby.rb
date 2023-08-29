print "Enter number upto which you want to find primes for: "
STDOUT.flush # Flushing output so that prompt text appears before input
limit = gets.to_i

for number in 2..limit
    # Assume number is prime until it is proved that it isnt
    prime = true
    
    #Ruby includes the upper bound, thats why we do number-1
    for check in 2..number-1
        if number % check == 0
            prime = false
            break
        end
    end
    
    if prime 
        puts number
    end
end
