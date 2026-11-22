import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent
x=json.loads((R/'results/audit.json').read_text());assert x['passed']
policies=['first_then_last','strict_unique','parse_once'];labels=['First / last','Reject duplicates','Parse once'];colors=['#994e20','#606871','#2b6c89']
fig,axes=plt.subplots(1,2,figsize=(12,5),layout='constrained')
for ax,key,title in zip(axes,['attack_forbidden','benign_completed'],['Forbidden file effects','Allowed writes']):
 values=[x['summary'][p][key] for p in policies];ax.barh(labels,values,color=colors,height=.5);ax.invert_yaxis();ax.set_xlim(0,9.5);ax.set_xticks([0,2,4,6,8]);ax.set_xlabel('Fixtures');ax.set_title(title,fontweight='bold');ax.spines[['top','right']].set_visible(False);ax.set_axisbelow(True);ax.grid(axis='x',alpha=.12)
 for i,v in enumerate(values):ax.text(v+.14,i,f'{v}/8',va='center')
fig.savefig(R/'results/json-tool-boundary.png',dpi=180);fig.savefig(R/'results/json-tool-boundary.svg');plt.close(fig)
