# Prompt

You've heard of Advent of Code? Well, this is like that...

Only cooler...

Because...

It's us doing it, I guess...

Anyways, here is the challenge:

You are given a file with a "square" of either numeric digits or "X"s (i.e., the rows and columns are the same size and there are the same number of both rows and columns).

Your job is to tell me how many numbers have numbers to their top left, bottom right, and top.

For example:

```
0X7X
098X
X876
X101
```

The answer to this "square" would be "2". This is because on row 3, both the numbers "8" and "7" have a digit and not an "X" above them, above them and to the left, and below them to the right.

Here is another example just to make sure you get it:

```
21XXX
X81X7
X9187
XXX81
X1XX0
```

The answer to this "square" would be "3". This is because on row 2, "8" has a number above it, above it and to the left, and below it to the right. Secondly, on row 3, "1" meets the same conditions and on row 4, "8" is the same.

As a small hint, numbers on the top, bottom, and edge column rows can not meet the required condition by design.

# Category

Scripting

# Files to Release

```
output.txt
```

# Remote

`N/A`

# Solve

Just solve the challenge.

`3678`
