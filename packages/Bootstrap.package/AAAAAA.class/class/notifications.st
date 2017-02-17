as yet unclassified
notifications
	| toplevel |
	toplevel := BTTopLevel new.
	
	toplevel add: (BTPage new
		align: #(expand expand);
		add: (((BTButton label: 'Show notification' icon: #flag) do: [ :button |
			button topLevel
				displayNotification: ((BTIcon icon: #life_ring), ' Critical Failure')
				type: #danger ]))).
	
	toplevel displayNotification: 'I''m staying.' type: #success.
	
	[(Delay forSeconds: 2) wait. toplevel displayNotification: ((BTIcon icon: #cloud), ' Hi') type: #warning ] fork.
	
	^toplevel