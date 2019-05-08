var record for rdm_varstim.py

provided vars
```
params={'coh' = provided or not provided
        'catch' = Provided True | False or not provided
        'in_out' = provided or not provided
        'minibatch_index'
        'name' = 'validation'|'gradient'|'test'
        'target_output' = Provided True | False or not provided
        
        }


```
run time vars

```
Nin  = 3
N    = 10
Nout = 2

ei, EXC, INH = tasktools.generate_ei(N)
>>>
ei = array([ 1,  1,  1,  1,  1,  1,  1,  1, -1, -1])
EXC = [0, 1, 2, 3, 4, 5, 6, 7]
INH = [8, 9]

START
2

Cout
array([[1., 1., 1., 1., 1., 1., 1., 1., 0., 0.],
       [1., 1., 1., 1., 1., 1., 1., 1., 0., 0.]])

nconditions
10
pcatch
1/11

params['name'] == 'validation':
b = params['minibatch_index'] % (nconditions + 1)
for b in range(1,11):
    k0, k1 = tasktools.unravel_index(b - 1, (len(cohs), len(in_outs)))
    coh = cohs[k0]
    in_out = in_outs[k1]
    print('coh = {}   in_out = {}'.format(coh,in_out))
>>>
coh = 1   in_out = 1
coh = 2   in_out = 1
coh = 4   in_out = 1
coh = 8   in_out = 1
coh = 16   in_out = 1
coh = 1   in_out = -1
coh = 2   in_out = -1
coh = 4   in_out = -1
coh = 8   in_out = -1
coh = 16   in_out = -1


fixation
100
stimulus
200
decision
300

T
600

epochs = {'fixation': (0, forward),
          'stimulus': (forward, forward + stimulus),
          'decision': (forward + stimulus, T),
          'T': T}

dt
3

e
{'fixation': [0, 1, 2,... 31, 32],
 'stimulus': [33, 34, 35, 36,... 98, 99], 
 'decision': [100, 101, 102,... 198, 199]}

t
array([  3.,   6... 597., 600.])

cohs
1 | 2 | 4 | 8 | 16  
in_out
-1 | 1
choice
1 | 0

START = 2 (colum 3 is start cue)

cohs  = [-16, -8, -4, -2, -1, 1, 2, 4, 8, 16]
scale(cohs)
array([0.244, 0.372, 0.436, 0.468, 0.484, 0.516, 0.532, 0.564, 0.628,
       0.756])

if choice = 1 (in_out = -1)
X
array([[0.   , 0.   , 1],
       [0.   , 0.   , 1],
        ...  fixation
       [0.   , 0.   , 1],
       [0.   , 0.   , 1],
       [0.244, 0.756, 1],
       [0.244, 0.756, 1],
        ...  stimulus
       [0.244, 0.756, 1],
       [0.244, 0.756, 1],
       [0.   , 0.   , 1],
       [0.   , 0.   , 1],
        ...  decision
       [0.   , 0.   , 1],
       [0.   , 0.   , 1]])
       
if choice = 0 (in_out = 1)
X (t,Nin)
array([[0.   , 0.   , 1],
       [0.   , 0.   , 1],
        ...  fixation
       [0.   , 0.   , 1],
       [0.   , 0.   , 1],
       [0.756, 0.244, 1],
       [0.756, 0.244, 1],
        ...  stimulus
       [0.756, 0.244, 1],
       [0.756, 0.244, 1],
       [0.   , 0.   , 1],
       [0.   , 0.   , 1],
        ...  decision
       [0.   , 0.   , 1],
       [0.   , 0.   , 1]])

if catch trial
Y (t,Nout)
array([[0.2, 0.2],
       [0.2, 0.2],
       ... all period
       [0.2, 0.2],
       [0.2, 0.2]])
M (t,Nout)
array([[1., 1.],
       [1., 1.],
       ... all period
       [1., 1.],
       [1., 1.]])
       
if not catch trial
Y (t,Nout)
    if choice = 1 (in_out = -1)
 Y
array([[0.2, 0.2],
       [0.2, 0.2],
        ... fixation + stimulus
       [0.2, 0.2],
       [0.2, 1. ],
        ...  decision
       [0.2, 1. ]])   
       
M (t,Nout)
array([[1., 1.],
        ...fixation
       [1., 1.],
       [0., 0.],
        ...stimulus don't care
       [0., 0.],
       [1., 1.],
        ...decision
       [1., 1.]])


```
return vars
```
generate_trial returns

trial = {'t': t
         'epochs': epochs
         'info': 
          if catch trial {}
          if not catch trial {'coh': coh, 'in_out': in_out, 'choice': choice} 
         'inputs' = X
         'outputs' = Y
         'mask' = M
         }
         
```