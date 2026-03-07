"""
class wether:
    temp="hot"
    strength = "strong"
    

temp = wether()

print(temp.temp)"""


class Temp:
    def func(self):
        print(self)

t = Temp()

t.func()
Temp.func(t)