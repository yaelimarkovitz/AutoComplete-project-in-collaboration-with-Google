class AutoCompleteData:
    def __init__(self, complete, sorce, offset, score):
        self.complete_sent = complete
        self.sorce_file = sorce
        self.offset = offset
        self.score = score

    def print(self):
        print("sentence: " + self.complete_sent + str(self.sorce_file))
