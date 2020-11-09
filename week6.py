# Clare Minnerath
# week 6 assignment
# factoring poorly defined N values

from Crypto.Hash import SHA256
import gmpy2

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


# problem 1 : |p-q| < 2N^1/4
oneN = 179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581

A = gmpy2.isqrt(oneN)+1
x = gmpy2.isqrt(A**2 - oneN)
# p = A-x, q = A+x
onep = A-x
oneq = A+x
print(onep)
print()

# problem 2 : |p-q| < 2^11N^1/4
N = 648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877

A = gmpy2.isqrt(N)+1
correctA = False
while not correctA:
    x = gmpy2.isqrt(A**2-N)
    p = A - x
    q = A + x
    if p*q == N:
        print(p)
        print()
        break
    A += 1

# problem 3 : |3p-2q| < N^1/4
N = 720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929

twoA = gmpy2.isqrt(24*N)+1
x = gmpy2.isqrt(twoA**2 - 24*N)
# 2q = A-x, 3p = A+x
q = (twoA+x)//4
p = (twoA-x)//6

if p*q == N:
    print(min(p,q))
    print()

# problem 4 : decrypt ct that uses problem 1 N & PKCSv1.5
phiN = (onep-1)*(oneq-1)
e=65537
# d found using gcd(phiN, e)
d = 15901287978999413029444103622387317669077639420371013629157181141513592652158568184727012903658813528491037910547521854815931164999641308185976587386289355866678615944319681939473842195092207377098269996346353744109549011306581302639353136684586796229221071755410527734011645528084075140176976118813890397473
ct = 22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540
msg = power_mod(ct, d, oneN)
msg = hex(msg)
for i in range(len(msg)-1):
    if msg[i]=='0' and msg[i+1]=='0':
        msg = msg[i+2:]
        break
msg = bytes.fromhex(msg)
print(msg.decode())