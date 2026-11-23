"""Shop catalogue: the distributor's items with prices and the local names owners use.

In production the catalogue is built from photos of a shop's distributor bills.
Here it is a fixed sample catalogue so the demo and the evals are reproducible.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Item:
    id: str
    name: str
    pack: str
    price: int  # retail price in rupees (whole rupees keeps the checksum exact)
    category: str
    shelf_life_days: int
    unit_cost: int  # distributor's landed cost per unit, used for credit notes and value-at-risk
    aliases: tuple[str, ...] = field(default_factory=tuple)

    @property
    def label(self) -> str:
        return f"{self.name} {self.pack}"


# Aliases are what people actually say at a Patiala counter (Hindi/Punjabi code-mix, romanised).
# Some aliases are deliberately shared between pack sizes ("surf", "parle", "maggi"):
# the amount paid is what resolves them.
ITEMS: list[Item] = [
    Item("parle_g_10", "Parle-G", "small", 10, "biscuits", 180, 8, ("parle", "parle g", "parle-g", "parleji", "parle chhota", "chhota parle")),
    Item("parle_g_50", "Parle-G", "family pack", 50, "biscuits", 180, 42, ("parle", "parle g", "parle-g", "parle bada", "bada parle", "parle family")),
    Item("goodday_10", "Good Day", "₹10 pack", 10, "biscuits", 150, 8, ("good day", "goodday", "good day chhota")),
    Item("goodday_20", "Good Day", "₹20 pack", 20, "biscuits", 150, 17, ("good day", "goodday", "good day bada")),
    Item("surf_10", "Surf Excel", "₹10 sachet", 10, "home care", 540, 8, ("surf", "surf excel", "surf chhota", "surf sachet")),
    Item("surf_20", "Surf Excel", "₹20 pack", 20, "home care", 540, 17, ("surf", "surf excel", "surf bada", "surf packet")),
    Item("maggi_14", "Maggi", "70 g", 14, "noodles", 270, 12, ("maggi", "maggie", "maggi chhota", "noodles")),
    Item("maggi_56", "Maggi", "4-pack", 56, "noodles", 270, 49, ("maggi", "maggie", "maggi bada", "maggi chaar wala")),
    Item("horlicks_500", "Horlicks", "500 g", 250, "health drinks", 365, 240, ("horlicks", "horlix")),
    Item("bournvita_500", "Bournvita", "500 g", 245, "health drinks", 365, 232, ("bournvita", "bornvita")),
    Item("bread_400", "Bread", "400 g", 40, "bakery", 5, 34, ("bread", "double roti", "pav")),
    Item("tata_salt_1kg", "Tata Salt", "1 kg", 28, "staples", 720, 24, ("namak", "salt", "tata salt", "tata namak")),
    Item("dettol_75", "Dettol soap", "75 g", 45, "personal care", 900, 39, ("dettol", "dettol sabun", "dettol soap")),
    Item("colgate_100", "Colgate", "100 g", 55, "personal care", 720, 47, ("colgate", "paste", "colgate paste")),
    Item("lays_10", "Lay's", "₹10", 10, "snacks", 120, 8, ("lays", "lays chips", "chips")),
    Item("kurkure_10", "Kurkure", "₹10", 10, "snacks", 120, 8, ("kurkure",)),
    Item("dairymilk_10", "Dairy Milk", "₹10", 10, "chocolates", 270, 8, ("dairy milk", "dairymilk", "chocolate", "choco")),
    Item("kissan_jam_200", "Kissan jam", "200 g", 95, "spreads", 365, 82, ("jam", "kissan jam", "kissan")),
]

BY_ID: dict[str, Item] = {it.id: it for it in ITEMS}


def alias_index(items: list[Item] | None = None) -> dict[str, set[str]]:
    """Map each spoken alias to the set of item ids it can mean."""
    idx: dict[str, set[str]] = {}
    for it in items or ITEMS:
        for a in it.aliases:
            idx.setdefault(a.lower(), set()).add(it.id)
    return idx


def get(item_id: str) -> Item:
    return BY_ID[item_id]
