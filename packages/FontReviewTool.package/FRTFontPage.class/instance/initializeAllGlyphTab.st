initialize-release
initializeAllGlyphTab

	gridWidget := (FRTGlyphGridWidget newWithRenderer: self renderer) minSize: 200 asPoint.
	^ allGlyphsTab := BTPage column
		minSize: 100 asPoint;
		expand: true;
		add: (BTScrollArea new add: gridWidget)