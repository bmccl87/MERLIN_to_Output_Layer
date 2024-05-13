import numpy as np
import matplotlib.pyplot as plt


metrics = {'POD','FAR','CSI','HSS'}
models = {
    'ML Model':(71,9,67,80),
    'Persistence':(68,32,51,67),
    'CAPE':(37,85,12,20),
    'E-Field':(28,88,9,15)
}
x=np.arange(4)
width=.2
multiplier=0

fig, ax = plt.subplots(layout='constrained',figsize=(16,10))

for mod, value in models.items():
    print(mod)
    offset = width * multiplier
    rects = ax.bar(x + offset, value, width, label=mod)
    ax.bar_label(recsts, padding=3,fontsize=24)
    multiplier += 1

ax.set_ylabel('Metric Value (%)',fontsize=24)
ax.set_title('Metrics for Lightning Prediction',fontsize=24)
ax.set_xticks(x + width, ['POD','FAR','CSI','HSS'],fontsize=24)
ax.set_yticks([0,20,40,60,80,100],['0','20','40','60','80','100'],fontsize=24)
ax.legend(loc='upper left', ncols=4,fontsize=24)
ax.set_ylim(0, 100)

plt.savefig('/Users/brandonmcclung/Desktop/Mostjabe_adapt.png')