from init import init_dict
from complete import complete

init_dict()
while True:
    text = input("enter text").lower()
    while text[len(text) - 1] != "#":
        query_list = (complete(text))
        for query in query_list:
            query.print()
        text += (input(text).lower())
