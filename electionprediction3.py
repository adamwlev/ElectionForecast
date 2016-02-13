from __future__ import division
while True:
    n = raw_input('Enter the number of candidates: ')
    try:
        int(n)
    except:
        print 'Sorry, I can only except an ' + '\033[1m' + 'integer' + '\033[0m' + ' for the number of candidates.'
        continue
    if int(n)>3:
        print "Sorry, I'm programmed to handle at most 3 candidates at most at the moment.."
        continue
    numofcand=int(n)
    break
namesofcand = []
for i in range(numofcand):
    namesofcand.append(raw_input('Enter candidate number ' + str(i+1) + "'s name (nicknames are a-ok): "))

votesforcand = []
for i in range(numofcand):
    while True:
        v = raw_input('Enter the number of votes collected for ' + namesofcand[i] + ': ')
        try:
            int(v)
        except:
            print '\033[1m' + 'Integers' + '\033[0m' + ' only silly!'
            continue
        votesforcand.append(int(v))
        break
votesobs=int(sum(votesforcand))

while True:
    p = raw_input('Enter the percentage of votes observed thus far (the estimate will do): ')
    try:
        int(p)
    except:
        print 'Only the integer please.'
        continue
    prctobs = int(p)/float(100)
    break

if numofcand==2:
    while True:
        p = raw_input('Enter the prior distribution alpha first: ')
        try:
            float(p)
        except:
            print 'Only the float please.'
            continue
        alpha = float(p)
        break

    while True:
        p = raw_input('Now the beta: ')
        try:
            float(p)
        except:
            print 'Only the float please.'
            continue
        beta = float(p)
        break
else:
    a=[0,0,0]
    for i in range(3):
        while True:
            p = raw_input('Enter the hyper parameter for candidate '+ str(i+1) + ', please: ')
            try:
                float(p)
            except:
                print 'Only the float please.'
                continue
            a[i] = float(p)
            break

votestobecast=int(votesobs/prctobs-votesobs)

    
import sympy as sy
import itertools as it
from functools import reduce
import operator
V=votestobecast
if numofcand==2:
    g=int((votestobecast+votesobs)/2+1-votesforcand[0])
    prob=0
    n=votesforcand[0]
    N=votesobs
    for k in range(g,votestobecast+1):
        prob+=sy.mpmath.binomial(V,k)*sy.mpmath.beta(k+alpha+n,V-k+beta+N-n)/sy.mpmath.beta(alpha+n,beta+N-n)
    print [float(prob),float(1-prob)]
else:
    a=[a[i]+votesforcand[i] for i in range(3)]
    A=sum(a)
    prob=[0,0,0]
    for i in it.product(range(V+1),repeat=3):
        if sum(i)!=V:
            continue
        votecount=[votesforcand[:][j]+i[j] for j in range(3)]
        for c in [u for u,k in enumerate(votecount) if k==max(votecount)]:
            l=1/float(len([u for u,k in enumerate(votecount) if k==max(votecount)]))
            prob[c]+=l*V*sy.mpmath.beta(A,V)/reduce(operator.mul,[i[r]*sy.mpmath.beta(a[r],i[r]) for r in range(3) if i[r]!=0],1)
    s=sum(prob)
    print [float(prob[i]/s) for i in range(3)],s
                
            
