BIN="priorities"

"${BIN}":
	gcc -Wall -no-pie "${BIN}".c -o "${BIN}"
	strip "${BIN}"

debug:
	gcc -g "${BIN}".c -o "${BIN}"

clean:
	rm -rf "${BIN}"
