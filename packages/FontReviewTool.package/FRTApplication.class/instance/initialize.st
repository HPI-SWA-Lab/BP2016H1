initialize-release
initialize

	super initialize.
	self backend: FRTHttpBackend new.
	
	FRTUser resetAvatarCache.
	
	sidebar := FRTSidebar new.
	
	self contentContainer add: sidebar at: 1.
	self showSidebar: false.
	self showHeader: false.
	
	BTPangoTextLayout available ifTrue: [BTPangoTextLayout refreshFontCache]