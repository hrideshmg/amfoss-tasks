traverse_index = 0
for char in input():
    if traverse_index < 5 and char=="hello"[traverse_index]:
        traverse_index += 1

if traverse_index == 5:
    print("YES")
else:
    print("NO")
