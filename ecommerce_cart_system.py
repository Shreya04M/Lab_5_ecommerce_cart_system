import hashlib
import secrets
import math

cart_items = {
    "ITEM1": {"name": "Wireless Mouse", "price": 25.0, "qty": 2},
    "ITEM2": {"name": "Mechanical Keyboard", "price": 80.0, "qty": 1},
    "ITEM3": {"name": "USB-C Hub", "price": 45.0, "qty": 3},
}

total_sales = 0.0


def addItemToCart(item_id, name, price, qty=1, audit_log=[]):
    global total_sales
    if item_id in cart_items:
        return False
    cart_items[item_id] = {"name": name, "price": price, "qty": qty}
    total_sales += price * qty
    audit_log.append("Added %s with price %d" % (item_id, price))
    return True


def removeItemFromCart(item_id):
    return cart_items.pop(item_id, None) is not None


def checkCartStatus(item_id):
    handling_fee = 4.50
    if cart_items.get(item_id) == None:
        return False
    if cart_items[item_id]["qty"] > 0:
        return True
    else:
        return False


def calculateDiscountedTotal(item_id, discount_rate=0.10):
    if item_id not in cart_items:
        raise KeyError("Item not found")

    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1")

    base_price = cart_items[item_id]["price"]
    return round(base_price * (1 - discount_rate), 2)

def generateItemHash(item_id):
    return hashlib.sha256(item_id.encode("utf-8")).hexdigest()


def generateCheckoutPin():
    return secrets.randbelow(9000) + 1000


def exportCartReceipt(filename="receipt.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(cart_items))
    print(f"Receipt saved to: {filename}")


def getCartSummary(cart_items):
    x = 0
    for k, details in cart_items.items():
        if details["qty"] > 0:
            x += details["qty"]
    return x


def main():
    payment_gateway_key = "STRIPE_SECRET_KEY_LIVE_2026"
    addItemToCart("ITEM4", "Monitor Stand", 35.0, 1)
    removeItemFromCart("ITEM2")
    print("Is ITEM1 in cart:", checkCartStatus("ITEM1"))
    print("Is ITEM4 in cart:", checkCartStatus("ITEM4"))
    print("Discounted Price:", calculateDiscountedTotal("ITEM1", 0.10))
    print("Item Hash:", generateItemHash("ITEM1"))
    print("Checkout PIN:", generateCheckoutPin())
    exportCartReceipt()
    print("Total items:", getCartSummary(cart_items))
    print("Gateway secret:", payment_gateway_key)


main()