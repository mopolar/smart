from mongoframes import *



class ShortLink(Frame):

	_fields = {
		'slug',
		'ios',
		'android',
		'web'
	}