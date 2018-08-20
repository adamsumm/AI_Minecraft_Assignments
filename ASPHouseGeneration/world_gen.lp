
#const max_width=12.
#const max_height=10.

terrain_type(grass;tree;flower;water;bridge).


width(1..max_width).
height(1..max_height).



1 {terrain(XX,YY,TERRAIN_TYPE) : terrain_type(TERRAIN_TYPE)} 1 :- 
	width(XX), 
	height(YY).
	
	
	
	
neighbors(XX,YY,TYPE, COUNT) :- 
	COUNT =  {terrain(XX-1,YY-1,TYPE);
					terrain(XX,YY-1,TYPE);
					terrain(XX+1,YY-1,TYPE);
					terrain(XX-1,YY,TYPE);
					terrain(XX+1,YY,TYPE);
					terrain(XX-1,YY+1,TYPE);	
					terrain(XX,YY+1,TYPE);
					terrain(XX+1,YY+1,TYPE)},
					terrain(XX,YY,_),					
					terrain_type(TYPE).
					
					
	
immediate_neighbors(XX,YY,TYPE, COUNT) :- 
	COUNT =  {terrain(XX,YY-1,TYPE);
					terrain(XX-1,YY,TYPE);
					terrain(XX+1,YY,TYPE);
					terrain(XX,YY+1,TYPE)},
					terrain(XX,YY,_),					
					terrain_type(TYPE).
					
					
horizontal(XX,YY,start) :- terrain(XX,YY,bridge), terrain(XX-1,YY,grass).
horizontal(XX,YY,start) :- terrain(XX,YY,bridge), terrain(XX+1,YY,grass).
horizontal(XX,YY,mid) :- terrain(XX,YY,bridge), horizontal(XX-1,YY,_).
horizontal(XX,YY,mid) :- terrain(XX,YY,bridge), horizontal(XX+1,YY,_).


vertical(XX,YY,start) :- terrain(XX,YY,bridge), terrain(XX,YY+1,grass).
vertical(XX,YY,start) :- terrain(XX,YY,bridge), terrain(XX,YY-1,grass).
vertical(XX,YY,mid) :- terrain(XX,YY,bridge), vertical(XX,YY-1,_).
vertical(XX,YY,mid) :- terrain(XX,YY,bridge), vertical(XX,YY+1,_).

:- terrain(XX,YY,bridge), not horizontal(XX,YY,_), not vertical(XX,YY,_).
:- terrain(XX,YY,bridge), horizontal(XX,YY,_), vertical(XX,YY,_).
:- horizontal(X1,YY,start), horizontal(X2,YY,start), X1-X2=1.
:- vertical(XX,Y1,start), vertical(XX,Y2,start), Y1-Y2=1.
:- horizontal(XX,Y1,start), horizontal(XX,Y2,start), Y1-Y2=1.
:- vertical(X1,YY,start), vertical(X2,YY,start), X1-X2=1.

:- {terrain(XX,YY,grass)} max_width*max_height*1/2 .

:- {terrain(XX,YY,water)} max_width*max_height*1/6 .
:- {terrain(XX,YY,bridge)} 5 .


:- terrain(XX,YY,flower), neighbors(XX,YY,flower, COUNT), COUNT > 3.

:- terrain(XX,YY,water), neighbors(XX,YY,water, COUNT), COUNT < 4.

:- terrain(XX,YY,bridge), neighbors(XX,YY,water, COUNT), COUNT < 4.


:- terrain(XX,YY,bridge), immediate_neighbors(XX,YY,bridge, B_COUNT), 
	terrain(XX,YY,bridge), immediate_neighbors(XX,YY,grass, G_COUNT), B_COUNT + G_COUNT != 2.
	
	
surrounded_by_water(XX,YY) :-  terrain(XX+1,YY,water),terrain(XX-1,YY,water).
surrounded_by_water(XX,YY) :-  terrain(XX,YY-1,water),terrain(XX,YY-1,water).

:- terrain(XX,YY,bridge), not surrounded_by_water(XX,YY).

:- terrain(XX,YY,bridge), immediate_neighbors(XX,YY,bridge, B_COUNT), B_COUNT < 1.
	
:- {terrain(XX,YY,TERRAIN_TYPE)} 0, terrain_type(TERRAIN_TYPE).

connected(XX,YY) :- terrain(XX,YY,grass).
connected(XX,YY) :- terrain(XX,YY,bridge), 1 {connected(XX,YY-1);
																	connected(XX-1,YY);
																	connected(XX+1,YY);	
																	connected(XX,YY+1)}.
																	
:- terrain(XX,YY,bridge), not connected(XX,YY).

1 {reachable(XX,YY,original) : width(XX), 
	height(YY)} 1.
    
:- reachable(XX,YY,original), not terrain(XX,YY,grass).
reachable(XX,YY) :- reachable(XX,YY,original).

reachable(XX,YY) :- reachable(XX+1,YY), not terrain(XX,YY,water), width(XX), height(YY).
reachable(XX,YY) :- reachable(XX-1,YY), not terrain(XX,YY,water), width(XX), height(YY).
reachable(XX,YY) :- reachable(XX,YY+1), not terrain(XX,YY,water), width(XX), height(YY).
reachable(XX,YY) :- reachable(XX,YY-1), not terrain(XX,YY,water), width(XX), height(YY).


:- terrain(XX,YY,TERRAIN), TERRAIN != water, not reachable(XX,YY).