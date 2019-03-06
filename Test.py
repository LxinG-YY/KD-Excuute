a = input()
a = a[::-1]
flag = True
for item in a:
    if a.count(item) == 1:
        flag = False
        print(item)
        break
if flag:
    print("NULL")