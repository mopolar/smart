# This file contains generic functions/utils used in the app
import random, string



def make_slug():
	"""Returns a random alphanumeric string"""
	return ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(6))
