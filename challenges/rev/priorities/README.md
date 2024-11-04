# Prompt 

"If you don't have time, you don't have priorities" - Tim Ferris

# Category 

RE

# Files to Release

```
priorities
```

# Remote

`challenges.carolinacon.org:8010`

# Solve

The `ANSWER` environment variable should be set to 0x44332211 or 1144201745 (the same value in hex or decimal). We can determine this because this value is used as SRAND, so the result will be deterministic. This is easier to solve if you debug the constructors, but you technically don't have to.

The answer in decimal is 1995583173. Entering this prints the flag. 

`cc_ctf{s0m3b0dyKN0W$th31rPR10R1T13S}`
