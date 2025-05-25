import time
import threading

# Product info
product = {
    "name": "Samsung Galaxy S22",
    "starting_price": 50000,
    "current_price": 50000,
    "highest_bidder": None
}

bidders = []
bidding_open = False
last_bid_time = None


# Step 1: Collect users for 30 seconds
def collect_users():
    print("🔔 Bidding will start in 30 seconds. Users can join now!\n")

    start_time = time.time()
    while time.time() - start_time < 30:
        remaining = int(30 - (time.time() - start_time))
        print(f"\r⏳ Time left to join: {remaining} seconds  ", end="")
        time.sleep(1)
        if remaining % 5 == 0 or remaining == 29:  # Prompt input a few times
            print("\n")
            name = input("Enter your name to join bidding: ")
            if name and name not in bidders:
                bidders.append(name)
                print(f"✅ {name} joined the bidding!\n")
    
    print("\n⏰ Time’s up! Bidding is starting now...\n")


# Step 2: Timer to close bidding if no bid in 30 seconds
def bidding_timer():
    global bidding_open
    while bidding_open:
        time_left = 30 - int(time.time() - last_bid_time)
        if time_left <= 0:
            bidding_open = False
            print("\n⏳ No new bid in 30 seconds...")
            print("💥 Bidding Closed!")
            if product["highest_bidder"]:
                print(f"🏆 Winner: {product['highest_bidder']}")
                print(f"💰 Final Price: Rs. {product['current_price']}")
            else:
                print("😢 No valid bids received.")
            break
        print(f"\r⌛ Waiting for next bid... {time_left}s  ", end="")
        time.sleep(1)


# Step 3: Bidding process
def start_bidding():
    global last_bid_time, bidding_open
    bidding_open = True
    last_bid_time = time.time()

    print(f"📦 Product: {product['name']}")
    print(f"💸 Starting Price: Rs. {product['starting_price']}\n")

    # Start timer in the background
    threading.Thread(target=bidding_timer, daemon=True).start()

    while bidding_open:
        for bidder in bidders:
            try:
                print()  # move to new line from timer
                bid = int(input(f"{bidder}, enter your bid: Rs. "))
                if not bidding_open:
                    break
                if bid > product["current_price"]:
                    product["current_price"] = bid
                    product["highest_bidder"] = bidder
                    last_bid_time = time.time()  # Reset the timer
                    print(f"\n✅ New highest bid: Rs. {bid} by {bidder}\n")
                else:
                    print("❌ Your bid must be higher than the current price.\n")
            except ValueError:
                print("❌ Please enter a valid number.\n")


# Run everything
collect_users()
start_bidding()
