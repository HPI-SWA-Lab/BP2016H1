initialize-release
initialize

	super initialize.
	
	familyList := BTPage column.
	
	self
		padding: BTWidget spacing * 3;
		add: ((BTButton label: 'Create New Family' icon: #plus)
			when: #clicked send: #openCreateFamilyPage to: self;
			align: #(end center));
		add: (BTScrollArea new
			add: familyList)