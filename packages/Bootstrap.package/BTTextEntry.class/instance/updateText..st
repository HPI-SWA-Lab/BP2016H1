text
updateText: aString

	super updateText: (aString escapeEntities ifEmpty: [ | secondaryColor |
		secondaryColor := (self colorScheme foreground) printHtmlString.
		'<span color="#', secondaryColor, '66">', self placeholder, '</span>'])