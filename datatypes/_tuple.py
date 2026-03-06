var = ("name","role","reg")

print(type(var))
print(var[0])
print("name" in var)

print(id(var))

nt = var.__add__(("sdf","df","dfsd"))
print(id(var))
print(var)
print(nt)