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

    # =========================================================================================
    # Active state example
    # =========================================================================================

    elif action == 'activatestate':
        import numpy as np

        from pycog import RNN
        from pycog.figtools import Figure

        # Model
        m = p['model']

        # Intensity
        try:
            intensity = float(args[0])
        except:
            intensity = 1

        # Create RNN
        if 'init' in args:
            print("* Initial network.")
            base, ext = os.path.splitext(p['savefile'])
            savefile_init = base + '_init' + ext
            rnn = RNN(savefile_init, {'dt': p['dt']}, verbose=True)
        else:
            rnn = RNN(p['savefile'], {'dt': p['dt']}, verbose=True)

        trial_func = p['model'].generate_trial
        trial_args = {
            'name': 'test',
            'catch': False,
            'intensity': intensity,
        }
        info = rnn.run(inputs=(trial_func, trial_args), seed=p['seed'])

        # Summary
        mean = np.mean(rnn.z)
        std = np.std(rnn.z)
        print("Intensity: {:.6f}".format(intensity))
        print("Mean output: {:.6f}".format(mean))
        print("Std. output: {:.6f}".format(std))

        # Figure setup
        x = 0.12
        y = 0.12
        w = 0.80
        h = 0.80
        dashes = [3.5, 1.5]

        t_forward  = 1e-3 * np.array(info['epochs']['forward']);
        t_stimulus = 1e-3 * np.array(info['epochs']['stimulus']);
        t_reversal = 1e-3 * np.array(info['epochs']['reversal']);

        fig = Figure(w=4, h=3, axislabelsize=7, labelpadx=5, labelpady=5, thickness=0.6,
                     ticksize=3, ticklabelsize=6, ticklabelpad=2)
        plots = {
            'in': fig.add([x, y + 0.72 * h, w, 0.3 * h]),
            'out': fig.add([x, y, w, 0.65 * h]),
            }

        plot = plots['in']
        plot.ylabel('Input', labelpad=7, fontsize=6.5)

        plot = plots['out']
        plot.xlabel('Time (sec)', labelpad=6.5)
        plot.ylabel('Output', labelpad=7, fontsize=6.5)

        # -----------------------------------------------------------------------------------------
        # Input
        # -----------------------------------------------------------------------------------------

        plot = plots['in']
        plot.axis_off('bottom')

        plot.plot(1e-3 * rnn.t, rnn.u[0], color=Figure.colors('red'), lw=0.5)

        # -----------------------------------------------------------------------------------------
        # Output
        # -----------------------------------------------------------------------------------------

        plot = plots['out']

        # Outputs
        colors = [Figure.colors('orange'), Figure.colors('blue')]
        plot.plot(1e-3 * rnn.t, rnn.z[0], color=colors[0], label='Forward module')
        plot.plot(1e-3 * rnn.t, rnn.z[1], color=colors[1], label='Reversal module')
        plot.xlim(1e-3 * rnn.t[0], 1e-3 * rnn.t[-1])
        plot.lim('y', np.ravel(rnn.z), lower=0)

        # Legend
        props = {'prop': {'size': 7}}
        plot.legend(bbox_to_anchor=(1.1, 1.6), **props)


        plot.vline(t_forward[-1], color='0.2', linestyle='--', lw=1, dashes=dashes)
        plot.vline(t_reversal[0], color='0.2', linestyle='--', lw=1, dashes=dashes)

        # Epochs
        plot.text(np.mean(t_forward), plot.get_ylim()[1], 'forward',
                  ha='center', va='center', fontsize=7)
        plot.text(np.mean(t_stimulus), plot.get_ylim()[1], 'stimulus',
                  ha='center', va='center', fontsize=7)
        plot.text(np.mean(t_reversal), plot.get_ylim()[1], 'reversal',
                  ha='center', va='center', fontsize=7)

        if 'init' in args:
            fig.save(path=p['figspath'], name=p['name'] + '_' + action + '_init')
        else:
            fig.save(path=p['figspath'], name=p['name'] + '_' + action)
        fig.close()

    else:
        print("[ {}.do ] Unrecognized action.".format(THIS))
