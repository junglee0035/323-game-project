shop_items = {
    "Battery Upgrade": 100,
    "Skin 2": 50,
    "Coin Magnet": 75,
    "Skip Level": 200
}

def buy_item(player_data, item_name):
    if item_name in player_data["inventory"]:
        return f"You already bought {item_name}!"

    cost = shop_items[item_name]
    if player_data["coins"] >= cost:
        player_data["coins"] -= cost
        player_data["inventory"].append(item_name)

        # Apply effects
        if item_name == "Battery Upgrade":
            player_data["max_energy"] += 50  # add 50 max energy as effect!

        return f"You bought {item_name}!"
    else:
        return "Not enough coins."


def shop_menu(player_data):
    while True:
        print("\n--- SHOP ---")
        for i, (item, price) in enumerate(shop_items.items(), start=1):
            owned = "(OWNED)" if item in player_data["inventory"] else ""
            print(f"{i}. {item} - {price} coins {owned}")
        print("q. Exit Shop")

        choice = input("Choose an item (1-4) or 'q': ").strip()

        if choice == "q":
            return "You left the shop."

        if choice in ["1", "2", "3", "4"]:
            item_list = list(shop_items.keys())
            item_name = item_list[int(choice) - 1]
            print(buy_item(player_data, item_name))
        else:
            print("Invalid choice.")
