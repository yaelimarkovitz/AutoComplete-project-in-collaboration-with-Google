from init import init_dict
from complete import complete
print("we preparing the system ")
init_dict()


while True:
    text = input("enter text ").lower()
    while text[len(text) - 1] != "#":
        query_list = (complete(text))
        if query_list:
            print("we found " + str(len(query_list))+" suggestion: ")
            for query in query_list:
                query.print(text)
        else:
            print("no match queries")
        text += (input(text).lower())
