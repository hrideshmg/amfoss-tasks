def strict_inc(arr):
    if list(set(arr)) != arr:
        return False
    elif sorted(arr) == arr:
        return True

# Disclaimer - I know this looks like an absolute mess (and it is) but hey it works!    

for _ in range(int(input())):
    input()
    arr = [int(x) for x in input().split()]
    operations = 0
    for num in reversed(arr):
        if not strict_inc(arr):
            while num != max(arr) or (num==max(arr) and arr.count(max(arr)) > 1):
                if sum(arr) == 0: 
                    operations = -1
                    break
                arr[arr.index(max(arr))] = max(arr)//2
                operations += 1

            if num == max(arr) and arr.count(max(arr)) == 1:
                arr.pop(arr.index(num))

    print(operations)
