from collections import Counter

def sint(list):
    if not list: return 0
    for num in range(max(list)+2): 
        if num not in list:
            return num
            break
for _ in range(int(input())):
    input()
    
    shipment = [int(x) for x in input().split()]      
    ship_freq = sorted(Counter(shipment).items())

    A = []
    B = []

    for case in ship_freq:
        model, freq = case
        if freq > 1:
            A.append(model)
            B.append(model)
        else:
            A.append(model)


    print(sint(A) + sint(B))
