import numpy as np
from scipy.ndimage.filters import gaussian_filter1d as gaussf
import matplotlib.pyplot as plt

import pyratbay as pb
import pyratbay.constants as pc


repack = pb.run('spectrum_H2O_repack.cfg', run_step='init', no_logfile=True)
exomol = pb.run('spectrum_H2O_exomol.cfg', run_step='init', no_logfile=True)
wl = 1.0 / (repack.spec.wn*pc.um)
nwave = repack.spec.nwave

temps = [300, 1200, 2500]
ntemp = len(temps)
ipress = 28  # 0.1 bar

repack_ec = np.zeros((ntemp, nwave))
exomol_ec = np.zeros((ntemp, nwave))
for i in range(ntemp):
    repack.atm.temp[:] = temps[i]
    exomol.atm.temp[:] = temps[i]
    pb._ra.update_atm(repack)
    pb._ra.update_atm(exomol)
    rec, ec_labels = repack.get_ec(ipress)
    eec, ec_labels = exomol.get_ec(ipress)
    repack_ec[i] = rec[0]
    exomol_ec[i] = eec[0]


fs = 11
lw = 0.75
xlim = (1.25, 1.4)
xticks = np.arange(1.24, 1.41, 0.02)
xticks = np.arange(1.25, 1.41, 0.03)

plt.figure(0, (8, 5.8))
plt.clf()
plt.subplots_adjust(0.08, 0.07, 0.98, 0.97, hspace=0.2, wspace=0.22)
for i in range(ntemp):
    # Extinction coefficient:
    ax1 = plt.subplot(ntemp, 2, 1+2*i)
    plt.semilogy(
        wl, exomol_ec[i], lw=lw, c='mediumblue', label='full ExoMol')
    plt.semilogy(
        wl, repack_ec[i], lw=lw, c='orange', label='repack ExoMol', alpha=0.8)
    ax1.text(
        0.02, 0.9, rf'$T = {temps[i]}$ K', fontsize=fs, transform=ax1.transAxes)
    ax1.set_xticks(xticks)
    ax1.set_xlim(xlim)
    ax1.tick_params(labelsize=fs-1, direction='in', which='both', right=True)
    # Fractional difference between log-values:
    diff = 100*(1-np.log(exomol_ec[i])/np.log(repack_ec[i]))
    ax2 = plt.subplot(ntemp, 2, 2+2*i)
    plt.plot(wl, diff, c='red', lw=lw)
    plt.plot(wl[1:-1], gaussf(diff[1:-1],100), c='black')
    ax2.set_xticks(xticks)
    ax2.set_xlim(xlim)
    ax2.set_ylim(-0.2, 1.0)
    ax2.tick_params(labelsize=fs-1, direction='in', which='both', right=True)
    if i == 0:
        ax1.legend(loc='lower right', fontsize=fs-1)
    if i == 1:
        ax1.set_ylabel(r'H$_2$O extinction coefficient (cm$^{-1}$)',fontsize=fs)
        ax2.set_ylabel(r'Dex residuals (%)', fontsize=fs)
ax1.set_xlabel('Wavelength (um)', fontsize=fs)
ax2.set_xlabel('Wavelength (um)', fontsize=fs)
plt.savefig('../plots/H2O_low-resolution_extinction_coefficient.pdf')


# Transmission spectrum at a temperature of 2500K:
temp = np.copy(repack.atm.temp)

i = 2
temp[:] = temps[i]
exomol.run(temp=temp)
repack.run(temp=temp)

plt.figure(10, (5.0, 5.5))
plt.clf()
plt.subplots_adjust(0.13, 0.08, 0.97, 0.97,  wspace=0.1)
# Transmission spectrum:
ax = plt.subplot(211)
plt.plot(
    wl, exomol.spec.spectrum/pc.percent, lw=lw, c='mediumblue',
    label='full ExoMol')
plt.plot(
    wl, repack.spec.spectrum/pc.percent, lw=lw, c='orange',
    label='repack ExoMol', alpha=0.85)
ax.text(
    0.03, 0.63, f'$T = {temps[i]}$ K', fontsize=fs, transform=ax.transAxes)
ax.set_xticks(xticks)
ax.set_xlim(xlim)
ax.tick_params(labelsize=fs-1, direction='in', which='both', right=True)
ax.set_ylabel(r'$(R_{\rm p}/R_{\rm s})^{2}$ (%)', fontsize=fs)
ax.set_xlabel('Wavelength (um)', fontsize=fs)
ax.legend(loc='upper left', fontsize=fs)
# Residuals:
ax = plt.subplot(212)
diff = (exomol.spec.spectrum - repack.spec.spectrum) / pc.ppm
plt.plot(wl, diff, c='red', lw=lw)
plt.plot(wl[1:-1], gaussf(diff[1:-1], 100), c='black')
ax.set_xticks(xticks)
ax.set_xlim(xlim)
ax.tick_params(labelsize=fs-1, direction='in', which='both', right=True)
ax.set_ylim(-1.0, 10)
ax.set_xlabel('Wavelength (um)', fontsize=fs)
ax.set_ylabel(
    r'$(R_{\rm p}/R_{\rm s})^{2}_{\rm exomol} -'
    r' (R_{\rm p}/R_{\rm s})^{2}_{\rm repack}$ (ppm)', fontsize=fs)
plt.savefig(
    f'../plots/H2O_low-resolution_transmission_spectrum_{temps[i]}K.pdf')

