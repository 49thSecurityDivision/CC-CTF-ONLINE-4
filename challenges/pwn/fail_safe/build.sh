#!/bin/sh 

cargo build --release
cp ./target/release/fail_safe ./
