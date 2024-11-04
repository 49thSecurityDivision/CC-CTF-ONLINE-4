BIN="plain_sight"

priority:
	gcc -O4 "${BIN}".c -o "${BIN}"
	strip "${BIN}"

debug:
	gcc -g "${BIN}".c -o "${BIN}"

clean:
	rm -rf "${BIN}"
