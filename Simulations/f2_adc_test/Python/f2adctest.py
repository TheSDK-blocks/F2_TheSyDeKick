#You may write any matlab code here to control your sim
#Execute this file n console with  
#exec(open("./f2adctest.py").read())
import os
import sys
rootpath='/tools/projects/kosta/TheSDK/Simulations/f2_adc_test'
statusfile= rootpath + '/Python/' + os.path.splitext(os.path.basename(__file__))[0]+'.status' 
picpath=rootpath + '/Pics';
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/f2_adc/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/f2_channel/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/f2_dsp/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/f2_rx/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/f2_serdes/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/f2_signal_gen/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/f2_system/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/f2_system_test/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/inv_sim/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/inverter/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/modem/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/refptr/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/rtl/py')
sys.path.append ('/tools/projects/kosta/TheSDK/Entities/thesdk/py')
from thesdk import *
thesdk.logfile="/tools/projects/kosta/TheSDK/Simulations/f2_adc_test/Python/f2adctest.status"
thesdk.initlog()

from f2_adc import f2_adc
import numpy as np
import matplotlib.pyplot as plt

fontsize = 15
linewidth = 1.5

def plot_generic(x, y_list, title_str, legend_list, xlabel_str, ylabel_str, xscale, yscale, plot_style_str='o-', xlim=[], ylim=[]):
    if (xscale, yscale) == ('linear', 'linear'):
        plot_type_str = 'plot'
    elif (xscale, yscale) == ('log', 'linear'):
        plot_type_str = 'semilogx'
    elif (xscale, yscale) == ('linear', 'log'):
        plot_type_str = 'semilogy'
    elif (xscale, yscale) == ('log', 'log'):
        plot_type_str = 'loglog'
    else:
        raise Exception('xscale = %s, yscale = %s, both should be linear or log!!' % (xscale, yscale))
    fig, ax = plt.subplots() # default is 1,1,1
    if (isinstance(x[0], list)) and (len(x) == len(y_list)): # several plots with different x values
        for x, y in zip(x, y_list):
            exec('ax.' + plot_type_str + '(x, y, plot_style_str, linewidth=linewidth)')
    else:
        if (isinstance(y_list[0], list)): # several plots with the same x values
            for y in y_list:
                exec('ax.' + plot_type_str + '(x, y, plot_style_str, linewidth=linewidth)')
        else: # single plot only
            exec('ax.' + plot_type_str + '(x, y_list, plot_style_str, linewidth=linewidth)')
    if xlim != []:
        plt.xlim(xlim)
    if ylim != []:
        plt.ylim(ylim)
    ax.set_xlabel(xlabel_str, fontsize=fontsize)
    plt.ylabel(ylabel_str, fontsize=fontsize)
    if title_str == []:
        loc_y = 1.05
    else:
        plt.title(title_str, fontsize=fontsize)
        loc_y = 1
    if legend_list != []:
        plt.legend(legend_list, loc=(0, loc_y))
    plt.grid(True, which='both')
    ax.tick_params(axis='both', which='major', labelsize=fontsize)
    plt.show()

t = f2_adc()
in_sig = np.linspace(-t.full_scale, t.full_scale, 1001)
t.iptr_A.Value = [in_sig]
t.picpath=picpath;
t.run()
out_sig = t._Z.Value[0]

plot_generic(list(in_sig), [list(in_sig), list(out_sig)],
             title_str=('ADC model with FullScale=%.1f and %d bits' % (t.full_scale, t.Nbits)), legend_list=['in', 'out'],
             xlabel_str='input', ylabel_str='output', xscale='linear', yscale='linear',
             plot_style_str='-', xlim=[min(in_sig), max(in_sig)], ylim=[min(in_sig), max(in_sig)])

