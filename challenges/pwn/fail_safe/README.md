# Prompt 

Rust is memory safe! 

...

Right?

*NOTE*: This challenge will either involve a lot of intuition or a lot of debugging. It is actual memory-safe Rust that was compiled with Rust's distributed tools as of last week. There really isn't a trick here, such as using `unsafe`.

# Category 

PWN

# File to Release 

```
src/main.rs
fail_safe
```

# Remote 

`challenges.carolinacon.org:8001`

# Solution 

We are doing a stack overwrite. Just enter the string `vr0n_the_internzlet_me_in_please` when prompted for input to get the flag.

`cc_ctf{vr0n_really_was_4_g00d_int3rn_huh...}`
