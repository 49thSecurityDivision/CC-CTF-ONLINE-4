# Global Entry 

It is so much cheaper when your time is worth money

# Files To Release 

`global_entry`

`challenges.carolinacon.org:8006`

# Solution 

You need to use a format string to leak an address to overcome ASLR. You do *not* need a stack canary leak, because we can control an overwrite of a Thread Local Storage (TLS) variable. 

Conveniently, the stack canary is also stored in TLS, so if we choose the appropriate offset of TLS, we can make the stack canary the Global Variable value that the program wants to write, which -- conveniently -- is ASCII encode-able.
