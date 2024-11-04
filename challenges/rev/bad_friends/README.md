# BF

Don't take it personally...

# Solution

https://kvbc.github.io/bf-ide/ was the IDE used to create and debug this challenge. We replicated this challenge from our friends at ImaginaryCTF after competing in that CTF earlier this year.

The code is straight forward once you understand it, but understanding it is the hard part, so YMMV.

Essentially, each "section" is split into 4 parts:

1. Accept input character
1. Choose a number of rounds
1. Increment a separate register for that many rounds by the second number of increments (clearer explanation later)
1. Subtract until the value is 0 (clearer explanation later)

So, let's take the first "section" as an example. When you split the code into these 4 rules, it looks like the following:

``
,              // Accept input character 
>>+++++++++++  // 11 "rounds" stored in second register (11 is the number of 'plus signs')
[<+++>-]       // 11 rounds multiplied by 3 stored in the first register (here, 3 is the number of 'plus signs')
<
[-<+>]         // Add character value to rounds * first register
<------------------------------------------------------------------------------------------------------------------------------------------ // Subtract by 139 (138 is our target, but we have a dangling 1)
[><]           // Check that the registers we care about equal 0
```

This is still a but confusing, so let's take the last example and add actual input. 

If your input is the character 'i' then the decimal value of that input is 105. If you multiply the number of rounds by the given increment (3, in this case), you get 11 x 3 == 33.
105 ('i') + 33 == 138. 
The decrement value is 139, but we had a dangling 1, so the number we actually want to hit is 138, which is what we have if we input the character 'i'.

So, 139 - dangling 1 - 138 == 0, which is our goal for each "section".

Basically, you just have to separate out each section and you can reverse the math to determine each character.
