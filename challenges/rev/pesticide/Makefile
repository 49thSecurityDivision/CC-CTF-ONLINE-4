BIN="pesticide"

"${BIN}":
	gcc -masm=intel -o "${BIN}" "${BIN}".c

debug:
	gcc -g -masm=intel -o "${BIN}" "${BIN}".c

no-break:
	sed 's/__asm__("int 3");/\/\/__asm__("int 3");/' "${BIN}".c > "${BIN}"_no_break.c
	gcc -g -masm=intel -o "${BIN}"_no_break "${BIN}"_no_break.c
	
clean:
	rm -rf ./"${BIN}"
	rm -rf ./"${BIN}"_no_break
