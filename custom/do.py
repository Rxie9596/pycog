#! /usr/bin/env python
"""
Sample script for performing common tasks.

If you use this script to run jobs on a cluster don't forget to change the `queue`
argument in `write_jobfile`. Of course, you may have to modify the function
itself depending on your setup.

"""
import argparse
import imp
import os
import shutil
import subprocess
import sys
import time
from   os.path import join

from pycog.utils import get_here, mkdir_p

#=========================================================================================
# Command line
#=========================================================================================

p = argparse.ArgumentParser()
p.add_argument('model_file', help="model specification")
p.add_argument('action', nargs='?', default='check')
p.add_argument('args', nargs='*')
p.add_argument('-s', '--seed', type=int, default=100)
p.add_argument('--suffix', type=str, default='')
p.add_argument('-p', '--ppn', type=int, default=1)
p.add_argument('-g', '--gpus', nargs='?', type=int, const=1, default=0)
p.add_argument('--dt', type=float, default=0.5)
p.add_argument('--dt_save', type=float, default=0.5)
a = p.parse_args()

# Model file
modelfile = os.path.abspath(a.model_file)
# eg. '/Users/yuxie/Lab/RNN/pycog/custom/models/worm_reversal'
if not modelfile.endswith('.py'):
    modelfile += '.py'
    # eg. '/Users/yuxie/Lab/RNN/pycog/custom/models/worm_reversal.py'

action  = a.action
args    = a.args
seed    = a.seed
suffix  = a.suffix
ppn     = a.ppn
gpus    = a.gpus
dt      = a.dt
dt_save = a.dt_save

print("MODELFILE: " + str(modelfile))
print("ACTION:    " + str(action))
print("ARGS:      " + str(args))
print("SEED:      " + str(seed))

#=========================================================================================
# Setup paths
#=========================================================================================

# Location of script
here   = get_here(__file__)      # eg. '/Users/yuxie/Lab/RNN/pycog/custom'
prefix = os.path.basename(here)  # eg. 'custom'

# Name to use
name = os.path.splitext(os.path.basename(modelfile))[0] # eg. 'worm_reversal'

# Scratch
scratchroot = os.environ.get('SCRATCH', join(os.path.expanduser('~'), 'scratch'))
# eg. '/Users/yuxie/scratch'
scratchpath = join(scratchroot, 'work', prefix, name)
# eg. '/Users/yuxie/scratch/work/custom/worm_reversal'

# Theano
theanopath = join(scratchpath, 'theano')
# eg. '/Users/yuxie/scratch/work/custom/worm_reversal/theano'

# Paths
workpath   = join(here, 'work')
# eg. '/Users/yuxie/Lab/RNN/pycog/custom/work'
datapath   = join(workpath, 'data', name)
# eg. '/Users/yuxie/Lab/RNN/pycog/custom/work/data/worm_reversal'
figspath   = join(workpath, 'figs', name)
# eg. '/Users/yuxie/Lab/RNN/pycog/custom/work/figs/worm_reversal'
trialspath = join(scratchpath, 'trials')
# eg. '/Users/yuxie/scratch/work/custom/worm_reversal/trials'

# Create necessary directories
for path in [datapath, figspath, scratchpath, trialspath]:
    mkdir_p(path)

# File to store model in
savefile = join(datapath, name + suffix + '.pkl')
# eg. '/Users/yuxie/Lab/RNN/pycog/custom/work/data/worm_reversal/worm_reversal.pkl'

#=========================================================================================
# Check log file
#=========================================================================================

if action == 'check':
    try:
        action = args[0]
    except IndexError:
        action = 'train'

    jobname = name
    if action != 'train':
        jobname += '_' + action

    logfile = '{}/{}.log'.format(scratchpath, name)
    try:
        with open(logfile, 'r') as f:
            shutil.copyfileobj(f, sys.stdout)
    except IOError:
        print("Couldn't open {}".format(logfile))
        sys.exit()
    print("")

#=========================================================================================
# Clean
#=========================================================================================

elif action == 'clean':
    from glob import glob

    # Data files
    base, ext = os.path.splitext(savefile)
    fnames = glob(base + '*' + ext)
    for fname in fnames:
        os.remove(fname)
        print("Removed {}".format(fname))

    # Theano compile directories
    fnames = glob('{}/{}-*'.format(theanopath, name))
    for fname in fnames:
        shutil.rmtree(fname)
        print("Removed {}".format(fname))

#=========================================================================================
# Submit a job
#=========================================================================================

elif action == 'submit':
    from pycog import pbstools

    if len(args) > 0:
        action = args[0]
        args   = args[1:]
    else:
        action = 'train'

    jobname = name
    if action != 'train':
        jobname += '_' + action

    if len(args) > 0:
        sargs = ' ' + ' '.join(args)
    else:
        sargs = ''

    cmd     = 'python {} {} {}{}'.format(join(here, 'do.py'), modelfile, action, sargs)
    pbspath = join(workpath, 'pbs')
    jobfile = pbstools.write_jobfile(cmd, jobname, pbspath, scratchpath,
                                     ppn=ppn, gpus=gpus, queue='s48')
    subprocess.call(['qsub', jobfile])

#=========================================================================================
# Train
#=========================================================================================

elif action == 'train':
    from pycog import Model

    # Model specification
    model = Model(modelfile=modelfile)

    # Avoid locks on the cluster
    compiledir = join(theanopath, '{}-{}'.format(name, int(time.time())))
    # eg. '/Users/yuxie/scratch/work/custom/worm_reversal/theano/worm_reversal-1557321793'

    # Train
    model.train(savefile, seed=seed, compiledir=compiledir, gpus=gpus)
# eg. savefile='/Users/yuxie/Lab/RNN/pycog/custom/work/data/
#                worm_reversal/worm_reversal.pkl'

#=========================================================================================
# Test resting state
#=========================================================================================

elif action == 'restingstate':
    import numpy as np

    from pycog          import RNN
    from pycog.figtools import Figure

    # Create RNN
    if 'init' in args:
        print("* Initial network.")
        base, ext = os.path.splitext(savefile)
        savefile_init = base + '_init' + ext
        rnn = RNN(savefile_init, {'dt': dt}, verbose=True)
    else:
        rnn = RNN(savefile, {'dt': dt}, verbose=True)
    rnn.run(3e3, seed=seed)

    # Summary
    mean = np.mean(rnn.z)
    std  = np.std(rnn.z)
    print("Mean output: {:.6f}".format(mean))
    print("Std. output: {:.6f}".format(std))

    fig  = Figure()
    plot = fig.add()

    colors = [Figure.colors('blue'), Figure.colors('orange')]
    for i in xrange(rnn.z.shape[0]):
        plot.plot(1e-3*rnn.t, rnn.z[i], color=colors[i%len(colors)])
        mean = np.mean(rnn.z[i])*np.ones_like(rnn.t)
        plot.plot(1e-3*rnn.t, mean, color=colors[i%len(colors)])
    plot.xlim(1e-3*rnn.t[0], 1e-3*rnn.t[-1])
    plot.lim('y', np.ravel(rnn.z), lower=0)

    plot.xlabel('Time (sec)')
    plot.ylabel('Outputs')

    fig.save(path=figspath, name=name+'_'+action)
    fig.close()

#=========================================================================================
# Plot network structure
#=========================================================================================

elif action == 'structure':
    from pycog import RNN

    # Create RNN
    if 'init' in args:
        print("* Initial network.")
        base, ext = os.path.splitext(savefile)
        savefile_init = base + '_init' + ext
        rnn = RNN(savefile_init, verbose=True)
    else:
        rnn = RNN(savefile, verbose=True)

    # Sort order for recurrent units
    sortby = None
    if len(args) > 0:
        if args[0] == 'selectivity':
            filename = join(datapath, name + '_selectivity.txt')
        else:
            filename = os.path.abspath(args[0])

        if os.path.isfile(filename):
            sortby = filename

    # Create figure
    fig = rnn.plot_structure(sortby=sortby)
    fig.save(path=figspath, name=name+'_'+action)
    fig.close()

#=========================================================================================
# Plot costs history
#=========================================================================================

elif action == 'costs':
    from pycog import RNN

    # Create RNN
    rnn = RNN(savefile, verbose=True)

    # Create figure
    fig = rnn.plot_costs()
    fig.save(path=figspath, name=name+'_'+action)
    fig.close()

#=========================================================================================
# Run analysis
#=========================================================================================

elif action == 'run':
    # Get analysis script
    try:
        runfile = args[0]
    except IndexError:
        print("Please specify the analysis script.")
        sys.exit()
    if not runfile.endswith('.py'):
        runfile += '.py'

    # Load analysis module
    try:
        r = imp.load_source('analysis', runfile)
    except IOError:
        print("Couldn't load analysis module from {}".format(runfile))
        sys.exit()

    # Load model
    try:
        m = imp.load_source('model', modelfile)
    except IOError:
        print("Couldn't load model module from {}".format(modelfile))
        sys.exit()

    # Reset args
    args = args[1:]
    if len(args) > 0:
        action = args[0]
        args   = args[1:]
    else:
        action = None
        args   = []

    params = {
        'seed':       seed,
        'model':      m,
        'savefile':   savefile,
        'name':       name,
        'datapath':   datapath,
        'figspath':   figspath,
        'trialspath': trialspath,
        'dt':         dt,
        'dt_save':    dt_save
        }
    r.do(action, args, params)

#=========================================================================================

else:
    print("Unrecognized action \'{}\'.".format(action))
