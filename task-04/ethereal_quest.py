resultant_vector = [0,0,0]
for _ in range(int(input())):
    xi,yi,zi = [int(num) for num in input().split()]
    resultant_vector[0] += xi
    resultant_vector[1] += yi
    resultant_vector[2] += zi
    
if resultant_vector == [0,0,0]:
    print("YES")
else:
    print("NO")
