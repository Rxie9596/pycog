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

# File to store sorted trials in
def get_sortedfile_stim_onset(p):
    return join(p['trialspath'], p['name'] + '_sorted_stim_onset.pkl')

# File to store d'
def get_dprimefile(p):
    return join(p['datapath'], p['name'] + '_dprime.txt')

# File to store selectivity
def get_selectivityfile(p):
    return join(p['datapath'], p['name'] + '_selectivity.txt')

def safe_divide(x):
    if x == 0:
        return 0
    return 1/x

# Define "active" units
def is_active(r):
    return np.std(r) > 0.1

# Nice colors to represent coherences, from http://colorbrewer2.org/
colors = {
        1: '#4292c6'
        }


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

    ntrials *= m.nconditions

    # RNN
    rng = np.random.RandomState(p['seed'])
    rnn = RNN(p['savefile'], {'dt': p['dt']}, verbose=False)

    # Trials
    w = len(str(ntrials))
    trials = []
    backspaces = 0
    try:
        for i in xrange(ntrials):
            b = i % m.nconditions
            # All conditions
            intensity = m.intensity_range[b]

            # Trial
            trial_func = m.generate_trial
            trial_args = {
                'name': 'test',
                'catch': False,
                'intensity': intensity,
            }
            info = rnn.run(inputs=(trial_func, trial_args), rng=rng)

            # Display trial type
            s = ("Trial {:>{}}/{}: intentsity: {:>+3}"
                 .format(i + 1 , w, ntrials, info['intensity']))
            sys.stdout.write(backspaces * '\b' + s)
            sys.stdout.flush()
            backspaces = len(s)

            # Save
            dt = rnn.t[1] - rnn.t[0]
            step = int(p['dt_save'] / dt)
            trial = {
                't': rnn.t[::step],
                'u': rnn.u[:, ::step],
                'r': rnn.r[:, ::step],
                'z': rnn.z[:, ::step],
                'info': info
            }
            trials.append(trial)
    except KeyboardInterrupt:
        pass
    print("")

    # Save all
    filename = get_trialsfile(p)
    with open(filename, 'wb') as f:
        pickle.dump(trials, f, pickle.HIGHEST_PROTOCOL)
    size = os.path.getsize(filename) * 1e-9
    print("[ {}.run_trials ] Trials saved to {} ({:.1f} GB)".format(THIS, filename, size))

#=========================================================================================

def sort_trials_stim_onset(trialsfile, sortedfile):

    # Load trials
    trials, ntrials = load_trials(trialsfile)

    # Get unique conditions
    conds = []
    for trial in trials:
        info = trial['info']
        conds.append(info['intensity'])
    conds = list(set(conds))

    #-------------------------------------------------------------------------------------
    # Prepare for averaging
    #-------------------------------------------------------------------------------------

    # Number of units
    nunits = trials[0]['r'].shape[0]

    # assume all trials has the same stimlus length
    # # stimulus time

    # Number of time points
    idx1   = np.where(trials[0]['t'] <= trials[0]['info']['epochs']['stimulus'][0])[0][-1] + 1
    idx2   = np.where(trials[0]['t'] <= trials[0]['info']['epochs']['stimulus'][1])[0][-1]
    sti_t  = trials[0]['t'][idx1:idx2+1]
    sti_t  = sti_t - sti_t[0]
    dt     = sti_t[1] - sti_t[0]

    forward  = [np.ptp(trial['info']['epochs']['forward']) for trial in trials]
    idx      = np.argmax(forward)
    trial    = trials[idx]
    t        = trial['t']
    w        = np.where(t <= trial['info']['epochs']['forward'][1])[0][-1]
    for_t    = trial['t'][:w+1]
    for_t    = for_t - for_t[-1] - dt + + sti_t[0]

    reversal = [np.ptp(trial['info']['epochs']['reversal']) for trial in trials]
    idx      = np.argmax(reversal)
    trial    = trials[idx]
    t        = trial['t']
    w1       = np.where(t <= trial['info']['epochs']['reversal'][0])[0][-1] + 1
    w2       = np.where(t <= trial['info']['epochs']['reversal'][1])[0][-1]
    rev_t    = trial['t'][w1:w2+1]
    rev_t    = rev_t - rev_t[0] + dt + sti_t[-1]

    t         = np.concatenate((for_t,sti_t,rev_t))
    for_ntime = len(for_t)
    sti_ntime = len(sti_t)
    rev_ntime = len(rev_t)
    ntime     = for_ntime + sti_ntime + rev_ntime

    #-------------------------------------------------------------------------------------
    # Average across conditions
    #-------------------------------------------------------------------------------------

    sorted_trials_for   = {c: np.zeros((nunits, for_ntime)) for c in conds}
    ntrials_by_cond_for = {c: np.zeros(for_ntime) for c in conds}

    sorted_trials_sti   = {c: np.zeros((nunits, sti_ntime)) for c in conds}
    ntrials_by_cond_sti = {c: np.zeros(sti_ntime) for c in conds}

    sorted_trials_rev   = {c: np.zeros((nunits, rev_ntime)) for c in conds}
    ntrials_by_cond_rev = {c: np.zeros(rev_ntime) for c in conds}

    sorted_trials   = {c: np.zeros((nunits, ntime)) for c in conds}
    ntrials_by_cond = {c: np.zeros(ntime) for c in conds}
    for trial in trials:
        info  = trial['info']
        c = info['intensity']

        t_i = trial['t']

        w_i = np.where(t_i <= trial['info']['epochs']['forward'][1])[0][-1]
        sorted_trials_for[c][:,-(w_i+1):] += trial['r'][:,:w_i+1]
        ntrials_by_cond_for[c][-(w_i+1):] += 1

        w1_i = np.where(t_i <= trial['info']['epochs']['stimulus'][0])[0][-1] + 1
        w2_i = np.where(t_i <= trial['info']['epochs']['stimulus'][1])[0][-1]
        sorted_trials_sti[c]   += trial['r'][:,w1_i:w2_i+1]
        ntrials_by_cond_sti[c] += 1

        w1_i = np.where(t_i <= trial['info']['epochs']['reversal'][0])[0][-1] + 1
        w2_i = np.where(t_i <= trial['info']['epochs']['reversal'][1])[0][-1]
        sorted_trials_rev[c][:,:(w2_i-w1_i+1)] += trial['r'][:,w1_i:w2_i+1]
        ntrials_by_cond_rev[c][:(w2_i-w1_i+1)] += 1

    for c in conds:
        sorted_trials_for[c] *= np.array([safe_divide(x) for x in ntrials_by_cond_for[c]])
        sorted_trials_sti[c] *= np.array([safe_divide(x) for x in ntrials_by_cond_sti[c]])
        sorted_trials_rev[c] *= np.array([safe_divide(x) for x in ntrials_by_cond_rev[c]])

        sorted_trials[c] = np.concatenate(
            (sorted_trials_for[c],sorted_trials_sti[c],sorted_trials_rev[c]), axis=1)

    # Save
    with open(sortedfile, 'wb') as f:
        pickle.dump((t, sorted_trials), f, pickle.HIGHEST_PROTOCOL)
        print(("[ {}.sort_trials_stim_onset ]"
               " Trials sorted and aligned to stimulus onset, saved to {}")
              .format(THIS, sortedfile))

#=========================================================================================

def plot_unit(unit, sortedfile, plot, t0=0, tmin=None, tmax=None, **kwargs):
    if tmin == None:
        tmin = -np.inf
    if tmax == None:
        tmax = np.inf

    # Load sorted trials
    with open(sortedfile) as f:
        t, sorted_trials = pickle.load(f)

    # Time
    w, = np.where((tmin <= t) & (t <= tmax))
    t  = t[w] - t0

    conds = sorted_trials.keys()

    all = []
    for c in sorted(conds, key=lambda c: c):
        intenstiy = c

        prop = {'color': colors[intenstiy],
                'lw':    kwargs.get('lw', 1.5)}

        prop['label'] = '{:.1f}'.format(intenstiy)

        r = sorted_trials[c][unit][w]
        plot.plot(t, r, **prop)
        all.append(r)

    plot.xlim(t[0], t[-1])
    plot.xticks([t[0], 0, t[-1]])
    plot.lim('y', all, lower=0)

    return np.concatenate(all)

#=========================================================================================
# TODO there might be a better way to calculate dprime in this case

def get_choice_selectivity(trialsfile, lower_bon=None, higher_bon=None):
    """
    Compute d' for choice.

    """

    if lower_bon == None:
        lower_bon = 150.2
    if higher_bon == None:
        higher_bon = 150.2

    # Load trials
    trials, ntrials = load_trials(trialsfile)

    N = trials[0]['r'].shape[0]
    Xfor  = np.zeros(N)
    Xfor2 = np.zeros(N)
    Xrev  = np.zeros(N)
    Xrev2 = np.zeros(N)
    n_for = 0
    n_rev = 0

    # method 1 & 2
    # r_for = np.zeros(N)
    # r_rev = np.zeros(N)
    for trial in trials:
        t = trial['t']
        start, end = trial['info']['epochs']['stimulus']
        forward,  = np.where((start - lower_bon < t) & (t <= start))
        reversal, = np.where((end < t) & (t <= end + higher_bon))

        r_for = np.sum(trial['r'][:,forward], axis=1)
        r_rev = np.sum(trial['r'][:,reversal], axis=1)

        Xfor  += r_for
        Xfor2 += r_for**2
        n_for += 1

        Xrev  += r_rev
        Xrev2 += r_rev**2
        n_rev += 1

        # method 1
        # r_for_m = np.mean(trial['r'][:, forward], axis=1)
        # r_for += r_for_m
        #
        # r_rev_m = np.mean(trial['r'][:, reversal], axis=1)
        # r_rev += r_rev_m

        # method 2
        # r_for_m = np.mean(trial['r'][:,forward], axis=1)
        # r_for_s = np.std(trial['r'][:,forward], axis=1)
        # r_for  += r_for_m/r_for_s
        #
        # r_rev_m = np.mean(trial['r'][:,reversal], axis=1)
        # r_rev_s = np.std(trial['r'][:,reversal], axis=1)
        # r_rev  += r_rev_m/r_rev_s

    mean_for  = Xfor/n_for
    var_for   = Xfor2/n_for - mean_for**2
    mean_rev = Xrev/n_rev
    var_rev  = Xrev2/n_rev - mean_rev**2

    # method 1 & 2
    # r_for = r_for / len(trials)
    # r_rev = r_rev / len(trials)

    dprime = (mean_for - mean_rev) / np.sqrt((var_for + var_rev) / 2)
    # dprime = r_for - r_rev

    return dprime

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
    # Sort
    #-------------------------------------------------------------------------------------

    elif action == 'sort_stim_onset':

        sort_trials(get_trialsfile(p), get_sortedfile_stim_onset(p))

    #-------------------------------------------------------------------------------------
    # activate state
    #-------------------------------------------------------------------------------------

    # TODO plot multiple units in the same figure
    # TODO replace units name with real neurons

    elif action == 'activatestate':

        # Model
        m = p['model']

        # Intensity
        try:
            intensity = float(args[0])
        except:
            intensity = 1

        # Plot unit
        try:
            unit = int(args[1])
        except:
            unit = None

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
        if unit is None:
            plot.plot(1e-3 * rnn.t, rnn.z[0], color=colors[0], label='Forward module')
            plot.plot(1e-3 * rnn.t, rnn.z[1], color=colors[1], label='Reversal module')
            plot.lim('y', np.ravel(rnn.z), lower=0)
        else:
            plot.plot(1e-3 * rnn.t, rnn.r[unit], color=colors[1], label='unit '+str(unit))
            plot.lim('y', np.ravel(rnn.r[unit]))

        plot.xlim(1e-3 * rnn.t[0], 1e-3 * rnn.t[-1])

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
            savename = p['name'] + '_' + action + '_init'
        else:
            savename = p['name'] + '_' + action

        if unit is not None:
            savename += '_unit_' + str(unit)

        fig.save(path=p['figspath'], name=savename)
        fig.close()

    # -------------------------------------------------------------------------------------
    # Plot single-unit activity aligned to stimulus onset
    # -------------------------------------------------------------------------------------

    elif action == 'units_stim_onset':
        from glob import glob

        try:
            lower_bon = float(args[0])
        except:
            lower_bon = None

        try:
            higher_bon = float(args[1])
        except:
            higher_bon = None

        # Remove existing files
        unitpath = join(p['figspath'], 'units')
        filenames = glob(join(unitpath, p['name'] + '_stim_onset_unit*'))
        for filename in filenames:
            os.remove(filename)
            print("Removed {}".format(filename))

        # Load sorted trials
        sortedfile = get_sortedfile_stim_onset(p)
        with open(sortedfile) as f:
            t, sorted_trials = pickle.load(f)

        rnn = RNN(p['savefile'], {'dt': p['dt']}, verbose=True)
        trial_func = p['model'].generate_trial
        trial_args = {
            'name': 'test',
            'catch': False,
        }
        info = rnn.run(inputs=(trial_func, trial_args), seed=p['seed'])

        t_stimulus = np.array(info['epochs']['stimulus']);
        stimulus_d = t_stimulus[1]-t_stimulus[0]

        for i in xrange(p['model'].N):
            # Check if the unit does anything
            # active = False
            # for r in sorted_trials.values():
            #     if is_active(r[i]):
            #         active = True
            #         break
            # if not active:
            #     continue

            dashes = [3.5, 1.5]

            fig = Figure()
            plot = fig.add()

            # -----------------------------------------------------------------------------
            # Plot
            # -----------------------------------------------------------------------------

            plot_unit(i, sortedfile, plot, tmin=lower_bon, tmax=higher_bon)

            plot.xlabel('Time (ms)')
            plot.ylabel('Firing rate (a.u.)')

            props = {'prop': {'size': 8}, 'handletextpad': 1.02, 'labelspacing': 0.6}
            plot.legend(bbox_to_anchor=(0.18, 1), **props)

            plot.vline(0, color='0.2', linestyle='--', lw=1, dashes=dashes)
            plot.vline(stimulus_d, color='0.2', linestyle='--', lw=1, dashes=dashes)

            # Epochs
            plot.text(-np.mean((0,stimulus_d)), plot.get_ylim()[1], 'forward',
                      ha='center', va='center', fontsize=7)
            plot.text(np.mean((0,stimulus_d)), plot.get_ylim()[1], 'stimulus',
                      ha='center', va='center', fontsize=7)
            plot.text(3*np.mean((0,stimulus_d)), plot.get_ylim()[1], 'reversal',
                      ha='center', va='center', fontsize=7)

            # -----------------------------------------------------------------------------

            fig.save(path=unitpath,
                     name=p['name'] + '_stim_onset_unit{:03d}'.format(i))
            fig.close()

    #-------------------------------------------------------------------------------------
    # Selectivity
    #-------------------------------------------------------------------------------------

    elif action == 'selectivity':

        try:
            lower = float(args[0])
        except:
            lower = None

        try:
            higher = float(args[1])
        except:
            higher = None

        # Model
        m = p['model']

        trialsfile = get_trialsfile(p)
        dprime     = get_choice_selectivity(trialsfile,lower_bon=lower,higher_bon=higher)

        def get_first(x, p):
            return x[:int(p*len(x))]

        psig  = 0.25
        units = np.arange(len(dprime))
        try:
            idx = np.argsort(abs(dprime[m.EXC]))[::-1]
            exc = get_first(units[m.EXC][idx], psig)

            idx = np.argsort(abs(dprime[m.INH]))[::-1]
            inh = get_first(units[m.INH][idx], psig)

            idx = np.argsort(dprime[exc])[::-1]
            units_exc = list(exc[idx])

            idx = np.argsort(dprime[inh])[::-1]
            units_inh = list(units[inh][idx])

            units  = units_exc + units_inh
            dprime = dprime[units]
        except AttributeError:
            idx = np.argsort(abs(dprime))[::-1]
            all = get_first(units[idx], psig)

            idx    = np.argsort(dprime[all])[::-1]
            units  = list(units[all][idx])
            dprime = dprime[units]

        # Save d'
        filename = get_dprimefile(p)
        np.savetxt(filename, dprime)
        print("[ {}.do ] d\' saved to {}".format(THIS, filename))

        # Save selectivity
        filename = get_selectivityfile(p)
        np.savetxt(filename, units, fmt='%d')
        print("[ {}.do ] Choice selectivity saved to {}".format(THIS, filename))

    #-------------------------------------------------------------------------------------

    else:
        print("[ {}.do ] Unrecognized action.".format(THIS))
