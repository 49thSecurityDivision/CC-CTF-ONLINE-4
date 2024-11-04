#!/usr/bin/python

import random
from pwn import *

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
    return story.split(" ")

def split_sentences(story):
    return story.split(". ")
    
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
    return words[word - 1].split(".")[0]

# What is the first word of sentence XXX?
def solve_5(story, sentence):
    sentences = split_sentences(story)
    return sentences[sentence - 1].split(" ")[0]

# What is the last word of sentence XXX?
def solve_6(story, sentence):
    sentences = split_sentences(story)
    return sentences[sentence - 1].split(" ")[-1:][0].split(".")[0]

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

def get_num(question, skip):
    for word in question.split(" "):
        try:
            num = int(word)
            if skip:
                skip = False
                continue
            else:
                return num
        except:
            continue

    return None

def you_lose():
    print("SOMETHING WENT WRONG")

#p = process([ "python3", "../story_time.py" ]);
p = remote("challenges.carolinacon.org", 8005)
while True:
    answer = ""
    story = ""
    question = ""
    num = 0
    word_num = 0
    skip = False

    print(p.recvline())
    print(p.recvline())
    story = p.recvline().strip().decode()
    print(story)
    question = p.recvuntil(b'?').strip().decode()
    print(question)


    if "How many words appear in this story" in question: # 0
        print("how many words question")
        answer = solve_0(story)

    elif "How many sentences appear" in question: # ------- 1
        print("how many sentences question")
        answer = solve_1(story)

    elif "shorter" in question: # ------------------------- 2
        print("shorter question")
        num = get_num(question, skip)
        if num is None:
            you_lose()
        answer = solve_2(story, num)

    elif "sentences with fewer than" in question: # ------- 3
        print("fewer than question")
        num = get_num(question, skip)
        if num is None:
            you_lose()
        answer = solve_3(story, num)

    elif "What is word " in question: # ------------------- 4
        print("which word question")
        word_num = get_num(question, skip)
        if word_num is None:
            you_lose()

        skip = True
        question = question[:-1]
        num = get_num(question, skip)
        if num is None:
            you_lose()
        skip = False

        answer = solve_4(story, num, word_num)

    elif "first word of sentence" in question: # ---------- 5
        print("first word question")
        question = question[:-1]
        num = get_num(question, skip)
        if num is None:
            you_lose()
        answer = solve_5(story, num)

    elif "last word of sentence" in question: # ----------- 6
        print("last word question")
        question = question[:-1]
        num = get_num(question, skip)
        if num is None:
            you_lose()
        answer = solve_6(story, num)

    print(p.recvline())
    print(answer)

    p.sendline(answer.encode())
