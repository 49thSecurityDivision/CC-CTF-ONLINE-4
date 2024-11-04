# Prompt

"The files are *in* the computer..."

# Category 

RE

# File to Release

```
mugatu
```

# Remote

`N/A`

# Solution

The program creates the flag on the machine it runs on. Debugging allows you to grab this in real time before the program deletes it, but you have to patch the program or hook the ptrace functionality to avoid the anti-debugging measures

If you get around that and debug the constructors, you can eventually stop and see that a file named `/tmp/shhhhhhh` is created, and holds the contents: `cc_ctf{you_found_me...}`

Also, if you've patched the bianry appropriately, `strace` will just print the flag.
