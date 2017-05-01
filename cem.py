#import numpy as np
import os,sys,random
from math import sqrt, log, pi, exp, sin, cos

def rand_normal(mu,sigma):
	rand1 = random.uniform(0.,1.)
	rand2 = random.uniform(0.,1.)
	z = sqrt( -2.0 * log(rand1) ) * sin ( 2.0 * pi * rand2 )
	return mu + z * sigma

def critic_emulator(commands): # returns one value e.g. grababble probability
	x = commands
	return exp(-(x[0]-5.)**2) + exp(-(x[1]-3.)**2)

def mean(v,idx=None):
	if idx==None:
		v = [v]
		idx = 0
	s = 0.
	c = 0
	for k in v:
		s += k[idx]
		c += 1
	return s/c

def var(v,idx=None):
	if idx==None:
		v = [v]
		idx = 0
	s = 0.
	c = 0
	for k in v:
		s += k[idx] * k[idx]
		c += 1
	return sqrt(s-mean(v,idx)**2)/c

def cem(f):
	# Setup
	max_step = 100000
	N_samples = 100
	N_survive = 10
	epsilon = 1e-3
	# define
	step = 0
	# initialize
	p1_mu = 100
	p1_sigma2 = 100**2
	p2_mu = 100
	p2_sigma2 = 100**2

	while step<max_step and p1_sigma2>epsilon and p2_sigma2>epsilon:
		commands = [[rand_normal(p1_mu,sqrt(p1_sigma2)),rand_normal(p2_mu,sqrt(p2_sigma2))] for _ in range(N_samples)]
		grabProb = [f(x) for x in commands]
		sortedCommands = [commands[grabProb.index(k)] for k in sorted(grabProb)[::-1]]
		p1_mu     = mean(sortedCommands[:N_survive],0)
		p1_sigma2 = var (sortedCommands[:N_survive],0)
		p2_mu     = mean(sortedCommands[:N_survive],1)
		p2_sigma2 = var (sortedCommands[:N_survive],1)
		print p1_mu,p2_mu,p1_sigma2,p2_sigma2
		step += 1

if __name__=="__main__":
	cem(f=critic_emulator)
	
