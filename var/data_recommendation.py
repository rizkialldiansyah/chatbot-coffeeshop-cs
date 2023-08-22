rules = {
    # rules (jenis, rasa, suhu, variasi)
    #====KOPI====
    # dingin
    ("kopi", "manis", "dingin", "susu"): "Es Kopi Pertama",
    ("kopi", "gurih", "dingin", "susu"): "Salted Caramel Latte",
    # ("kopi", "asam", "dingin", "susu"): None,
    # ("kopi", "manis", "dingin", "non"): None,
    # ("kopi", "gurih", "dingin", "non"): None,
    ("kopi", "asam", "dingin", "non"): "Black (Iced)",
    # panas
    ("kopi", "manis", "panas", "susu"): "White (Hot)",
    # ("kopi", "gurih", "panas", "susu"): None,
    # ("kopi", "asam", "panas", "susu"): None,
    # ("kopi", "manis", "panas", "non"): None,
    # ("kopi", "gurih", "panas", "non"): None,
    ("kopi", "asam", "panas", "non"): "Black (Hot)",
    #====non====
        # dingin
    ("non", "manis", "dingin", "susu"): "Ice Choco",
    ("non", "gurih", "dingin", "susu"): "Red Velvet",
    # ("non", "asam", "dingin", "susu"): None,
    ("non", "manis", "dingin", "non"): "Ice Peach Tea",
    ("non", "gurih", "dingin", "non"): "Sip and Sour",
    ("non", "asam", "dingin", "non"): "Not So Tamariend",
    # panas
    ("non", "manis", "panas", "susu"): "Hot Choco",
    ("non", "gurih", "panas", "susu"): "Hot Red Velvet",
    # ("non", "asam", "panas", "susu"): None,
    # ("non", "manis", "panas", "non"): None,
    # ("non", "gurih", "panas", "non"): None,
    ("non", "asam", "panas", "non"): "Hot Lemon Tea",
}

# Bobot Prioritas tiap parameter rules
weight = {
    "jenis": 0.35,
    "rasa": 0.2,
    "suhu": 0.275,
    "variasi": 0.175
}
