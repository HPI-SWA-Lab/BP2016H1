as yet unclassified
rejectsEvent: anEvent
	" since we can have overlapping contours at any point, we have to make sure the initial
	  mousedown doesn't get absorbed by an otherwise empty sibling curve "
	
	anEvent type = #mouseDown ifFalse: [^ false].
	self submorphsDo: [:segment | (segment rejectsEvent: anEvent) ifFalse: [^ false]].
	^ true