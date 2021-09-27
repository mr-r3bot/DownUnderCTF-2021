import string
from Crypto.Cipher import AES
from base64 import b64decode
from pwn import *


block_size = 16


def send_payload(p, data: str) -> str:
    p.sendlineafter("Enter plaintext:", data.encode())
    p.recvline()
    return_data = p.recvline()
    return return_data.decode().split("\n")


def find_offset(p) -> int:
    static = "A"*block_size*2
    offset_char = "}"
    for i in range(0, block_size):
        data_send = offset_char * i + static
        data_return = send_payload(p, data_send)
        blocks = b64decode(data_return[0])
        if blocks[block_size*2] == blocks[block_size*3]:
            print("Found offset: ", i)
            return i

    print("Offset error")
    exit(1)


def brute_force_letter(p, key="") -> str:
    offset = find_offset(p)
    offset_str = "B" * offset

    for i in range(0, block_size):
        static = "A"*(block_size - len(key) - 1)
        base_block = send_payload(p, offset_str + static)
        base_block = b64decode(base_block[0])
        block_should_be = base_block[block_size*2: block_size*3]

        for c in string.printable:
            data_send = offset_str + static + key + c
            data_return = send_payload(p, data_send)[0]
            decoded_block = b64decode(data_return)
            if block_should_be == decoded_block[block_size*2:block_size*3]:
                print ("Found a character: ", c)
                key += c
                print ("Current key value: ", key)
                break

    return key

def main(p):
    key = brute_force_letter(p)
    data = send_payload(p, "")
    cipher = AES.new(key, AES.MODE_ECB)
    pt = cipher.decrypt(data[0])
    print(pt)
    # DUCTF{ECB_M0DE_K3YP4D_D474_L34k}


if __name__ == "__main__":
    p = remote("pwn-2021.duc.tf", 31914)
    main(p)
