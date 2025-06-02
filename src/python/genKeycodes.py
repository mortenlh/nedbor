import random
import string

def genRandomkey(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

numberOfKeys = 90000
keylength = 9

keys = [genRandomkey(keylength) for i in range(numberOfKeys)]

with open("koder.txt","w") as file:
    for line in keys:
        file.write(line+"\n")

print("Done")        