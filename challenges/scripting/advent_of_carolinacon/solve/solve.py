with open("../challenge.txt", "r") as file:
    chal = file.readlines()

max_row = 75 - 1 # We are using indexes,
max_col = 75 - 1 # so subtract one

curr_row = 2 - 1
curr_col = 2 - 1

nums = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]

total = 0
for r in range(1, max_row):
    for c in range(1, max_col):
        if chal[r][c] in nums:
            if chal[r-1][c-1] in nums:
                if chal[r-1][c] in nums:
                    if chal[r+1][c+1] in nums:
                        total += 1
                        #print(f"{r+1}x{c+1}: {chal[r][c]}")

print(f"Total: {total}")
