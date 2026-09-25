# ==========================================================
# InsightSQL AI - Business Configuration
# ==========================================================

# -----------------------
# Product Categories
# -----------------------

CATEGORIES = [
    "Electronics",
    "Home",
    "Sports",
    "Books",
    "Fashion",
    "Beauty",
    "Toys",
    "Groceries"
]

# -----------------------
# Category Price Ranges (€)
# -----------------------

PRICE_RANGES = {
    "Electronics": (80, 800),
    "Home": (20, 300),
    "Sports": (15, 250),
    "Books": (10, 60),
    "Fashion": (15, 180),
    "Beauty": (8, 90),
    "Toys": (12, 120),
    "Groceries": (3, 40)
}

# -----------------------
# German City Distribution
# Higher weight = more customers
# -----------------------

CITY_WEIGHTS = {
    "Berlin": 24,
    "Hamburg": 16,
    "Munich": 15,
    "Cologne": 12,
    "Frankfurt": 10,
    "Stuttgart": 8,
    "Leipzig": 6,
    "Dresden": 5,
    "Bremen": 2,
    "Hanover": 2
}

# -----------------------
# Payment Method Distribution
# -----------------------

PAYMENT_WEIGHTS = {
    "Credit Card": 45,
    "PayPal": 30,
    "Debit Card": 20,
    "Bank Transfer": 5
}

# -----------------------
# Order Status Distribution
# -----------------------

STATUS_WEIGHTS = {
    "Completed": 85,
    "Pending": 7,
    "Returned": 5,
    "Cancelled": 3
}

# -----------------------
# Product Catalog
# -----------------------

PRODUCTS = {
    "Electronics": [
        "Wireless Mouse",
        "Mechanical Keyboard",
        "USB-C Hub",
        "Monitor",
        "Webcam",
        "Laptop Stand",
        "SSD 1TB",
        "Bluetooth Speaker",
        "Noise Cancelling Headphones",
        "Smart Watch",
        "Power Bank",
        "USB Microphone",
        "Gaming Chair",
        "WiFi Router",
        "Tablet"
    ],

    "Home": [
        "Coffee Maker",
        "Vacuum Cleaner",
        "Desk Lamp",
        "Air Fryer",
        "Electric Kettle",
        "Dining Chair",
        "Wall Clock",
        "Cookware Set",
        "Blender",
        "Storage Box",
        "Bookshelf",
        "Curtains",
        "Bed Sheet",
        "Memory Pillow",
        "Floor Mat"
    ],

    "Sports": [
        "Yoga Mat",
        "Football",
        "Adjustable Dumbbell",
        "Resistance Band",
        "Skipping Rope",
        "Tennis Racket",
        "Basketball",
        "Cycling Helmet",
        "Sports Water Bottle",
        "Running Shoes",
        "Gym Gloves",
        "Fitness Ball",
        "Foam Roller",
        "Sports Backpack",
        "Pull-up Bar"
    ],

    "Books": [
        "Data Science Guide",
        "Python Programming",
        "SQL Essentials",
        "Machine Learning Basics",
        "Deep Learning Intro",
        "Business Analytics",
        "Statistics Handbook",
        "AI for Everyone",
        "Clean Code",
        "Algorithms Book",
        "Database Systems",
        "Power BI Guide",
        "Linear Algebra",
        "Probability Basics",
        "Data Visualization"
    ],

    "Fashion": [
        "Hoodie",
        "T-Shirt",
        "Jeans",
        "Sneakers",
        "Winter Jacket",
        "Baseball Cap",
        "Leather Backpack",
        "Cotton Socks",
        "Sweater",
        "Formal Shirt",
        "Shorts",
        "Leather Belt",
        "Scarf",
        "Beanie",
        "Watch Strap"
    ],

    "Beauty": [
        "Face Wash",
        "Moisturizer",
        "Shampoo",
        "Conditioner",
        "Body Lotion",
        "Perfume",
        "Lip Balm",
        "Sunscreen",
        "Hair Serum",
        "Beard Oil",
        "Hand Cream",
        "Face Mask",
        "Vitamin C Serum",
        "Organic Soap",
        "Hair Dryer"
    ],

    "Toys": [
        "Puzzle",
        "Building Blocks",
        "Toy Car",
        "Board Game",
        "Doll",
        "Chess Set",
        "RC Car",
        "Plush Bear",
        "Card Game",
        "Robot Kit",
        "Coloring Set",
        "Toy Train",
        "Drone Toy",
        "Magic Cube",
        "Lego Pack"
    ],

    "Groceries": [
        "Olive Oil",
        "Green Tea",
        "Coffee Beans",
        "Whole Wheat Pasta",
        "Basmati Rice",
        "Organic Honey",
        "Rolled Oats",
        "Peanut Butter",
        "Almonds",
        "Protein Bar",
        "Milk Powder",
        "Breakfast Cereal",
        "Dark Chocolate",
        "Chia Seeds",
        "Walnuts"
    ]
}

# -----------------------
# Product Popularity
# Higher value = sells more often
# -----------------------

POPULARITY = {
    "Wireless Mouse": 10,
    "Mechanical Keyboard": 8,
    "USB-C Hub": 8,
    "Monitor": 6,
    "Webcam": 7,
    "SSD 1TB": 5,
    "Coffee Maker": 8,
    "Air Fryer": 9,
    "Yoga Mat": 9,
    "Running Shoes": 8,
    "Football": 7,
    "SQL Essentials": 9,
    "Python Programming": 10,
    "Data Science Guide": 8,
    "Hoodie": 9,
    "Sneakers": 10,
    "Face Wash": 8,
    "Shampoo": 10,
    "Puzzle": 8,
    "Building Blocks": 7,
    "Olive Oil": 8,
    "Green Tea": 9,
    "Protein Bar": 10,
    "Peanut Butter": 9
}