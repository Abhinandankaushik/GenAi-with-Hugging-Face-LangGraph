staff = [("amit",16),("zara",17)]


for name,age in staff:
    if age >= 18:
        print(f"{name} is eligible to manage the staff")
        break
else:                 # in for-else else block run only when then loop end without break  
    print(f"No one is eligible")