from math import sqrt, ceil, pow

import numpy as np
from sympy import gcd, div, Float


def isStrCospec(A, a, b):
    """For a graph to have PST it needs to obey numerous rules and the first one is that the vertices with PST must be
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
    """
    Ma = A.minor_submatrix(a, a)
    Mb = A.minor_submatrix(b, b)
    Mab = Ma.minor_submatrix(b - 1, b - 1)

    phi = A.charpoly()
    phia = Ma.charpoly()
    phib = Mb.charpoly()
    phiab = Mab.charpoly()

    if phia != phib or not isSimplePoles(phi, phiab):
        return False
    else:
        return True


def isSimplePoles(phi, phiab):
    """The second condition for strong cospectral is that the poles of phiab/phi must be simple. This is trickier to check and
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
    """
    gx = gcd(phi, phiab)
    fx, r = div(phi, gx)
    fx_der = fx.diff()
    great = gcd(fx, fx_der)
    coeffs = great.all_coeffs()
    del coeffs[len(coeffs) - 1]
    for coeff in coeffs:
        if coeff > 0:
            return False
    return True


def sieveEratosthenes(n):
    """One of the steps requires that we find square-free numbers, that is, numbers that have a prime decomposition with all
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
    """
    isPrime = np.full([n, 1], True)
    for i in range(2, ceil(sqrt(n)) + 1):
        if isPrime[i - 1]:
            for j in range(int(pow(i, 2)), n + 1, i):
                isPrime[j - 1] = False
    return isPrime


def getSquareFree(n):
    """The function SquareFree gives a list of square-free number from 1 to n in a similar way that we found all primes. The
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
    """
    isSqrFree = np.full([n, 1], True)
    isPrime = sieveEratosthenes(n)
    sqrFreeList = []
    for i in range(2, n + 1):
        if isPrime[i - 1]:
            for j in range(int(pow(i, 2)), n + 1, int(pow(i, 2))):
                isSqrFree[j - 1] = False
    for i in range(n):
        if isSqrFree[i]:
            sqrFreeList.append(i + 1)
    return sqrFreeList

def getEigenSupp(a, eigenvec, eigenval):
    """Returns the eigenvalue support of the vertex a.

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
    """
    supp = []
    for i in range(len(eigenval)):
        if abs(eigenvec[a][i]) > 1e-10:
            supp.append(round(eigenval[i],5))
    return supp

def checkRoots(A, a, eigenvec, eigenval):
    """CheckRoots is responsible for checking the second condition for PST which is that all eigenvalues is the eigenvalue support
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
    """
    supp = getEigenSupp(a, eigenvec, eigenval)
    Ma = Ma = A.minor_submatrix(a, a)
    phi = A.charpoly()
    phia = Ma.charpoly()
    h, r = div(phi, gcd(phi, phia))
    k = h.degree()
    intRoots = 0
    for i in range(-len(eigenval) ** 4, len(eigenval) ** 4 + 1):
        if h(i) == 0 and i in supp:
            delta = 1
            intRoots += 1
    quadRoots = 0
    sqrtFreeInt = getSquareFree(int((4 * A**2).trace()))
    p = h.all_coeffs()[1]
    deltaTmp = 0
    for deltaS in sqrtFreeInt:
        q = 0
        while (p + q * sqrt(deltaS) / 2) <= sqrt(int(((A**2).trace()))):
            # print(f'\np + q * sqrt(deltaS) / 2 = {Float(p + q * sqrt(deltaS) / 2, 3)}\nsupp = {supp}\nCondition: {Float(p + q * sqrt(deltaS) / 2, 3) in supp}\n')
            if (
                h(p + q * sqrt(deltaS) / 2) == 0
                and Float(p + q * sqrt(deltaS) / 2, 3) in supp
            ):
                quadRoots += 1
                deltaTmp = deltaS
            q += 1
    # print(quadRoots < k, intRoots < k)
    if quadRoots > 0:
        delta = deltaTmp
    if quadRoots < k and intRoots < k:
        return False, 0, 0
    diffs = []
    for i in range(len(supp)):
        diffs.append((max(supp) - supp[i]) / np.sqrt(delta))

    g = 0
    for diff in diffs:
        # print(f'g = {g}, diff = {diff}')
        g = np.gcd(Float(g), Float(diff))
    return True, g, delta


def swapNodes(nodeA, nodeB):
    """_summary_

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
    """
    nodeA = nodeA + nodeB
    nodeB = nodeA - nodeB
    nodeA = nodeA - nodeB
    return nodeA, nodeB


def getEigenVal(D):
    """_summary_

    Parameters
    ----------
    D : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    eigenVal = []
    for i in range(len(D.col(0))):
        temp = D.col(i)[i]
        if abs(temp) < 0.0000001:
            temp = 0
        eigenVal.append(temp)
    return eigenVal
