import System.IO (hFlush, stdout)

primeChecker :: Integer -> Integer-> Bool
primeChecker number check =
  if number == 2 then True 
    else
      if mod number check == 0
        then False
        else
        -- If the number is not divisible by a number one less than itself then its prime since all prior numbers have been checked.
        if check == (number-1)
          then True
          else primeChecker number (check+1)

printPrimes :: Integer -> Integer -> IO ()
printPrimes number limit =
  if number <= limit
    then
      -- If number is prime then print number and recursively call counter with number+1
      -- If number is not prime return a null value and recursively call counter with number+1
      -- If number reaches limit then just return null value.
      -- the do notation is neccessary for sequencing actions within the IO monad
      -- return () is neccessary to maintaing a consistent monadic structure within the if branches
      if primeChecker number 2
        then do
          putStrLn(show number)
          printPrimes (number+1) limit
        else do
          return ()
          printPrimes (number+1) limit
      else
        return ()

main::IO ()
main = do
  putStr("Enter number upto which you wish to calculate primes for: ")
  hFlush stdout  -- Flush the output buffer to print the user prompt before taking input
  
  lim_str <- getLine
  let lim_int = read lim_str::Integer
  printPrimes 2 lim_int
