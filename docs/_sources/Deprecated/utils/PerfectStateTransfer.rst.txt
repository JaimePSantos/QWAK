isStrCospec
===========

For a graph to have PST it needs to obey numerous rules and the first one is that the vertices with PST must be
strongly cospectral. Two vertices a and b are strong cospectral if the characteristic polynomial of the matrix Ma, that has
the colum and row a removed, is equal to the characteristic polynomial of the matrix Mb, that has the column and row b
removed. This is easily checked using SymPy and it is what the function StrCospec does.

Parameters
----------
A : _type_
    _description_
a : _type_
    _description_
b : _type_
    _description_

Returns
-------
_type_
    _description_

isSimplePoles
=============

The second condition for strong cospectral is that the poles of phiab/phi must be simple. This is trickier to check and
it starts by defning a polynomial g(x)=gcd(phi,phiab). Then, there will be no poles if f(x) = phi/g(x) is a polynomial
without repeated roots. This occurs when gcd(f(x),f'(x)) is a constant, then we only need to check the coeeficients and
see if all of them is zero except the last one. This is done by the function SimplePoles.

Parameters
----------
phi : _type_
    _description_
phiab : _type_
    _description_

Returns
-------
_type_
    _description_

sieveEratosthenes
=================

One of the steps requires that we find square-free numbers, that is, numbers that have a prime decomposition with all
primes being unique. Fist we use the Sieve of Eratosthenes, and the corresponding function, to find all primes from 1 to n.
It works by choosing the first prime in the list, in this case 2, then squareing it and removing all its multiples from the
list. The algorithm then choose the next prime and does the same procedure. At the end, we have a list with True at position
i if i+1 is prime and False otherwise.

Parameters
----------
n : _type_
    _description_

Returns
-------
_type_
    _description_

getSquareFree
=============

The function SquareFree gives a list of square-free number from 1 to n in a similar way that we found all primes. The
algorithm get the list of primes from 1 to n, then it start a loop of integers from 2 to n, when i is prime the algorithm
associates False to all multiples of i^2. It returns a list with True (False) in the entry i if i-1 is (not) square free.

Parameters
----------
n : _type_
    _description_

Returns
-------
_type_
    _description_

getEigenSupp
============

Returns the eigenvalue support of the vertex a.

The eigenvalue support of the vertex a is the set of all eigenvalues such that
the projection matrix of the eigenvalue r applied to the vector with 1 in the a-th
entry and zero in all others is not zero.

Parameters
----------
a : int
    The index of the vertex.
eigenvec : numpy.ndarray
    The eigenvectors of the graph.
eigenval : numpy.ndarray
    The eigenvalues of the graph.

Returns
-------
list
    The eigenvalues in the eigenvalue support of the vertex a.

checkRoots
==========

CheckRoots is responsible for checking the second condition for PST which is that all eigenvalues is the eigenvalue support
of a must be all integers or all quadratic integers with the format p+qr*Sqrt(delta)/2, with qr changing from eigenvalue to
to eigenvalue. The frist step is to define h(x) = phi/gcd(phi,phia) that have all its roots in the eigenvalue support of a,
then its degree k will be crucial.
First, we check for integer roots in the interval [-n^4,n^4] that the eigenvalues should be. We check by putting the
value in the loop, i, direct into h(i) and we see if it is equal to zero. If it is, then we check if i is in the
eigenvalue support of a. With both conditions satisfied, it stores 1 to delta and sum one to intRoots.
Then we check if all roots are quadratic integers p+qr*Sqrt(delta)/2. We know that p will be equal to the coefficient
of the second bigest power of h(x). Then, all we need to do is loop through the values of delta in the list of square-free
integers. Then, we loop qr until it is bigger than Sqrt(Tr(A²)) and check if is a root of h(x) and it is also in the
eigenvalue support of a. In case it is true, we store the value of delta and sum one to quadRoots.
Here we check if quadRoots or intRoots are bigger than k, which is the degree of our polynomial h(x). If none of them is
then we know that PST is not possible and we return False.
The time that PST occurs is just pi/g*Sqrt(delta) where g = gcd(theta0 - thetar), i.e. the gcd between all the differences
of the eigenvalue theta0 (the biggest eigenvalue) and all others eigenvalues.

Parameters
----------
A : _type_
    _description_
a : _type_
    _description_
eigenvec : _type_
    _description_
eigenval : _type_
    _description_

Returns
-------
_type_
    _description_

swapNodes
=========

_summary_

Parameters
----------
nodeA : _type_
    _description_
nodeB : _type_
    _description_

Returns
-------
_type_
    _description_

getEigenVal
===========

_summary_

Parameters
----------
D : _type_
    _description_

Returns
-------
_type_
    _description_

