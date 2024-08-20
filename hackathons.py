import datetime

class AuctionItem:
    def init(self, title, description, min_bid, start_time, end_time):
        self.title = title
        self.description = description
        self.min_bid = min_bid
        self.start_time = start_time
        self.end_time = end_time
        self.highest_bid = 0
        self.highest_bidder = None
        self.bids = []

    def add_bid(self, bid_amount, bidder):
        if bid_amount > self.highest_bid:
            self.highest_bid = bid_amount
            self.highest_bidder = bidder
            self.bids.append((bid_amount, bidder))
            return True
        return False

    def is_active(self):
        now = datetime.datetime.now()
        return self.start_time <= now <= self.end_time

    def close_auction(self):
        if datetime.datetime.now() > self.end_time:
            return True
        return False

class User:
    def init(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.bids = []
    
    def place_bid(self, auction, amount):
        if auction.add_bid(amount, self.username):
            self.bids.append((auction.title, amount))
            return True
        return False

class AuctionSystem:
    def init(self):
        self.users = {}
        self.auctions = {}
        self.logged_in_user = None

    def register_user(self, username, password, email):
        if username in self.users:
            print("User already exists!")
            return
        self.users[username] = User(username, password, email)
        print("User registered successfully!")

    def login_user(self, username, password):
        if username in self.users and self.users[username].password == password:
            self.logged_in_user = self.users[username]
            print("Login successful!")
        else:
            print("Invalid credentials!")

    def create_auction(self, title, description, min_bid, start_time, end_time):
        if not self.logged_in_user:
            print("You must be logged in to create an auction.")
            return

        auction_id = len(self.auctions) + 1
        self.auctions[auction_id] = AuctionItem(
            title, description, min_bid, start_time, end_time
        )
        print(f"Auction created successfully with ID {auction_id}!")

    def place_bid(self, auction_id, amount):
        if not self.logged_in_user:
            print("You must be logged in to place a bid.")
            return
        
        if auction_id not in self.auctions:
            print("Auction not found!")
            return

        auction = self.auctions[auction_id]
        if not auction.is_active():
            print("Auction not available!")
            return

        if self.logged_in_user.place_bid(auction, amount):
            print(f"Bid placed successfully! Current highest bid: {auction.highest_bid}")
        else:
            print("Bid too low or invalid!")

    def show_auctions(self):
        if not self.auctions:
            print("No auctions available.")
            return
        
        for id, auction in self.auctions.items():
            status = "Active" if auction.is_active() else "Closed"
            print(f"ID: {id}")
            print(f"Title: {auction.title}")
            print(f"Description: {auction.description}")
            print(f"Minimum Bid: {auction.min_bid}")
            print(f"Start Time: {auction.start_time}")
            print(f"End Time: {auction.end_time}")
            print(f"Highest Bid: {auction.highest_bid}")
            print(f"Highest Bidder: {auction.highest_bidder}")
            print(f"Status: {status}")
            print("Bids:")
            for bid_amount, bidder in auction.bids:
                print(f"  {bidder} bid {bid_amount}")
            print()

    def show_user_profile(self):
        if not self.logged_in_user:
            print("You must be logged in to view the profile.")
            return
        
        user = self.logged_in_user
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print("Bids Made:")
        for auction_title, amount in user.bids:
            print(f"  Auction: {auction_title}, Amount: {amount}")

def main():
    system = AuctionSystem()

    while True:
        print("1. Register")
        print("2. Login")
        print("3. Create Auction")
        print("4. Place Bid")
        print("5. Show Auctions")
        print("6. Show User Profile")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            system.register_user(username, password, email)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            system.login_user(username, password)
        elif choice == '3':
            title = input("Enter auction title: ")
            description = input("Enter auction description: ")
            min_bid = float(input("Enter minimum bid amount: "))
            start_time = datetime.datetime.strptime(input("Enter start time (YYYY-MM-DD HH:MM:SS): "), '%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.strptime(input("Enter end time (YYYY-MM-DD HH:MM:SS): "), '%Y-%m-%d %H:%M:%S')
            system.create_auction(title, description, min_bid, start_time, end_time)
        elif choice == '4':
            auction_id = int(input("Enter auction ID: "))
            amount = float(input("Enter bid amount: "))
            system.place_bid(auction_id, amount)
        elif choice == '5':
            system.show_auctions()
        elif choice == '6':
            system.show_user_profile()
        elif choice == '7':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()