# PySimuRun
---
## Why Python
*PySimuRun* is created as a general simulation launcher for 
IC functional verification jobs 
(Mostly, running Synopsys VCS, Candence IES etc.).

I've depended on shell scripts combined with Makefile for a while,
and they work together great for simple jobs like invoking compiler 
and simulator, even post processing simulation results. However, 
 maybe I'm bad at either, I couldn't update these scripts easily 
 when I'm trying to support more features. Then I switch to Python
 to replace my original shell scripts.
 
---
## Usage
### Command line and options
```
run test_cases [-s,--old_seed] [-o, --dumpoff] [-g, --gui]
               [[-r, --repeat] repeat_times] 
               [[-e, --ext_cmds] command_string]
```
### Run simulation of given test case
For example, all test cases are stored in `../cases`

These cases are:
```
$ ls ../cases
case1 case2 case_suit
$ ls ../cases/case_suit
case11 case12
```

Run simulation with indicating test case path
```
$ ./run ../cases/case1 # Simulation of 'case1'
```

Run simulation with pattern matching:
```
$ ./run case1
0) ../cases/case1
1) ../cases/case_suit/case11
Please input the number: # Press 1 if you wanna run 'case11'
```

Run simulation of several cases one by one:
```
$ ./run case1 case11  # Simulation of 'case1', then 'case11'
```

Run simulation of all cases in a path
```
$ ./run ../cases/case_suit  # 'case11' and 'case12'
```

---
### Configuration Files
*PySimuRun* loads three configuration files, in YAML format, 
in its working process. They are:
* PySimuRun/.config.yaml
* PySimuRun/Launchers/.workflow.yaml
* PySimuRun/Launchers/.sim_template.yaml

**.config.yaml**

*.config.yaml* is the essential setting *PySimuRun* needs. It
sets three builtin extensions' name and working round information.
It also sets other extension names(Python module names, 
stored in path: *PySimuRun/Launchers/extension/* ) 
which will be imported when `run` script starts.

> The three builtin extensions are: cases, gui and dump
> * cases: The extension adds case path to compiling command line
>* gui: Invoke the GUI of simulator
> * dump: Control the waveform dumping compiling options

Here's a example of *.config.yaml*
```
# Builtin Extensions
cases:
  name: cases
  round:
    compile: compile
    run: run

gui:
  name: gui

dump:
  name: dump

# Other Extensions
extension_list:
  - uvm_verbosity
  - no_cmp
```


**.workflow.yaml** and **.sim_template.yaml**

*.workflow.yaml* lists how many HDL compiling steps, like 
 HDL analysis and elaboration, are needed.
Each step is defined as a 'round' here, composed of:
* A round name
* A list of command plussing its options

*.sim_template.yaml* lists the commands invoked in one simulation.
Each step is defined as a 'round' here too, composed of:
* A round name
* A list of command plussing its options

However, there's a special essential round name `run` in it, 
which defines the main simulation process. All commands before
it is considered as pre-run commands, and as post-run commands after it.

So, both YAML file supports the same format as following:
```
# Round 1
- name: round1
  command:
  - command1
  - option1
  - option2
  
# Round 2
- name: round2
  command:
  - command2
  - option1
  - option2
```

