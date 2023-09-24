reference_list = list("amfoss")
for _ in range(int(input())):
    diff = 0
    str_list = list(input().strip())
    for index, char in enumerate(str_list):
        if char != reference_list[index]:
            diff += 1
    print(diff)
