from termcolor import colored, cprint
import sys
from colors import  *
class AutoCompleteData:
    def __init__(self, complete, sorce, offset, score):
        self.complete_sent = complete
        self.sorce_file = sorce
        self.offset = offset
        self.score = score

    def print(self,text):
        first_index = (self.complete_sent.lower()).find(text)
        # print(first_index)
        end_index = first_index+len(text)
        if(first_index==-1):
            print(self.complete_sent+" ( the source from " + str(self.sorce_file) + " in line " + str(self.offset) +" score : "+str(self.score)+ " )")
        else:
            print(self.complete_sent[:first_index] ,end=" ")
            sys.stdout.write(BLUE)
            print(text,end="")
            sys.stdout.write(RESET)
            print(self.complete_sent[end_index:] + " ( the source from " + str(self.sorce_file) + " in line " + str(self.offset) +" score : "+str(self.score)+ " )" )
