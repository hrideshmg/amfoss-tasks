def isSorted(arr: list):
    return True if sorted(arr) == arr else False

def isElegant(arr: list):
    if isSorted(arr): return True
    else:
        last_element = arr[-1]
        for i in range(1, len(arr)):
            test_series = arr.copy()
            test_series.extend(arr[0:i])
            del test_series[0:i]
            if isSorted(test_series): 
                return True
            
        return False

for _ in range(int(input())):
    input()
    blocks = [int(x) for x in input().split()]
    series = []
    ans = ""
    for block in blocks:
        if isElegant(series + [block]):
            series.append(block)
            ans += '1'
        else:
            ans += '0'
    print(ans)
