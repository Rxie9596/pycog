"""
Some commonly used functions for defining a task.

"""
from __future__ import division

import numpy as np

#-----------------------------------------------------------------------------------------
# Define E/I populations
#-----------------------------------------------------------------------------------------

def generate_ei(N, pE=0.8):
    """
    E/I signature.

    Parameters
    ----------

    N : int
        Number of recurrent units.

    pE : float, optional
         Fraction of units that are excitatory. Default is the usual value for cortex.

    """
    assert 0 <= pE <= 1

    Nexc = int(pE*N)
    Ninh = N - Nexc

    idx = range(N)
    EXC = idx[:Nexc]
    INH = idx[Nexc:]

    ei       = np.ones(N, dtype=int)
    ei[INH] *= -1

    return ei, EXC, INH

#-----------------------------------------------------------------------------------------
# Functions for defining task epochs
#-----------------------------------------------------------------------------------------

def get_idx(t, interval):
    start, end = interval

    return list(np.where((start < t) & (t <= end))[0])

def get_epochs_idx(dt, epochs):
    t = np.linspace(dt, epochs['T'], int(epochs['T']/dt))
    #assert t[1] - t[0] == dt, "[ tasktools.get_epochs_idx ] dt doesn't fit into T."

    return t, {k: get_idx(t, v) for k, v in epochs.items() if k != 'T'}

#-----------------------------------------------------------------------------------------
# Functions for generating epoch durations that are multiples of the time step
#-----------------------------------------------------------------------------------------

def uniform(rng, dt, xmin, xmax):
    return (rng.uniform(xmin, xmax)//dt)*dt

def truncated_exponential(rng, dt, mean, xmin=0, xmax=np.inf):
    while True:
        x = rng.exponential(mean)
        if xmin <= x < xmax:
            return (x//dt)*dt

def truncated_normal(rng, dt, mean, sigma, xmin=-np.inf, xmax=np.inf):
    while True:
        x = rng.normal(mean, sigma)
        if xmin <= x < xmax:
            return (x//dt)*dt

#-----------------------------------------------------------------------------------------
# Functions for generating orientation tuning curves
#-----------------------------------------------------------------------------------------

def deg2rad(s):
    return s*np.pi/180

def vonMises(s, spref, g=1, kappa=5, b=0, convert=True):
    arg = s - spref
    if convert:
        arg = deg2rad(arg)

    return g*np.exp(kappa*(np.cos(arg)-1)) + b

#-----------------------------------------------------------------------------------------
# Convert batch index to condition
#-----------------------------------------------------------------------------------------

def unravel_index(b, dims):
    return np.unravel_index(b, dims, order='F')

#-----------------------------------------------------------------------------------------
# Functions for generating connection matrices
#-----------------------------------------------------------------------------------------

def generate_Crec(ei, p_exc=1, p_inh=1, rng=None, seed=1, allow_self=False):
    if rng is None:
        rng = np.random.RandomState(seed)

    N    = len(ei)
    exc, = np.where(ei > 0)
    inh, = np.where(ei < 0)

    C = np.zeros((N, N))
    for i in exc:
        C[i,exc] = 1*(rng.uniform(size=len(exc)) < p_exc)
        if not allow_self:
            C[i,i] = 0
        C[i,inh]  = 1*(rng.uniform(size=len(inh)) < p_inh)
        C[i,inh] *= np.sum(C[i,exc])/np.sum(C[i,inh])
    for i in inh:
        C[i,exc] = 1*(rng.uniform(size=len(exc)) < p_exc)
        C[i,inh] = 1*(rng.uniform(size=len(inh)) < p_inh)
        if not allow_self:
            C[i,i] = 0
        C[i,inh] *= np.sum(C[i,exc])/np.sum(C[i,inh])
    C /= np.linalg.norm(C, axis=1)[:,np.newaxis]

    return C

#-----------------------------------------------------------------------------------------
# Callbacks
#-----------------------------------------------------------------------------------------

def correct_2afc_bias(trials, z, rmin=0.45, rmax=0.55):
    """
    Use to correct bias in the psychometric curve.

    """
    ends    = [len(trial['t'])-1 for trial in trials]
    choices = [np.argmax(z[ends[i],i]) for i, end in enumerate(ends)]

    r = choices.count(0)/choices.count(1)
    x = max(min(1/(1 + r), rmax), rmin)
    print(r, [x, 1-x])
    #return None
    return [x, 1-x]

#-----------------------------------------------------------------------------------------
# Performance measure
#-----------------------------------------------------------------------------------------

def performance_2afc(trials, z):
    ends    = [len(trial['t'])-1 for trial in trials]
    choices = [np.argmax(z[ends[i],i]) for i, end in enumerate(ends)]
    correct = [choice == trial['info']['choice']
               for choice, trial in zip(choices, trials) if trial['info']]

    return 100*sum(correct)/len(correct)

def performance_2afc_min_condition(trials, z):
    ends    = [len(trial['t'])-1 for trial in trials]
    choices = [np.argmax(z[ends[i],i]) for i, end in enumerate(ends)]

    correct = {}
    for choice, trial in zip(choices, trials):
        if not trial['info']:
            continue

        cond = tuple(trial['info'].values())
        correct.setdefault(cond, []).append(choice == trial['info']['choice'])
    correct = [sum(c)/len(c) for c in correct.values()]

    return 100*min(correct)

# perfomance mesure forword to reversal
# added by yu xie
# TODO add lower bound to indexing z[rev_starts[i]:rev_starts[i] + 5, i, 1]
# rev_starts[i] + 5 may exceed trial length
def perfomance_f2r(trials, z):

    for_ends = []
    for trial in trials:
        if trial['info']:
            for_ends.append(trial['e']['forward'][-1])
        else:
            for_ends.append(None)

    rev_starts = []
    for trial in trials:
        if trial['info']:
            rev_starts.append(trial['e']['reversal'][0])
        else:
            rev_starts.append(None)

    for_dif = []
    for i, end in enumerate(for_ends):
        if for_ends[i]:
            prebound = max(for_ends[i] - 5 , 0)
            for_dif.append(np.mean(z[prebound:for_ends[i]+1, i, 0])
                           - np.mean(z[prebound:for_ends[i]+1, i, 1]))

    rev_dif = []
    for i, end in enumerate(rev_starts):
        if rev_starts[i]:
            rev_dif.append(np.mean(z[rev_starts[i]:rev_starts[i] + 5, i, 0])
                           - np.mean(z[rev_starts[i]:rev_starts[i] + 5, i, 1]))


    for_dif = np.array(for_dif)
    rev_dif = np.array(rev_dif)
    diff = for_dif - rev_dif

    return 100*(np.mean(diff)/1.6)