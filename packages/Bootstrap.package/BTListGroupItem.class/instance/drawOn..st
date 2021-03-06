drawing
drawOn: aCanvas
	| bordered rounded |
	(self parent notNil and: [self parent isListGroup])
		ifTrue: [
			rounded := {false. false. false. false}.
			bordered := {true. true. false. true}.
			self isFirstChild ifTrue: [
				rounded at: 1 put: true; at: 2 put: true ].
			self isLastChild ifTrue: [
				rounded at: 3 put: true; at: 4 put: true.
				bordered at: 3 put: true ]]
		ifFalse: [
			rounded := {true. true. true. true}.
			bordered := {true. true. true. true} ].

	BTWidget
		drawBackgroundOn: aCanvas
		bounds: self bounds
		colors: (self colorScheme hovered: (hovered or: [active]))
		rounded: rounded
		bordered: bordered