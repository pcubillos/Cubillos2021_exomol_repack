import matplotlib.pyplot as plt
import numpy as np

import pyratbay as pb


pyrat = pb.run('spectrum_VO_repack.cfg', init=True)
wl = 1e4/pyrat.spec.wn
# Eval at 2200 K and pressure where VO HWHM is ~1 cm-1:
pyrat.atm.temp[:] = 2200.0
pyrat.run(temp=pyrat.atm.temp)
vo_index = list(pyrat.mol.name).index('VO')
ilayer = 35
ec, _ = pyrat.get_ec(ilayer)
number_density = pyrat.atm.d[ilayer, vo_index]
# Extinction coefficient (cm**-1) to opacity (cm**2 / molecule):
repack_opacity = ec[0] / number_density

# McKemmish data:
mckemmish_wl, mckemmish_opacity = np.loadtxt(
    '../inputs/mckemmish_exomol_vo.dat', unpack=True)

fs = 12
xrans = [
    (0.29, 1.5),
    (0.406, 0.741),
    (1.0, 5.0),
    ]
yrans = [
    (1e-23, 3e-16),
    (3e-20, 2e-16),
    (1e-24, 1e-17),
    ]

plt.figure(1, (6,8))
plt.clf()
plt.subplots_adjust(0.14, 0.06, 0.98, 0.99, hspace=0.1)
for i in range(3):
    ax = plt.subplot(3, 1, 1+i)
    plt.plot(
        mckemmish_wl, mckemmish_opacity, color='mediumblue', lw=1.0,
        label='ExoMol VOMYT')
    plt.plot(
        wl, repack_opacity, color='orange', lw=1.0, alpha=0.85,
        label='repack ExoMol')
    plt.yscale('log')
    plt.xlim(xrans[i])
    plt.ylim(yrans[i])
    plt.xlabel('Wavelength (um)', fontsize=fs)
    plt.ylabel(r'Opacity (cm$^2$ molecule$^{-1}$)', fontsize=fs)
    if i == 0:
        plt.legend(loc='best', fontsize=fs)
    ax.tick_params(
        labelsize=fs-1, direction='in', which='both',
        bottom=True, top=True, left=True, right=True)
plt.savefig('../plots/VO_opacity_spectrum.pdf')
plt.savefig('../plots/VO_opacity_spectrum.png')

