# Utility to decode register values
# Copyright © 2006-2018 Jeremy Kerr and contributors
# Released under the GNU General Public License version 2 or later

import os

from pyparsing import Literal, Word, ZeroOrMore, Group, Dict, Optional, \
        printables, ParseException, restOfLine

from .register import Bitfield, Register

class ConfigurationError(Exception):
	def __init__(self, file, message):
		self.file = file
		self.message = message

def parse_config(bnf, regs, file):
	f = open(file)

	tokens = bnf.parseString(f.read())

	order_map = {'bit-0-is-lsb':	Register.bit_0_is_lsb,
			'bit-0-is-msb':	Register.bit_0_is_msb,
			'ibm':		Register.bit_0_is_msb,
			'default':	Register.bit_0_is_msb}

	for tok in tokens:
		ts = tok.asList()
		id = ts.pop(0)

		if id in regs:
			raise ConfigurationError(file,
				"Register %s is already defined" % id)

		reg = Register(id)

		alias_id = None
		fields = []

		for t in ts:
			if t[0] == 'name':
				name = t[1]
				reg.name = name.strip()
			elif t[0] == 'width':
				reg.width = int(t[1])
			elif t[0] == 'field':
				f = Bitfield.parse_bitfield(t[1], reg)
				if f is None:
					raise ConfigurationError(file,
						"Invalid field in %s" % id)
				fields.append(f)
			elif t[0] == 'value':
				if len(fields) == 0:
					raise ConfigurationError(file,
						"No field for value in %s" % id)
				v = Bitfield.parse_value(t[1])
				if v is None:
					raise ConfigurationError(file,
						"Invalid value in %s" % id)

				fields[-1].add_value(v[0], v[1])
			elif t[0] == 'order':
				if len(fields) != 0:
					raise ConfigurationError(file,
						("bit order defined after " \
						+ "fields in %s") % id)

				order_str = t[1].strip().lower()
				order_str = order_str.replace(' ', '-')

				if order_str not in order_map:
					raise ConfigurationError(file,
						"Invalid bit order %s in %s" % \
						(order_str, id))
				reg.bit_order = order_map[order_str]

			elif t[0] == 'alias':
				alias_id = t[1].strip()

		if alias_id is not None:
			if reg.name is not None or fields != []:
				raise ConfigurationError(file, ("Definiton " \
					+ "for %s is an alias, but has other " \
					+ "attributes") % id)

			if alias_id not in regs:
				raise ConfigurationError(file, "Aliasing "
					"non-existent register %s (from %s)" \
					% (alias_id, id))

			reg = regs[alias_id]
			continue

		if reg.name is None or reg.name == '':
			raise ConfigurationError(file,
				"No name for entry %s" % id)

		if len(fields) == 0:
			raise ConfigurationError(file,
				"Register %s has no fields" % id)

		for f in fields:
			reg.add_field(f)

		regs[id] = reg

def parse_config_dir(data, dir, fnames):
	(bnf, regs) = data
	for fname in fnames:
		full_fname = os.path.join(dir, fname)

		if fname.endswith('.conf'):
			parse_config(bnf, regs, full_fname)

def parse_all_configs(configs):
	regs = {}

	# set up the bnf to be used for each file
	lbrack = Literal("[").suppress()
	rbrack = Literal("]").suppress()
	colon  = Literal(":").suppress()
	semi   = Literal(";")

	comment = semi + Optional(restOfLine)

	nonrbrack = "".join([c for c in printables if c != "]"]) + " \t"
	noncolon  = "".join([c for c in printables if c != ":"]) + " \t"

	sectionDef = lbrack + Word(nonrbrack) + rbrack
	keyDef = ~lbrack + Word(noncolon) + colon + restOfLine

	bnf = Dict(ZeroOrMore(Group(sectionDef + ZeroOrMore(Group(keyDef)))))
	bnf.ignore(comment)

	# bundle into a single var that can be passed to os.path.walk
	conf_data = (bnf, regs)

	for conf in configs:
		if not os.path.exists(conf):
			continue
		if os.path.isdir(conf):
			for dirpath, dirnames, filenames in os.walk(conf):
				parse_config_dir(conf_data, dirpath, filenames)
		else:
			parse_config(bnf, regs, conf)
	return regs

