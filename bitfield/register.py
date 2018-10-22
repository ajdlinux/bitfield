# Utility to decode register values
# Copyright © 2006-2018 Jeremy Kerr and contributors
# Released under the GNU General Public License version 2 or later

class Bitfield(object):
	def __init__(self, bits, name):
		self.bits = bits
		self.name = name
		self.values = {}

	def width(self):
		return len(self.bits)

	def add_value(self, value, description):
		self.values[int(value, 0)] = description

	def mask(self, reg, value):
		ret = 0
		out_len = len(self.bits)

		if reg.bit_order == reg.bit_0_is_msb:
			bit_pairs = zip(self.bits, range(0, out_len))
		else:
			bit_pairs = zip(self.bits, range(out_len - 1, -1, -1))

		for (in_bit, out_bit) in bit_pairs:
			# shift this bit down to the LSB (and mask the rest)
			i = (value >> (reg.width - in_bit - 1)) & 1
			# shift back to the output position in the field
			i <<= out_len - out_bit - 1
			ret |= i
		return ret

	def value(self, value):
		if value in self.values:
			return self.values[value]
		return None

	@staticmethod
	def mask_and_shift_to_bits(width, mask, shift):
		bits = []
		val = mask << shift
		for i in range(0, width):
			if mask & (1 << i):
				bits.insert(0, width - i - 1 - shift)
		return bits

	@staticmethod
	def mask_to_bits(width, mask):
		return Bitfield.mask_and_shift_to_bits(width, mask, 0)

	@staticmethod
	def parse_bitfield(line, reg):
		a = line.split(None, 1)
		if len(a) != 2:
			return None
		(range_str, name) = a

		bits = []
		for s in range_str.split(','):
			if ':' in s:
				bounds = [reg.bit_number(int(n))
					  for n in s.split(':', 1)]
				start = min(bounds)
				end = max(bounds)
				bits.extend(range(start, end + 1))
			elif '<<' in s:
				(mask, shift) = [int(s.strip())
                                                 for s in s.split('<<')]
				bits.extend(Bitfield.mask_and_shift_to_bits( \
					reg.width, mask, shift))
			elif s.startswith('&'):
				mask = int(s[1:], 0)
				bits.extend(Bitfield.mask_to_bits(reg.width, \
							mask))
			else:
				bits.append(reg.bit_number(int(s)))

		return Bitfield(bits, name)



	@staticmethod
	def parse_value(line):
		a = line.split(None, 1)
		if len(a) != 2:
			return None
		return a

class Register(object):
	bit_0_is_msb = 0
	bit_0_is_lsb = 1

	def __init__(self, id):
		self.id = id
		self.fields = []
		# set defaults
		self.name = None
		self.bit_order = self.bit_0_is_msb
		self.width = 64

	def add_field(self, field):
		self.fields.append(field)

	def decode(self, value, ignore_zero):
		field_width = (self.width + 3) // 4
		name_width = max([len(f.name) for f in self.fields])

		str = "0x%0*lx [%d]\n" % (field_width, value, value)

		for field in self.fields:
			v = field.mask(self, value);
			if ignore_zero and v == 0:
				continue
			desc = field.value(v)
			if desc is not None:
				str += "%*s: 0x%x [%s]\n" \
					% (name_width, field.name, v, desc)
			else:
				str += "%*s: 0x%x\n" \
					% (name_width, field.name, v)
		return str

	def bit_number(self, number):
		if self.bit_order == self.bit_0_is_lsb:
			number = self.width - number - 1
		return number
