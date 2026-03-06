""" 
syntax : {expression for item in iterable if condition}
              |---{key:value} 
"""


book_price_inr = {
    
    "textbook": 500,
    "storybook": 800,
    "filmbook": 700
}


book_price_usd = {  book:round(price/90,2) for book,price in book_price_inr.items()  }

print(book_price_usd)