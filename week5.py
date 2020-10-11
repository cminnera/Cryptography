# Clare Minnerath
# Week 5 assignment
# compute discrete log % prime p

import math  # Use sqrt, floor
import functools # Use reduce (Python 2.5+ and 3.x)


def populate_table(h,g,B,p):
    table = {}
    g_inv = inverse_mod(g,p)
    h_g_inv = h * g % p
    for x in range(B):
        h_g_inv = h_g_inv * g_inv % p 
        table[h_g_inv] = x
    return table

def search_table(g,B,p,table):
    g_pB = power_mod(g,B,p)
    for x in range(B):
        temp = power_mod(g_pB,x,p)
        if temp in table:
            return x, table[temp]

def power_mod(b,e,n):
    """power_mod(b,e,n) computes the eth power of b mod n.
    (Actually, this is not needed, as pow(b,e,n) does the same thing for positive integers.
    This will be useful in future for non-integers or inverses.)"""
    if e<0: # Negative powers can be computed if gcd(b,n)=1
        e = -e
        b = inverse_mod(b,n)
    accum = 1; i = 0; bpow2 = b
    while ((e>>i)>0):
        if((e>>i) & 1):
            accum = (accum*bpow2) % n
        bpow2 = (bpow2*bpow2) % n
        i+=1
    return accum

def inverse_mod(a,n):
    """inverse_mod(b,n) - Compute 1/b mod n."""
    (g,xa,xb) = xgcd(a,n)
    if(g != 1): raise ValueError("***** Error *****: {0} has no inverse (mod {1}) as their gcd is {2}, not 1.".format(a,n,g))
    return xa % n

def xgcd(a,b):
    """xgcd(a,b) returns a tuple of form (g,x,y), where g is gcd(a,b) and
    x,y satisfy the equation g = ax + by."""
    a1=1; b1=0; a2=0; b2=1; aneg=1; bneg=1
    if(a < 0):
        a = -a; aneg=-1
    if(b < 0):
        b = -b; bneg=-1
    while (1):
        quot = -(a // b)
        a = a % b
        a1 = a1 + quot*a2; b1 = b1 + quot*b2
        if(a == 0):
            return (b, a2*aneg, b2*bneg)
        quot = -(b // a)
        b = b % a;
        a2 = a2 + quot*a1; b2 = b2 + quot*b1
        if(b == 0):
            return (a, a1*aneg, b1*bneg)

def main():
    p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
    g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
    h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333
    B = pow(2,20)

    LHS_table = populate_table(h,g,B,p)
    x0, x1 = search_table(g,B,p,LHS_table)
    print("x = ", B*x0 + x1)

if __name__ == "__main__":
    main()

