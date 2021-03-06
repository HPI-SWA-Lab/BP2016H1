primitives
primitiveLayoutSetHeight
	<var: #layout type: 'PangoLayout *'>
	<export: true>
	
	| layout height |
	interpreterProxy methodArgumentCount = 2 ifFalse: [ ^interpreterProxy primitiveFail ].
	
	layout := self sqLayoutForHandle: (interpreterProxy stackIntegerValue: 1).
	height := interpreterProxy stackIntegerValue: 0.
	interpreterProxy failed ifTrue: [ ^interpreterProxy primitiveFailFor: 100 ].
	
	self cCode: 'pango_layout_set_height(layout, height < 0 ? height : height * PANGO_SCALE)'.
	
	^interpreterProxy pop: interpreterProxy methodArgumentCount