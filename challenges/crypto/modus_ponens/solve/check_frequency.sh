#!/bin/sh

#cat decrypted_answer.txt | tr '[:upper:][:lower:]' '[:lower:][:lower:]' | grep -o . | sort | uniq -c > frequency.txt
cat encrypted_challenge.txt | tr '[:upper:][:lower:]' '[:lower:][:lower:]' | grep -o . | sort | uniq -c > frequency.txt
