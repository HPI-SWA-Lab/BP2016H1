converting
jsonWriteOn: aWriteStream

	^ (Dictionary new
		at: 'alignment' put: self alignment asString;
		at: 'fontNameForPango' put: self fontNameForPango;
		at: 'fontId' put: self fontId;
		at: 'pointSize' put: self pointSize;
		at: 'text' put: self text;
		at: 'openTypeFeatures' put: self openTypeFeatures;
		at: 'deletable' put: self deletable;
		at: 'placeholder' put: self placeholder;
		yourself) jsonWriteOn: aWriteStream