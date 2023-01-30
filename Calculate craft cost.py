import json
import requests


def get_item_from_ah(item, rarity=""):
    print(f"Looking for {item} {rarity} on auction house")
    price = []
    ah = requests.get("https://api.hypixel.net/skyblock/auctions").json()
    for page in range(ah["totalPages"]):
        print(f"Auction house page: {page}")
        ah = requests.get("https://api.hypixel.net/skyblock/auctions", params={"page": page}).json()
        try:
            for auction in ah["auctions"]:
                try:
                    if rarity != "":
                        if auction["bin"] and "Skin" not in auction["item_name"] and item in auction["item_name"] and auction["tier"] == rarity:
                            print(f"Adding: {auction['starting_bid']}")
                            price.append(auction["starting_bid"])
                    else:
                        if auction["bin"] and "Skin" not in auction["item_name"] and item in auction["item_name"]:
                            print(f"Adding: {auction['starting_bid']}")
                            price.append(auction["starting_bid"])
                except KeyError:
                    if auction["bin"] and "Skin" not in auction["item_name"] and item in auction["item_name"]:
                        print(f"Adding: {auction['starting_bid']}")
                        price.append(auction["starting_bid"])
        except KeyError:
            pass
    if len(price) != 0:
        print(f"Lowest price for {item} found is: {sorted(price)[0]}")
        return sorted(price)[0]
    else:
        print(f"{item} is not on auction house")
        return 0


def get_item_from_bazzar(item):
    print(f"Looking for {item} on bazzar")
    baz = requests.get("https://api.hypixel.net/skyblock/bazaar").json()
    for x in baz["products"]:
        if x == item:
            print(f"Lowest price for {item} found is: {baz['products'][x]['buy_summary'][0]['pricePerUnit']}")
            return baz["products"][x]["buy_summary"][0]["pricePerUnit"]
    print(f"{item} is not on bazzar")
    return 0


def get_craft_cost(item, item_rarity=""):
    item = get_item_recipe(item, item_rarity)
    craft_cost = 0
    items_used = []

    for x in item:
        if item[x] != "":
            crafting_item = item[x].split(":")
            item_rarity = get_item_rarity(crafting_item[0])
            named_item = get_item_name(crafting_item[0])
            print(f"Getting price of {named_item}")
            if crafting_item[0] in items_used:
                cost = items_used[items_used.index(crafting_item[0]) + 1]
                print(f"{named_item} already used, using {str(cost)} as price")
                cost *= int(crafting_item[1])
            else:
                print(f"{named_item} was note yet used, looking for price")
                cost = get_item_from_bazzar(crafting_item[0])
                if cost == 0:
                    cost = get_item_from_ah(named_item, item_rarity)
                items_used.append(crafting_item[0])
                items_used.append(cost)
                cost *= int(crafting_item[1])
            craft_cost += cost
            craft_cost = round(craft_cost)
            print(f"After adding {named_item} crafting cost is: {craft_cost}")

    return craft_cost


def get_item_name(item):
    with open("items_original.json", "r") as f:
        items = json.loads(f.read())

        for x in items:
            if x["id"] == item:
                return x["name"]
    return item


def get_item_recipe(item, rarity):
    with open("items.json", "r") as f:
        items = json.loads(f.read())

        for x in items:
            if rarity != "":
                if x["displayname"] == item and x["lore"][-1].split()[0][4:] == rarity:
                    return x["recipe"]
            else:
                if x["displayname"] == item:
                    return x["recipe"]
    return item


def get_item_rarity(item):
    with open("items.json", "r") as f:
        items = json.loads(f.read())

        for x in items:
            if x["internalname"] == item:
                print(x["lore"][-1].split()[0][4:])
                return x["lore"][-1].split()[0][4:]

    return ""


while True:
    try:
        item = input("Please enter name of your item: ").split(":")
        if len(item) > 1:
            craft_price = get_craft_cost(item[0], item[1].upper())
            lowest_bin = get_item_from_ah(item[0], item[1].upper())
        else:
            craft_price = get_craft_cost(item[0])
            lowest_bin = get_item_from_ah(item[0])
        print("Craft cost: " + str(craft_price))
        print("Lowest bin: " + str(lowest_bin))
    except requests.exceptions.ChunkedEncodingError:
        print("Server error :(")


