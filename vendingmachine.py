import csv 
import math

#order counter
order_number = 1

#accepted coins
accepted_input = [2.0 , 1.0 , 0.5, 0.2]

#stock items
stock_items = {
    "Water": {"Price": 1.50, "Stock": 5},
    "Soda" : {"Price": 1.50, "Stock": 10},
    "Chocolate" : {"Price": 2.5, "Stock": 5},
    "Crisps" : {"Price": 1.50, "Stock": 5},
    "Sandwich" : {"Price": 1.50, "Stock": 5},
}

#coin format
def format_coin(coin):
    return f"£{int(coin)}" if coin >= 1 else f"{int(coin*100)}p"

#coin input
def coins_inserted():
    balance = 0

    print("\nInsert Coins (£2, £1, 50p, 20p). Type 'Done' when finished.")

    while True:
        coin = input("Enter: ").lower()

        if coin == "done":
            break
        try:
            money = float(coin[:-1])/100 if coin.endswith("p") else float(coin) #checks if input is £ or p
            if money in accepted_input:
                balance += money
                print(f"Balance £{balance:.2f}")
            else:
                print("Invalid coin input.")
        except:
            print("Invalid input.")
    return balance


#print stock
def show_stock():

    lookup = {} #allows for direct lookup in vending()

    print("\n --- Vending Machine Menu ---")

    for i, (name, info) in enumerate(stock_items.items(), 1):
        print(f"{i}. {name} £{info['Price']:.2f} (Stock {info['Stock']})")
        lookup[str(i)] = name

    return lookup

#discount
def discount(basket, total):

    #if items bought > 3, 5% discount
    if len(basket)>=3: return 0.05

    #if money spent > 7, 15% discount
    if total > 7: return 0.15

    #if money spent > 5, 10% discount
    if total > 5: return 0.10

    return 0


#change
def change(amount):
    coins = []

    for c in accepted_input:
       count = int(amount // c)
       coins += [c] * count
       amount = round(amount - count * c , 2)
    return coins, amount


#csv receipt
def receipt(order, basket, total, disc, final, balance, coins):
    with open(f"receipt_{order}.csv","w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["Order", order])

        for i in basket: w.writerow([i,f"£{stock_items[i]['Price']:.2f}"])
        w.writerow(["Discount", f"{int(disc*100)}%"])
        w.writerow(["Total", f"£{total:.2f}"])
        w.writerow(["Final", f"£{final:.2f}"])
        w.writerow(["Balance", f"£{balance:.2f}"])
        w.writerow(["Change", ", ".join(format_coin(c) for c in coins)])
    print(f"Receipt saved: receipt_{order}.csv") #includes the order number in the save file

#vending function
def vending():
    global order_number

    while True:
        print(f"\n --- Order #{order_number} ---")

        balance = coins_inserted()
        basket, total = [], 0

        #user choice
        while True:
            lookup = show_stock()

            #user input
            choice = input("Select item # or 'done': ").lower()

            if choice == "done":
                break #checks to see if the user is done
            elif choice in lookup:
                name = lookup[choice]
                item = stock_items[name]

                if item["Stock"] > 0 and balance >= item["Price"]:
                    basket.append(name)
                    total += item["Price"]
                    balance -= item["Price"]
                    item["Stock"] -= 1
                    print(f"Added {name}. Balance £{balance:.2f}")
                else:
                    print("Out of stock or insufficient funds.")
            else:
                print("Invalid choice.")
            
        #basket checkout
        if basket:
            disc = discount(basket, total)
            final = total * (1 - disc)
            
            if order_number % 2 == 1 and final > 2: balance += 1 #bonus change rule for odd order number
            coins, kept = change(balance)

            print(f"Total £{total:.2f}, Discount{int(disc*100)}%, Final £{final:.2f}")
            print("Change: ", ", ".join(format_coin(c) for c in coins))
            if kept: print(f"Unreturned kept: £{kept:.2f}")

            receipt(order_number, basket, total, disc, final, balance, coins)
        else:
            print("No purchase.")

        order_number += 1

        if input("Next customer? (y/n): ").lower() != "y": break

    vending()