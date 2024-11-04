# Prompt 

*Get ready*, sit back, relax, and watch the following video: https://www.youtube.com/watch?v=inpok4MKVLM

Come back once you are fully refreshed and get the flag!

# Category

RE

# File to Release

```
meditation
```

# Remote

`N/A`

# Solution

Just start Wireshark or strace and let the challenge run for the length of the associated YouTube video. The program makes a call to `russian-bot.net`. Going to that URL gives the flag.

`cc_ctf{4ll_it_t4k35_is_peace_and_relaxation}'
