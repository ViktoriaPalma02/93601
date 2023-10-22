from textblob import Word

#find spelling of each word
count = 0
user_input = input("Please input a sentence\n")
word_list = user_input.split()
for i in range(0, len(word_list)):
    evaluate_word = Word(word_list[i]).spellcheck()
    a = list(evaluate_word[0])
    count += a[1]

#produce percentage of correct spelling from input
input_length = len(word_list)
correct_spelling = count/input_length
print(correct_spelling)
