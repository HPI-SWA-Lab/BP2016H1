initialize-release
initialize

	| fontSelectButton resetFontButton |
	super initialize.
	
	titleLabel := BTLabel new subHeading.
	
	authorLabel := BTLabel new
		align: #(end center);
		secondary.
	
	sampleTextWidget := FRTRichTextEditor new
		when: #saved send: #saveSampleText: to: self;
		yourself.
	
	fontSelectCompletion :=  FRTFontPicker new
		placeholder: 'Select Font for all Paragraphs ...';
		when: #confirmed send: #applyName:font: to: self.
	
	fontSelectButton := ((BTButton label: 'Apply Font')
		colorType: #primary;
		when: #clicked send: #triggerConfirmed to: fontSelectCompletion).
	
	resetFontButton := ((BTButton label: 'Reset to System Font')
		colorType: #secondary;
		when: #clicked send: #resetFont to: self).

	self
		add: (BTPage row
			add: titleLabel;
			add: authorLabel);
		add: (BTPage row
			add: fontSelectCompletion;
			add: fontSelectButton;
			add: resetFontButton);
		add: sampleTextWidget