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
votesobs=float(sum(votesforcand))

while True:
    p = raw_input('Enter the percentage of votes observed thus far (the estimate will do): ')
    try:
        int(p)
    except:
        print 'Only the integer please.'
        continue
    prctobs = int(p)/float(100)
    break

meanests = []
stderrors = []
votestobecast = int(votesobs/prctobs-votesobs)
for i in range(numofcand):
    phat=votesforcand[i]/votesobs
    meanests.append(phat)
    stderrors.append((phat*(1-phat)/votesobs)**.5)

import numpy as np
import math
def Phi(x):
    # constants
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911

    # Save the sign of x
    sign = 1
    if x < 0:
        sign = -1
    x = abs(x)/math.sqrt(2.0)

    # A&S formula 7.1.26
    t = 1.0/(1.0 + p*x)
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)

    return 0.5*(1.0 + sign*y)

def phi(x):
    return 1/(2*math.pi)**.5*math.exp(-x*x*.5)

def integrate(f,a,b,N):
    x=np.linspace(a,b,N)
    return np.trapz([f(i) for i in x],x)

## true pdf of max of two Nrv
def Z(x,mux,sigx,muy,sigy,p):
    yn = (x-muy)/sigy
    xn = (x-mux)/sigx
    pd = (1-p*p)**.5
    return 1/sigy*phi(yn)*Phi((xn-p*yn)/pd)+1/sigx*phi(xn)*Phi((yn-p*xn)/pd)

## approx. of pdf of max of two Nrv using first two moments
def D(mux,sigx,muy,sigy,p):
    a=(sigx*sigx+sigy*sigy-2*p*sigx*sigy)**.5
    alpha=(mux-muy)/a
    Pa=Phi(alpha)
    Pna=Phi(-1*alpha)
    pa=phi(alpha)
    mud=mux*Pa+muy*Pna+a*pa
    sigd=((sigx*sigx+mux*mux)*Pa+(sigy*sigy+mux*mux)*Pna+(mux+muy)*a*pa-mud*mud)**.5
    return (mud,sigd)

numofsims=100000
p=np.zeros([numofcand,numofsims],dtype=float)
for i in range(numofsims):
    nrv=[]
    for j in range(numofcand):
        nrv.append(np.random.normal(meanests[j],stderrors[j]))
    s=sum(nrv)
    nrvs=[k/s for k in nrv]
    p[:,i]=nrvs

mmat=np.transpose(np.matrix(meanests))*np.matrix(meanests)
cov=-1*votestobecast*(np.cov(p)+mmat)+votestobecast*votestobecast*np.cov(p)
cov+=np.matrix(np.diag(np.array(meanests)*votestobecast))
means=(votestobecast*np.array(meanests)+np.array(votesforcand))
cor=np.divide(cov,np.sqrt(np.transpose(np.matrix(np.diag(cov)))*np.matrix(np.diag(cov))))

if numofcand==2:
    odds1=Phi((means[0]-means[1])/(np.sum(np.diag(cov))-2*cov[0,1])**.5)
    odds2=1-odds1
    print [odds1,odds2]
elif numofcand==3:
    max01=D(means[0],(np.diag(cov)[0])**.5,means[1],(np.diag(cov)[1])**.5,cor[0,1])
    max02=D(means[0],(np.diag(cov)[0])**.5,means[2],(np.diag(cov)[2])**.5,cor[0,2])
    max12=D(means[1],(np.diag(cov)[1])**.5,means[2],(np.diag(cov)[2])**.5,cor[1,2])
    odds0=Phi((means[0]-max12[0])/(np.diag(cov)[0]+max12[1]-2*min([cov[0,1],cov[0,2]]))**.5)
    odds1=Phi((means[1]-max02[0])/(np.diag(cov)[1]+max02[1]-2*min([cov[1,0],cov[1,2]]))**.5)
    odds2=Phi((means[2]-max01[0])/(np.diag(cov)[2]+max01[1]-2*min([cov[2,0],cov[2,1]]))**.5)
    s=sum([odds0,odds1,odds2])
    print [odds0/s,odds1/s,odds2/s]
