# Prompt 

I invented a new way to prevent debugging!

I just wrote what debuggers normally do into the binary itself!

Good luck...

# Category

RE

# Files to Release

```
pesticide
```

# Remote

`N/A`

# Solve

You *can* solve this manually, but I deliberately made the flag extra long to discourage this. 

The intended solution is to write a script that replaces all of the `int 3` instructions with `nop`s or write a script that pulls the character bytes out. If you use the `nop` method, you can just run the program normally, and add a break point at the final `puts` statement to see the flag on the stack. For reasons I did not look into, the flag does not 100% print to the terminal correctly, which I expect will throw many users off -- but, the flag bytes are in the binary itself, so it seems fair to me.

`cc_ctf{1_h0p3_y0u_scr1pt3d_th15_1nst34d_0f_m4nu4lly_TRYING_t0_retype_this_entire_fl4g_b3c4use_th4t_w0uld_have_t4k3n_a_v3ry_l0ng_tim3!}`
