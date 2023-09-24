input()
list = [int(x) for x in input().split()]

for index, number in enumerate(list):
    if number == min(list):
        if list.count(number) > 1:
            print("Still Aetheria")
            break
        print(index+1)
        break
