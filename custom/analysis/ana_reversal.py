"""
Analyze worm reversal task.

"""
from __future__ import division

import cPickle as pickle
import os
import sys
from   os.path import join

import numpy as np

from pycog          import fittools, RNN, tasktools
from pycog.figtools import Figure

THIS = "custom.analysis.ana_reversal"

#=========================================================================================
# Setup
#=========================================================================================

# File to store trials in
def get_trialsfile(p):
    return join(p['trialspath'], p['name'] + '_trials.pkl')

# Load trials
def load_trials(trialsfile):
    with open(trialsfile) as f:
        trials = pickle.load(f)

    return trials, len(trials)

#=========================================================================================

def run_trials(p, args):
    """
    Run trials.

    """
    # Model
    m = p['model']

    # ntrials: Number of trials for each condition
    try:
        ntrials = int(args[0])
    except:
        ntrials = 100

    # TODO use different ncondition
    ntrials *= m.nconditions + 1

    # RNN
    rng = np.random.RandomState(p['seed'])
    rnn = RNN(p['savefile'], {'dt': p['dt']}, verbose=False)




#=========================================================================================

def do(action, args, p):
    """
    Manage tasks.

    """
    print("ACTION*:   " + str(action))
    print("ARGS*:     " + str(args))

    #-------------------------------------------------------------------------------------
    # Trials
    #-------------------------------------------------------------------------------------

    if action == 'trials':
        run_trials(p, args)

    #-------------------------------------------------------------------------------------

    else:
        print("[ {}.do ] Unrecognized action.".format(THIS))
