writing
testWriteFalse
	| expectedResult testInput |
	 
	expectedResult := '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <false/>
</plist>'.
	
	testInput := KRNPList new 
		content: false;
		yourself.
	
	self
		assert: (self helperTestParsePListToXMLString: testInput)
		equals: (self helperTestParseStringToXMLString: expectedResult)