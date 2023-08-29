limit = int(input("Enter number upto which you want to find primes for: "))

for number in range(2, limit + 1):
    # Assume number is prime until it is proved that it isn't
    prime = True

    for check in range(2, number):
        if number % check == 0:
            prime = False
            break

    if prime:
        print(number)
