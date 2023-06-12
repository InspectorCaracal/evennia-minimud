from collections import Counter
from evennia import CmdSet
from evennia.utils import make_iter
from evennia.utils.evtable import EvTable

from .command import Command


class CmdList(Command):
    """
    View a list of items available for sale.
    """

    key = "list"
    aliases = ("browse",)

    def func(self):
        # verify that this shop has a storage box
        if not (storage := self.obj.db.storage):
            self.msg("This shop is not open for business.")
            return

        listings = []
        for obj in storage.contents:
            # check if the object has a price set
            if price := obj.db.price:
                # add it and its price to the listings
                listings.append((obj.name, price))

        condensed = Counter(listings)
        listings = [[key[0], val, key[1]] for key, val in condensed.items()]
        if not condensed:
            self.msg("This shop has nothing for sale right now.")
            return

        # build a table from the sale listings
        table = EvTable("Item", "Amt", "Price", border="rows")
        for key, val in condensed.items():
            table.add_row(key[0], val, key[1])

        # send it to the player
        self.msg(str(table))


class CmdBuy(Command):
    """
    Attempt to buy an item from this shop.

    Usage:
        buy <obj>
        buy <num> <obj>

    Example:
        buy iron sword
        buy 12 arrow
    """

    key = "buy"
    aliases = ("order", "purchase")

    def parse(self):
        """
        Parse out the optional number of units for the command
        """
        self.args = self.args.strip()
        # this splits the args at the first space into a string and a possibly-empty list of strings
        first, *rest = self.args.split(" ", maxsplit=1)

        # if the rest is empty, we assume it's just an object name
        if not rest:
            self.count = 1
        # is the first item a number?
        elif first.isdecimal():
            self.count = int(first)
            # combine the rest back into a string
            self.args = " ".join(rest)
        else:
            # the first word is not a number, so it's all just one object
            self.count = 1

    def func(self):
        # verify that this shop has a storage box
        if not (storage := self.obj.db.storage):
            self.msg("This shop is not open for business.")
            return

        # check if we have any money first
        if not (coins := self.caller.db.coins):
            self.msg("You don't have any money!")
            return

        # we want a stack of the item, matching the parsed count
        objs = self.caller.search(self.args, location=storage, stacked=self.count)
        if not objs:
            # we found nothing, or it was too vague of a search
            return

        # make the result into a list so we can handle it consistently
        objs = make_iter(objs)
        objs = [obj for obj in objs if obj.db.price]
        if not objs:
            # avoid this! don't put objects without price tags into the storage box!
            self.msg(f"There are no {self.args} for sale.")
            return

        example = objs[0]
        count = len(objs)
        obj_name = example.get_numbered_name(count, self.caller)[1]
        # calculate the total for all the objects
        total = sum([obj.attributes.get("price", 0) for obj in objs])

        # do we have enough money?
        if coins < total:
            self.msg(f"You need {total} coins to buy that.")
            return

        # confirm that this is what the player wants to buy
        confirm = yield (f"Do you want to buy {obj_name} for {total}? Yes/No")

        # if it's not a form of yes, cancel
        if confirm.lower().strip() not in ("yes", "y"):
            self.msg("Purchase cancelled.")
            return

        # everything is good! do a capitalism!
        for obj in objs:
            obj.location = self.caller

        self.caller.db.coins -= total

        self.msg(f"You exchange {total} coins for {count} {obj_name}.")


class CmdSell(Command):
    """
    Offer something for sale to a shop.

    Usage:
        sell <obj>
        sell <num> <obj>

    Example:
        sell sword
        sell 8 apple
    """

    key = "sell"

    def parse(self):
        """
        Parse out the optional number of units for the command
        """
        self.args = self.args.strip()
        # this splits the args at the first space into a string and a possibly-empty list of strings
        first, *rest = self.args.split(" ", maxsplit=1)

        # if the rest is empty, we assume it's just an object name
        if not rest:
            self.count = 1
        # is the first item a number?
        elif first.isdecimal():
            self.count = int(first)
            # combine the rest back into a string
            self.args = " ".join(rest)
        else:
            # the first word is not a number, so it's all just one object
            self.count = 1

    def func(self):
        # verify that this shop has a storage box
        if not (storage := self.obj.db.storage):
            self.msg("This shop is not open for business.")
            return

        # we want a stack of the item, matching the parsed count
        objs = self.caller.search(self.args, location=self.caller, stacked=self.count)
        if not objs:
            # we found nothing, or it was too vague of a search
            return

        # make the result into a list so we can handle it consistently
        objs = make_iter(objs)
        example = objs[0]
        count = len(objs)
        obj_name = example.get_numbered_name(count, self.caller)[1]
        # calculate the total for all the objects
        total = sum([obj.attributes.get("value", 0) for obj in objs])

        # confirm that this is what the player wants to buy
        confirm = yield (f"Do you want to sell {obj_name} for {total}? Yes/No")

        # if it's not a form of yes, cancel
        if confirm.lower().strip() not in ("yes", "y"):
            self.msg("Sale cancelled.")
            return

        # everything is good! do a capitalism!
        for obj in objs:
            self.obj.add_stock(obj)

        self.caller.db.coins += total

        self.msg(f"You exchange {total} coins for {obj_name}.")


class ShopCmdSet(CmdSet):
    key = "Shop CmdSet"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()

        self.add(CmdList)
        self.add(CmdBuy)
        self.add(CmdSell)
