from init import init_dict
from complete import complete
import sys

print("Loading the files and preparing the system...")
init_dict()

text = input("The system is ready. please enter text ").lower()
while True:

    while text[len(text) - 1] != "#":
        query_list = (complete(text))
        if query_list:
            print("we found " + str(len(query_list)) + " suggestion: ")
            for query in query_list:
                query.print(text)
        else:
            print("no match queries")
        text += (input(text).lower())
    text = input("please enter text ").lower()
