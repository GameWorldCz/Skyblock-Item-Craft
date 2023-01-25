import json
from time import sleep
import requests
import os


def get_item_from_ah(item):
    print(f"Looking for {item} on auction house")
    price = []
    ah = requests.get("https://api.hypixel.net/skyblock/auctions").json()
    for page in range(ah["totalPages"]):
        print(f"Auction house page: {page}")
        ah = requests.get("https://api.hypixel.net/skyblock/auctions", params={"page": page}).json()
        try:
            for auction in ah["auctions"]:
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


def get_craft_cost(item):
    item = get_item(item)
    craft_cost = 0
    items_used = []

    for num, x in enumerate(item):
        if item[x] != "":
            crafting_item = item[x].split(":")
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
                    cost = get_item_from_ah(named_item)
                cost *= int(crafting_item[1])
                items_used.append(crafting_item[0])
                items_used.append(cost)
            craft_cost += cost
            craft_cost = round(craft_cost, 1)
            print(f"After adding {named_item} crafting cost is: {craft_cost}")

    return craft_cost


def get_item_name(item):
    with open("items_original.json", "r") as f:
        items = json.loads(f.read())

        for x in items:
            if x["id"] == item:
                print(f"Renaming {item} to {x['name']}")
                return x["name"]
    return item


def get_item(item):
    with open("items.json", "r") as f:
        items = json.loads(f.read())

        for x in items:
            if x["displayname"] == item:
                return x["recipe"]
    return item


while True:
    item = input("Please enter name of your item: ")
    craft_price = get_craft_cost(item)
    lowest_bin = get_item_from_ah(item)
    print("Craft cost: " + str(craft_price))
    print("Lowest bin: " + str(lowest_bin))
    
