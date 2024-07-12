import random


async def generate_unique_code():
    code = random.randint(1000, 9999)
    return code
