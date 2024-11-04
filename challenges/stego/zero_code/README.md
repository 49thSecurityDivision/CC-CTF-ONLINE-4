# Zero Code 

Zero amount of the code will tell you the answer

# Solution 

Byte analysis of the binary indicates there are several `0x20` bytes in the ELF file that make it unusable. If you open the binary is an easy-to-format hex edit, such as `ghex`, you can manipulate the file until the bytes make ASCII art of the flag. Check the screenshot for an example. 

`cc_ctf{code_zero}`
