import string
import random
from time import sleep

some_list = [1, 2, 3, 4, 5]

# Generator
another = (x * x for x in range(100_000_000_000) if x % 2 == 0)
print(another)


# Iterator
class Something:
    def __init__(self) -> None:
        self.last_item = 0

    def __next__(self):
        self.last_item += 1
        if self.last_item >= 10:
            raise StopIteration
        return self.last_item

    def __iter__(self):
        return self


# Example of while True that's equivalent to for loop
# while True:
#     try:
#         item = next(another)
#     except StopIteration:
#         break
#     else:
#         print(item)   # The content of the for loop


def password_maker(length: int = 10):
    print("STARTING OUR RUN")
    while True:
        print("GENERATED NEW PASSWORD")
        yield "".join(random.choice(string.ascii_letters) for _ in range(length))


gen1 = password_maker()
gen2 = password_maker(length=20)

print(gen1)
print(gen2)


def slow_gen():
    sleep(0.1)
    yield "FIRST"
    sleep(0.2)
    yield "SECOND"
    sleep(0.3)
    yield "THIRD"
    sleep(0.4)


gen = slow_gen()
next(gen)
next(gen)
next(gen)
# next(gen)  # The fourth `next` will error with StopIteration, because there's nothing more to "yield"
gen = slow_gen()
next(gen)
next(gen)
next(gen)
# next(gen)  # The fourth `next` will error with StopIteration, because there's nothing more to "yield"

for item in slow_gen():
    print(item)
    
for item in slow_gen():
    print("AGAIN", item)
