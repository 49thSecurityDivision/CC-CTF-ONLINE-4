#!/usr/bin/python

import random

from wonderwords import RandomSentence

# Create RandomSentence class
s = RandomSentence()

# Reset count to 0
count = 0

# Declare questions
questions = {
        0: "How many words appear in this story?",
        1: "How many sentences appear in this story?",
        2: "How many words shorter than XXX characters appear in this story?",
        3: "How many sentences with fewer than XXX words appear in this story?",
        4: "What is word XXX of sentence YYY?",
        5: "What is the first word of sentence XXX?",
        6: "What is the last word of sentence XXX?",
        }
    
# Helper functions 
def split_words(story):
    return story.split(" ")[:-1]

def split_sentences(story):
    return story.split(". ")[:-1]
    
# Solve questions 

# How many words appear in this story?
def solve_0(story):
    return str(len(split_words(story)))

# How many sentences appear in this story?
def solve_1(story):
    return str(len(split_sentences(story)))

# How many words shorter than XXX characters appear in this story?
def solve_2(story, length):
    answer = []
    words = split_words(story)

    for w in words:
        w = w.strip('.')
        if len(w) < length:
            answer.append(w)
            
    return str(len(answer))

# How many setences with fewer than XXX words appear in this story?
def solve_3(story, word_count):
    answer = []
    sentences = split_sentences(story)
    
    for sentence in sentences:
        words = sentence.split(" ") 
        if len(words) < word_count:
            answer.append(sentence)
        
    return str(len(answer)) 

# What is word XXX of sentence YYY?
def solve_4(story, sentence, word):
    sentences = split_sentences(story)
    words = sentences[sentence - 1].split(" ")
    return words[word - 1]

# What is the first word of sentence XXX?
def solve_5(story, sentence):
    sentences = split_sentences(story)
    return sentences[sentence - 1].split(" ")[0]

# What is the last word of sentence XXX?
def solve_6(story, sentence):
    sentences = split_sentences(story)
    return sentences[sentence - 1].split(" ")[-1:][0]

def prep_question(q_num, story, num_sentences, num_words):
    question = questions[q_num]
    
    if 0 == q_num: # nuffin..
        question = question
        answer = solve_0(story)
        
    if 1 == q_num: # nuffin..
        question = question
        answer = solve_1(story)
        
    if 2 == q_num: # No constraint needed
        num = random.randint(1, 40)
        question = question.replace("XXX", str(num))
        answer = solve_2(story, num)
        
    if 3 == q_num: # Self imposed limit of exactly 5 words per sentence
        more_or_less = random.randint(1, 10000) % 2
        if more_or_less == 0:
            num = random.randint(0, 5) # Answer will be 0
        else:
            num = random.randint(6, 1000) # Answer will be all sentences
            
        question = question.replace("XXX", str(num))
        answer = solve_3(story, num)
        
    if 4 == q_num: # Constrain sentence *and* word count
        word     = random.randint(1, num_words)
        sentence = random.randint(1, num_sentences)
        
        question = question.replace("XXX", str(word))
        question = question.replace("YYY", str(sentence))
        
        answer = solve_4(story, sentence, word)
        
    if 5 == q_num: # Constraint sentence count
        sentence = random.randint(1, num_sentences)
        
        question = question.replace("XXX", str(sentence))
        answer = solve_5(story, sentence)
    if 6 == q_num: # Constrain sentence count
        sentence = random.randint(1, num_sentences)
        
        question = question.replace("XXX", str(sentence))
        answer = solve_6(story, sentence)

    return question, answer

while count < 1000:
    answer = ""
    story = ""
    user_input = ""
    
    num_sentences = random.randint(1, 20)
    num_words     =  5 # words per sentence
    for i in range(0, num_sentences):
        story += s.sentence()
        story += " "
        
    q_num = random.randint(0,6)
    question, answer = prep_question(q_num, story, num_sentences, num_words)
    answer = answer.strip('\n')

    print("Here's the story:\n")
    print(story)
    print("\n" + question)
    r = input(user_input)

    if (r == answer):
        count += 1
    else:
        #count = 0
        print("FAILED!")
        exit(1)

if (count == 1000):
    print("cc_ctf{just_take_a_look_its_in_a_book}")
