### Actions to perform

command line parameters
```python
p.add_argument('model_file', help="model specification")
p.add_argument('action', nargs='?', default='check')
p.add_argument('args', nargs='*')
p.add_argument('-s', '--seed', type=int, default=100)
p.add_argument('--suffix', type=str, default='')
p.add_argument('-p', '--ppn', type=int, default=1)
p.add_argument('-g', '--gpus', nargs='?', type=int, const=1, default=0)
p.add_argument('--dt', type=float, default=0.5)
p.add_argument('--dt_save', type=float, default=0.5)

```
* clean up files and documents
```bash
python do.py models/task_name clean
```

* traning network
```bash
python do.py models/task_name train
python do.py models/task_name train -s 1001 -g0
```

* plot cost history
```bash
python do.py models/task_name costs
```

* plot performance (if performance is defined)
```bash
python do.py models/worm_reversal_con performance    # without target
python do.py models/worm_reversal_con performance 85 # with target
```

* plot network structure
```bash
python do.py models/task_name structure init                # plot initial structure
python do.py models/task_name structure                     # plot structure after training
python do.py models/task_name structure selectivity         # sort by selectivity or other criteriapython do.py models/task_name structure selectivity     # sort by selectivity or other criteria
python do.py models/task_name structure selectivity init    # sort by selectivity or other criteria
```

* plot network output when there is no input (restingstate)
```bash
python do.py models/task_name restingstate init    # plot initial restingstate response
python do.py models/task_name restingstate         # plot restingstate response after training
```

* check log file
```bash
python do.py models/task_name check
```

* submit jobs when using on the cluster
```bash
python do.py models/task_name submit
```

* run analysis examples
```bash
python do.py rdm_model run rdm_script trials 4000 -dt 0.5 --dt_save 20  # run rnn with 4000 trials for each condition
python do.py rdm_model run rdm_script psychometric               # var stimulus
python do.py rdm_model run rdm_script psychometric threshold     # response time version
python do.py rdm_model run rdm_script sort_stim_onset
python do.py rdm_model run rdm_script units_stim_onset
python do.py rdm_model run rdm_script sort_response
python do.py rdm_model run rdm_script units_response
python do.py rdm_model run rdm_script selectivity
```



## All used commands in paper/all.py
```bash
python all.py -s
=> Perceptual decision-making task
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim train -s 1001 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm trials 4000 --dt_save 20
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm sort_stim_onset
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm units_stim_onset
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt train -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm trials 1500 --dt_save 10
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm sort_response
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm units_response
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_rdm.py
=> Perceptual decision-making task (structure)
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale train -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm trials 2000 --dt_save 100
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm selectivity
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense train -s 101 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm trials 2000 --dt_save 100
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm selectivity
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed train -s 1001 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm trials 2000 --dt_save 100
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm selectivity
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_structure.py
=> Context-dependent integration task
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante train -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante trials 200 --dt_save 20
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante sort
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante regress
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante units
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_mante.py
=> Context-dependent integration task (areas)
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas train -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante trials 200 --dt_save 20
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante sort
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante regress
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante units
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_mante_areas.py
=> Connectivity for sequence execution task
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_connectivity.py
=> Multisensory integration task
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory train -s 111 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory run /Users/yuxie/Lab/RNN/pycog/examples/analysis/multisensory trials 500 --dt_save 20
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory run /Users/yuxie/Lab/RNN/pycog/examples/analysis/multisensory sort
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory run /Users/yuxie/Lab/RNN/pycog/examples/analysis/multisensory units
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_multisensory.py
=> Parametric working memory task
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo train -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo run /Users/yuxie/Lab/RNN/pycog/examples/analysis/romo trials 100 --dt_save 20
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo run /Users/yuxie/Lab/RNN/pycog/examples/analysis/romo sort
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo run /Users/yuxie/Lab/RNN/pycog/examples/analysis/romo units
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_romo.py
=> Eye-movement sequence execution task
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee train -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee run /Users/yuxie/Lab/RNN/pycog/examples/analysis/lee trials 100 --dt_save 2
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_lee.py
=> Performance
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_performance.py

```
