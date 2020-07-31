$Title  ese504_project

  Sets
       i   'polls'     / i1*i16 /
       j   'voters'  /j1*j13689/
       l  'x_y'  / x,y /;

  Parameter a(i) 'capacity of poll i';
  a(i) = 857;

  Parameter b(j) 'demand of each voter';
  b(j) = 1;

  Table g(i,l)  'distance of each polling place from origin (UL corner), x represents row coord, y represents column coord'
                     x             y      
    i1               0.2866    0.8912      
    i2               1.2787    0.0928      
    i3               0.2622    0.1722       
    i4               0.3213    0.5631
    i5               0.6408    0.0768
    i6               0.0562    0.2690
    i7               0.7780    0.2730 
    i8               0.2172    0.5438
    i9               0.3427    0.0104
    i10              0.1413    0.7794
    i11              1.1127    0.1311
    i12              1.3519    0.0721
    i13              0.3746    0.7613
    i14              0.3601    0.5868     
    i15              0.3232    0.6314
    i16              0.3672    0.9751
 ;

  Scalar r 'rideshare cost per mile' /.92/;
  Scalar q 'rideshare base fare' /1.38/;
  Scalar f 'rideshare cost per minute translated to per mile' /.96/;
      
  Parameter c(i,j)  'cost to take voter j to poll i';
  c(i,j) = (r+f)*(sqrt(sqr(g(i,'x') - (0.013608*(floor((ord(j)-1)/117)))) + sqr(g(i,'y') - (0.013608*(mod(ord(j)-1,117))))));

  Variables
       x(i,j)  'assignment of poll i to voter j, either 0 or 1'
       z       'total cost covered by rideshare' ;

  Positive Variable x;

  Equations
       cost        'define objective function'
       supply(i)   'observe supply limit at poll i'
       demand(j)   'satisfy demand for voter j' ;

  cost ..        z  =e=  (q*13689) + sum((i,j), c(i,j)*x(i,j)) ;

  supply(i) ..   sum(j, x(i,j))  =l=  a(i) ;
  demand(j) ..   sum(i, x(i,j))  =g=  b(j) ;

  Model ese504_project /all/ ;

*==========================
option lp=cplex;

$onecho > cplex.opt
objrng all
rhsrng all
$offecho
ese504_project.optfile=1;
* the lines between $onecho and $offecho produce a file called cplex.opt
* the line objrng all asks for the ranges of validity of all obj. fn. coefficients
* the line rhsrng all asks for the ranges of validity of all right hand side coefficients
* the line transport.optfile says that the ranging should be done for the model transport
*==========================

  Solve ese504_project using lp minimizing z ;

  Display x.l, x.m;

  file output /output.txt/,
      results /results.txt/;
  put output;
  put /'Poll capacity'/;
  loop(i, put @3, i.tl, @15, a(i)/);
  put /'Voter demand'/;
  loop(j, put @3, j.tl, @15, b(j)/);

  put results;
  put /'Model Results'/;
  loop((i,j), put i.tl, @12, j.tl, @24, x.l(i,j):8:4/);
  put /'Optimal Cost'/;
  put z.l;
