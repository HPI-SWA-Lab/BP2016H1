as yet unclassified
label: aString action: aSymbol
	^self new
		action: aSymbol;
		add: (BTLabel text: aString)