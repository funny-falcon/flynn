#!/usr/bin/env python3

import pprint
import argparse
import sys

import flynn
import kugel

argparser = argparse.ArgumentParser()
argparser.add_argument("file", nargs="?", default=sys.stdin.buffer.raw)

args = argparser.parse_args()

file = args.file
if isinstance(file, str):
	file = open(file, "rb")

def search(f, needle):
	buf = f.read(len(needle))
	while buf != needle:
		r = f.read(1)
		if not r:
			raise EOFError()
		buf = buf[1:] + r

while True:
	try:
		search(file, b"\x1b\x1b\x1b\x1b\x01\x01\x01\x01")
	except EOFError:
		break
	while True:
		try:
			msg = flynn.load(file)
		except flynn.InvalidSMLError:
			print("Invalid SML!")
			break
		if msg == flynn.EndOfMessage:
			print("End of message")
			break
		pprint.pprint(msg)
		kugel.rotz(msg)

