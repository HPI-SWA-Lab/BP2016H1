load-by
hasSingleAssociationNamed: aStringOrSymbol

	^ self associations
		at: aStringOrSymbol asSymbol
		ifPresent: [:association | association isSingle]
		ifAbsent: [false]