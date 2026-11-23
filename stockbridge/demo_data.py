"""A sample route for the demo: 8 shops on one Patiala distributor route (synthetic data).

The numbers are made up but shaped like a real route: a few slow shops holding stock that
won't sell, faster shops nearby that will run out, one lot past the return window, and one
lot too close to expiry to move.
"""
from __future__ import annotations

from .twin import Lot, Policy, RouteTwin, Shop

SHOPS = [
    Shop("sharma", "Sharma General Store", 1.0, 1.2, 6000),
    Shop("bansal", "Bansal Kirana", 2.1, 0.8, 8000, spent_this_week=6240),
    Shop("school", "School Road Store", 2.6, 2.0, 5000),
    Shop("gill", "Gill Stores", 3.5, 0.4, 7000),
    Shop("arora", "Arora Kirana", 4.0, 1.5, 6000),
    Shop("verma", "Verma Mart", 0.6, 3.0, 9000),
    Shop("sethi", "Sethi General Store", 1.4, 3.6, 6000),
    Shop("kaur", "Kaur Provision Store", 3.0, 3.2, 5000),
]

# (shop, item, units per day)
RATES = [
    # Horlicks: Sharma sells none, Bansal and School Road sell steadily.
    ("sharma", "horlicks_500", 0.0), ("bansal", "horlicks_500", 0.43), ("school", "horlicks_500", 0.21),
    ("gill", "horlicks_500", 0.05), ("kaur", "horlicks_500", 0.10),
    # Good Day ₹20: slow at Sharma, fast at Bansal.
    ("sharma", "goodday_20", 0.29), ("bansal", "goodday_20", 1.7), ("arora", "goodday_20", 0.6),
    # Bread: sells but the lot is about to expire.
    ("sharma", "bread_400", 2.0), ("bansal", "bread_400", 3.0),
    # Bournvita: Gill is slow, Arora and Kaur sell.
    ("gill", "bournvita_500", 0.05), ("arora", "bournvita_500", 0.40), ("kaur", "bournvita_500", 0.15),
    # Dettol: Verma overstocked, Sethi sells.
    ("verma", "dettol_75", 0.10), ("sethi", "dettol_75", 0.50), ("kaur", "dettol_75", 0.20),
    # Everyday counter items at Sharma (used by the shop-app demo).
    ("sharma", "parle_g_10", 3.0), ("sharma", "parle_g_50", 0.2), ("sharma", "surf_10", 1.0), ("sharma", "surf_20", 0.6),
    ("sharma", "maggi_14", 2.5), ("sharma", "goodday_10", 1.2), ("sharma", "lays_10", 2.0), ("sharma", "dairymilk_10", 1.5),
    ("sharma", "tata_salt_1kg", 0.8),
]

LOTS = [
    Lot("L1", "sharma", "horlicks_500", "B2307", 9, 41),
    Lot("L2", "bansal", "horlicks_500", "B2311", 2, 60),
    Lot("L3", "sharma", "goodday_20", "G0418", 20, 25),
    Lot("L4", "bansal", "goodday_20", "G0422", 3, 40),
    Lot("L5", "sharma", "bread_400", "0712", 12, 2),
    Lot("L6", "gill", "bournvita_500", "B1981", 8, 33),
    Lot("L7", "verma", "dettol_75", "D554", 24, 52),
    Lot("L8", "sethi", "dettol_75", "D561", 5, 120),
    Lot("L9", "sharma", "parle_g_10", "P1101", 14, 120),
    Lot("L10", "sharma", "parle_g_50", "P1102", 4, 140),
    Lot("L11", "sharma", "surf_10", "S0901", 10, 400),
    Lot("L12", "sharma", "surf_20", "S0902", 6, 400),
    Lot("L13", "sharma", "maggi_14", "M0310", 8, 150),
    Lot("L14", "sharma", "goodday_10", "G0430", 12, 100),
    Lot("L15", "sharma", "lays_10", "C0201", 15, 60),
    Lot("L16", "sharma", "dairymilk_10", "D0101", 18, 200),
    Lot("L17", "sharma", "tata_salt_1kg", "T0505", 10, 600),
]

# Sample counter conversations for the shop-app demo (transcript, amount paid by UPI; None = cash).
SAMPLE_SALES = [
    ("bhaiya teen parle g ek surf dena", 50),
    ("ek good day ek surf de do", 30),
    ("do maggi aur ek lays", 38),
    ("ek dairy milk chocolate", 10),
    ("tata namak ek packet", None),
]


def build() -> RouteTwin:
    import copy
    shops = {s.id: copy.deepcopy(s) for s in SHOPS}
    lots = [copy.deepcopy(l) for l in LOTS]
    rates = {(s, i): r for s, i, r in RATES}
    return RouteTwin("Gupta Distributors · Patiala Route 4", (0.0, 0.0), shops, lots, rates,
                     policy=Policy(clearance_discount=0.6))
