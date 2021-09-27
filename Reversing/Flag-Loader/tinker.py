
DUCTF_str = "DUCTF"
input_letters = []
null_byte = "\0"
other_local = "\x01"

for i in range(0,5):
    x = ""
    x = chr(ord(null_byte)^ord(DUCTF_str[i]))
    x = ord("\0") / (ord(other_local) * ord(chr(i) + "\x01"))
    input_letters.append(x)

print (input_letters)