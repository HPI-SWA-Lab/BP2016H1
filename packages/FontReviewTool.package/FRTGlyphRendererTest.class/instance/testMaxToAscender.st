as yet unclassified
testMaxToAscender

	| size |
	size := renderer extentOf: {'C'} size: 1000.
	
	(self expect: size) to equal: 100 @ ((self simpleFontinfo at: 'ascender') - (self simpleFontinfo at: 'descender'))