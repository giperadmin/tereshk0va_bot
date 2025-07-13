def test(n):
    match n:
        case "1":
            return 8
        case "2":
            return 9
        case _:
            return 0

n=input()
print(test(n))
