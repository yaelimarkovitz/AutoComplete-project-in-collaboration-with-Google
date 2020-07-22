class AutoCompleteData:
    def __init__(self, complete, sorce, offset, score):
        self.complete_sent = complete
        self.sorce_file = sorce
        self.offset = offset
        self.score = score

    def print(self,text):
        first_index = self.complete_sent.find(text)
        end_index = first_index+len(text)
        print(self.complete_sent + " ( the source from " + str(self.sorce_file) + " in line " + str(self.offset) +"score : "+str(self.score)+ " )")
