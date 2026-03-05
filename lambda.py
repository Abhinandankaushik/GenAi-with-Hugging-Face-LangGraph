# (lambda name: print(name))("Abhinandan")


f = lambda n: 1 if n==0 or n==1 else n*f(n-1)


print(f(100))
