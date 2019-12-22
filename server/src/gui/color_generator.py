import random


def generate_hex_color(id):
    random.seed(id)
    return "#" + f"{random.randint(0,256):02x}{random.randint(0,256):02x}{random.randint(0,256):02x}"