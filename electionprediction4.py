from __future__ import division
import numpy as np

def run_intro():
	while True:
	    n = raw_input('Enter the number of candidates: ')
	    try:
	        int(n)
	    except:
	        print 'Sorry, I can only except an ' + '\033[1m' + 'integer' + '\033[0m' + ' for the number of candidates.'
	        continue
	    if int(n) < 2:
	    	print 'Integers greater or equal to 2 please.'
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
	        if int(v) < 0:
	        	print 'No negative numbers please'
	        	continue
	        votesforcand.append(int(v))
	        break
	votesobs=int(sum(votesforcand))

	while True:
	    p = raw_input('Enter the percentage of votes observed thus far (the estimate will do): ')
	    try:
	        float(p)
	    except:
	        print 'Please enter only a number between 0.0001 and 99.9999'
	        continue
	    if float(p) < 0.0001 or float(p) > 99.9999:
	    	print 'Please enter only a number between 0.0001 and 99.9999'
	    	continue
	    prctobs = int(p)/float(100)
	    break

	if numofcand==2:
	    while True:
	        p = raw_input('''Enter the prior distribution alpha first in the beta distribution that represents the liklihood
	        				of a vote going candidate 1's way: ''')
	        try:
	            float(p)
	        except:
	            print 'Only the float please.'
	            continue
	        if float(p)<0:
	        	print 'Must be positive.'
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
	        if float(p)<0:
	        	print 'Must be positive.'
	        	continue
	        beta = float(p)
	        break
	else:
	    a=[0]*numofcand
	    for i in range(numofcand):
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

	return (numofcand,votestobecast,votesforcand,a)

def run_sim(tup,nsim):
	numofcand,votestobecast,votesforcand,a = tup
	a = np.array(a) + np.array(votesforcand)
	ps = np.random.dirichlet(a,nsim)
	wins = np.zeros(numofcand)
	for i in xrange(nsim):
		wins[np.random.multinomial(1,ps[i,:],nsim).sum(0).argmax()] += 1
	return wins/nsim

def main():
	print run_sim((4,230000,[700,699,698,653],[0,0,0,0]),10000)
	#run_sim(run_intro(),10000)

if __name__ == '__main__':
	main()