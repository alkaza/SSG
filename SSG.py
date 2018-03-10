
# coding: utf-8

# # Super Simple Gantt (SSG)
# 
# This python codelet plots Gantt chart through super simple interface.
# 
# - - -
# 
# **usage** : *python SSG.py \[infile.txt\]*
# 
# SSG produce ***outfile-[infile].png*** as output. For *infile.txt* format, see the '2. Load Gantt chart data' at below

# ## 1. Import libraries
# - - -
# Let's import **sys** and **matplotlib** as below. **sys** is used for accepting command line arguments and **matplotlib** is used for plotting Gantt chart.

# In[ ]:

import sys
import matplotlib.pyplot


# ## 2. Load Gantt chart data
# - - -
# SSG takes very simple text data as input. SSG expects that records in the same task-name group are sorted following time-ascending order.
# 
# The format of text file should follow below form:
# 
# > \[task-name\] \[start-time\] \[end_time\]
# 
# > \[task-name\] \[start-time\] \[end_time\]
# 
# > ...
# 
# **Example**. *infile.txt*
# 
# > T1 100000 120000
# 
# > T2 120000 140000
# 
# > T1 130000 150000
# 
# > T2 145000 150000

# In[ ]:

infile = open(sys.argv[1], 'r')

data = dict()
for line in infile:
    task_name, start_time, end_time = line.split()
    if str(task_name) not in data:
        data[str(task_name)] = [[int(start_time), int(end_time) - int(start_time)]]
    else:
        data[str(task_name)] += [[int(start_time), int(end_time) - int(start_time)]]


# ## 3. Prepare figure
# - - -
# For analysis, SSG will plot **1 + [the-number-of-tasks] charts** in output figure.
# One for Gantt chart, the others for execution time (duration) plots.
# Below cell prepare figure which has two chart area.

# In[ ]:

fig = matplotlib.pyplot.figure()

Gantt_axis = fig.add_subplot(len(data) + 1, 1, 1)

execution_time_axis = []
for pos in range(len(data)):
    execution_time_axis += [fig.add_subplot(len(data) + 1, 1, pos + 2)]


# ## 4. Draw Gantt chart
# - - -
# Draw Gantt chart using input data.

# In[ ]:

yticks = []
ylabels = []
yoffset = 10

for task_name in data:
    Gantt_axis.broken_barh(data[task_name], [yoffset, 9], facecolors='blue')
    Gantt_axis.ticklabel_format(useOffset=False, style='plain')
    yticks += [yoffset + 5]
    ylabels += [task_name]
    yoffset += 10

Gantt_axis.set_title('Gantt chart')
Gantt_axis.set_yticks(yticks)
Gantt_axis.set_yticklabels(ylabels)
Gantt_axis.grid(True)


# ## 5. Draw execution time (=duration) plot
# - - -
# Draw execution time (=duration) plot

# In[ ]:

plotidx = 0

for task_name in data:
    execution_cnt = [k + 1 for k in range(len(data[task_name]))]
    execution_time = [execution[1] for execution in data[task_name]]
    
    execution_time_axis[plotidx].scatter(execution_cnt, execution_time)
    execution_time_axis[plotidx].ticklabel_format(useOffset=False, style='plain')
        
    execution_time_axis[plotidx].set_title('Execution time - ' + task_name)
    execution_time_axis[plotidx].set_xticks(execution_cnt)
    execution_time_axis[plotidx].grid(True)
    
    plotidx = plotidx + 1


# ## 6. Plot all
# - - -
# Plot a chart for Gantt, [the-number-of-tasks] charts for execution times (=durations).

# In[ ]:

fig.tight_layout()
fig.savefig('./outfile-' + sys.argv[1] + '.png')

