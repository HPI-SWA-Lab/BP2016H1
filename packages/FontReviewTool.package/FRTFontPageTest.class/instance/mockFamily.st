mock-data
mockFamily

	author := FRTUser new username: 'Eva'.

	family := FRTFamily new
		familyName: 'Riblooon';
		previewGlyphs: '';
		standardSampleText: (FRTSampleText new
				text: FRTRichText standardEmptyFamilyText asJsonString;
				title: 'blah';
				shouldBeInOverview: false;
				author: author);
		versionMessages: #();
		author: author;
		yourself.

	family fonts add: (FRTFont new
		fontName: 'HI';
		author: author).

	^ family