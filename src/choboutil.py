def hash(str):
    h = 0
    for s in str:
        h = h * 31 + ord(s)
        if (h > 100000007):
            h %= 100000007
    return h