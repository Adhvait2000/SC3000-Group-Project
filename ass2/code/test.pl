% Define gender
female(queen_elizabeth).
female(princess_ann).
male(prince_charles).
male(prince_andrew).
male(prince_edward).

% Define current crrown
crown(queen_elizabeth).

% Define parent relationships
parent(queen_elizabeth, prince_charles).
parent(queen_elizabeth, princess_ann).
parent(queen_elizabeth, prince_andrew).
parent(queen_elizabeth, prince_edward).
parent(queen_elizabeth, future_princess).



% Define birth order
% born_after(X,Y) --> X is born before Y --> X is older than Y
born_after(queen_elizabeth, prince_charles).
born_after(prince_charles, princess_ann).
born_after(princess_ann, prince_andrew).
born_after(prince_andrew, prince_edward).
born_after(prince_edward, future_princess).


% Determining birth born_after transitivity
born_after_x(A,B) :- born_after(A,B).

born_after_x(A,C) :-
  born_after(A,B), born_after_x(B,C).


% Checks if same gender
same_gender(X,Y) :- (male(X), male(Y)); (female(X), female(Y)).

% Ensures same gender, and second arg is younger sibling
same_g_younger(X,Y) :- same_gender(X,Y), born_after_x(X, Y).

% Ensures that the first arg is male and second arg is female.
diff_g(X,Y) :- male(X), female(Y).

% Checks if a list contains males before females
order([H,S|T]) :- order_r(H, [S,T]).
order([_]).
order([]).


order_r_helper(X,Y) :- (same_g_younger(X,Y); diff_g(X,Y)), not(crown(X)), not(crown(Y)).

order_r(H, [S,T]) :-
  order_r_helper(H,S), order_r(S,T).

% order_r(H,[T]) :- order_r_helper(H, T).
order_r(H,T) :- order_r_helper(H, T).
% order_r(_).