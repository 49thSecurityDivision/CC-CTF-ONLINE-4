BIN="meditation" 

"${BIN}":
	cargo build --release
	cp -f ./target/release/${BIN} ./

debug:
	cargo build
	cp -f ./target/debug/${BIN} ./

clean:
	cargo clean
	rm -rf ./${BIN} || :
