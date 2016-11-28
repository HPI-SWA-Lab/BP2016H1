accessing
initialize
	super initialize.
	self
		startPoint: KRNBezierControlPointMorph new;  
		addMorph: self startPoint;
		
		controlPoint1: KRNBezierControlPointMorph new;
		addMorph: self controlPoint1;
		
		controlPoint2: KRNBezierControlPointMorph new;
		addMorph: self controlPoint2;
		
		endPoint: KRNBezierControlPointMorph new;
		addMorph: self endPoint;
		
		extent: 200@200;
		color: Color white.
		
	self startPoint position: 50@100.
	self controlPoint1 position: 50@50.
	self controlPoint2 position: 100@50.
	self endPoint position: 100@100