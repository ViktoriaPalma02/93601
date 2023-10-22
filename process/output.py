from textblob import TextBlob
from textblob import Word

#This file is a sample of code that will show the process of the code
#retrive data from databsae

'''
class Author:
    def __str__(self, first, last, id, credential ):
        self.first = first
        self.last = last
        self.id = id
        self.credential = credential'''


class Professional:
    def __init__(self, input):
        self.input = input

    def correctspelling(self):
        count = 0
        word_list = self.input.split()
        for i in range(0, len(word_list)):
            evaluate_word = Word(word_list[i]).spellcheck()
            a = list(evaluate_word[0])
            count += a[1]
        input_length = len(word_list)
        correct_spelling = count/input_length
        return correct_spelling
    
    def consistent_spelling(self):
        pass

    def correct_punctuality(self):
        pass

    def correct_grammar(self):
        pass



#sampletextA = Author("Viktoria", "Palma", "", "", "True")
sampletextP = "Banana's are yellow jruits with block seeds in thee middle. While some like it, the taste is often too mushy to enjoy. "

#print(sampletextP.correctspelling())
grape = Professional(sampletextP)
print(grape.correctspelling())
#print(grape.input)

'''class Evaluate:
    def __init__(self, spell, polarity, subjectivity):
        self.spell = spell
        self.polarity = polarity
        self.subjectivity = subjectivity

    def sentiment(self, polarity, subjectivity):
        pass
        


#sample 
resultA = Evaluate()'''