while True:
    n = raw_input('Enter the number of candidates: ')
    try:
        int(n)
    except:
        print 'Sorry, I can only except an ' + '\033[1m' + 'integer' + '\033[0m' + ' for the number of candidates.'
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
    stderrors.append(((votesforcand[i]/votesobs)*(1-votesforcand[i]/votesobs)/votesobs)**.5)
import numpy as np
victories=[0]*numofcand
numOfSims=100000
for i in xrange(numOfSims):
    x=[np.random.normal(meanests[j],stderrors[j]) for j in range(numofcand)]
    s=sum(x)
    xs = [x[j]/s for j in range(numofcand)]
    votes=np.random.multinomial(votestobecast,xs)
    votecount=[votes[j]+votesforcand[j] for j in range(numofcand)]
    m=max(votecount)
    winners=[u for u,k in enumerate(votecount) if k==m]
    if len(winners)==1:
        victories[winners[0]]+=1.0
    else:
        for j in winners:
            victories[j]+=1.0/len(winners)

prctwin = [victories[u]/numOfSims for u in range(numofcand)]
print prctwin
