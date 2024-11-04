BIN="motivation"

"${BIN}":
	gcc -fno-stack-protector -no-pie "${BIN}".c -o "${BIN}"

debug:
	gcc -g -fno-stack-protector -no-pie "${BIN}".c -o "${BIN}"

clean:
	rm -rf "${BIN}"
