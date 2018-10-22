# Utility to decode register values
# Copyright © 2006-2018 Jeremy Kerr and contributors
# Released under the GNU General Public License version 2 or later

import os
import sys

from getopt import getopt, GetoptError
from .config import ConfigurationError, parse_all_configs

# List of paths to look for configuration files. If a directory is specified,
# it will be (recursively) scanned for .conf files.
configs = ["/etc/bitfield.d", "/etc/bitfield",
		os.path.join(os.getenv("HOME"), ".bitfield.d"),
		os.path.join(os.getenv("HOME"), ".bitfield.conf")]

def usage(prog):
	print("Usage: %s <-l> | <-s pattern> | [-n] register [value...]" % prog)

def list_regs(regs):
	for (id, r) in regs.items():
		print("%18s : %s" % (id, r.name))

def search_regs(regs, str):
	return dict((k, regs[k]) for k in regs \
			if str.lower() in regs[k].name.lower() + k.lower())

def decode_value(reg, value, options):
	try:
		i = int(value, 0)
	except ValueError as e:
		print("error: invalid value '%s'" % value)
		return

	if i > ((1 << reg.width) - 1):
		print(("error: value '%s' is too large " + \
			"for %d-bit register '%s'") % (value, reg.width, reg.id))
		return

	print(reg.decode(i, options['non-zero']))

def main():
	try:
		(opts, args) = getopt(sys.argv[1:], "hlns:", \
			["help", "list", "non-zero", "search="])
	except GetoptError:
		usage(sys.argv[0])
		return 1

	try:
		regs = parse_all_configs(configs)
	except ConfigurationError as e:
		print("Error parsing configuration file %s:\n\t%s" % \
			(e.file, e.message))
		return 1

	if regs == {}:
		print("No configuration available")
		return 1

	options = {}
	options['non-zero'] = False

	for o, a in opts:
		if o in ("-h", "--help"):
			usage(sys.argv[0])
			return

		if o in ("-l", "--list"):
			list_regs(regs)
			return

		if o in ("-s", "--search"):
			list_regs(search_regs(regs, a))
			return

		if o in ("-n", "--non-zero"):
			options['non-zero'] = True

	if not args:
		usage(sys.argv[0])
		return 1

	reg_id = args.pop(0)
	if reg_id not in regs:
		print("No such register '%s'" % reg_id)
		return 1

	reg = regs[reg_id]
	print("decoding as %s" % reg.name)

	if args:
		value_iter = args.__iter__()
	else:
		value_iter = iter(sys.stdin.readline, '')

	try:
		for value in value_iter:
			decode_value(reg, value.strip(), options)
	except KeyboardInterrupt as e:
		pass

	return 0

if __name__ == "__main__":
	sys.exit(main())
