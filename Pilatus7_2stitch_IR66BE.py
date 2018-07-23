
import numpy as np
import scipy
import matcompat

# if available import pylab (from matlibplot)
try:
    import matplotlib.pylab as plt
except ImportError:
    pass

tic = ''
#% start timer; this takes XX seconds as written
#%% User inputs
#% ECHEM %
dumpname = 'StitchedImgs_all'
#% location for dumping images
basename = 'Pilatus\Processed\b_mehta_glass_scan'
#% start of filename to load
midname = '_'
#% middle of filename to load
endname = '_Qchi.mat'
#% end of filename to load
imgname = 'glass_zalignment_'
#% for naming output images
firstind = 1.
#% first scan file index
lastind = 9.
#% last scan file index
firstphi = 0.
#% first phi index
numphi = 1.
#% number of phi scans to process
dphi = 1.
#% spacing between phis
rq = 250.
#% #pts/q; range of real data is appx 244.5 to 818.5
rchi = 5.
#% # pts/chi; range of real data is 5.97 to 21.25
#%% Generate phi names
phis = cell(1, numphi)
for i in np.arange(1, (numphi)+1):
    phival = firstphi+np.dot(i-1, dphi)
    if phival<10.:
        phis.cell[int(i)-1] = np.array(np.hstack(('000', num2str(phival))))
    elif phival<100.:
        phis.cell[int(i)-1] = np.array(np.hstack(('00', num2str(phival))))
        
    else:
        phis.cell[int(i)-1] = np.array(np.hstack(('0', num2str(phival))))
        
    
    
mkdir(dumpname)
#% makes folder for dumping files
#%% Create final Q0, chi0, Qchi0 arrays
firstfile = np.array(np.hstack((basename, num2str(firstind), midname, phis.cell[0], endname)))
np.load(firstfile)
#% loads first file, should be one with lowest delta/tth
minq = matcompat.max(Q(:))
minchi = matcompat.max(chi(:))
maxchi = matcompat.max(chi(:))
lastfile = np.array(np.hstack((basename, num2str(lastind), midname, phis.cell[0], endname)))
#% loads last file, should be one with highest delta/tth
np.load(lastfile)
maxq = matcompat.max(Q(:))
lq0int = np.ceil(np.dot(rq, maxq-minq))
lchi0int = np.ceil(np.dot(rchi, maxchi-minchi))
#% making q array
dQ0 = 1./rq
#% fixed spacing in q
Q0min = matdiv(np.round(np.dot(rq, minq)), rq)
#% set min value of fixed q array (Q0) from Q1
Q0max = Q0min+np.dot(lq0int-1., dQ0)
#% set max value of fixed q array (Q0)
Q0 = np.arange(Q0min, (Q0max)+(dQ0), dQ0)
#% make full fixed q array (Q0)
#% making chi array
dchi0 = 1./rchi
#% fixed spacing in chi
chi0min = matdiv(np.round(np.dot(rchi, minchi)), rchi)
#% set min value of fixed chi array (chi0) from chi1
chi0max = chi0min+np.dot(lchi0int-1., dchi0)
#% set max value of fixed chi array (chi0)
chi0 = np.arange(chi0min, (chi0max)+(dchi0), dchi0)
#% make full fixed chi array (chi0)
#% make all-phi qchi arrays
Qchi0_allphi = np.zeros(lchi0int, lq0int)
#% empty array for combined phi image
Qchi0log_allphi = np.zeros(lchi0int, lq0int)
#% empty array for combined log phi image
#%% Stitch together all the files!
#% for phi
for p in np.arange(1., (numphi)+1):
    #% make qchi arrays
    
#% save q and chi data files
chi0name = np.array(np.hstack((dumpname, '\\', imgname, 'chi0.mat')))
q0name = np.array(np.hstack((dumpname, '\\', imgname, 'Q0.mat')))
plt.save(q0name, 'Q0')
plt.save(chi0name, 'chi0')
#%% Normalize and save qchi with all phis
Qchi0_allphi = matdiv(Qchi0_allphi, numphi)
#% normalize the combined-phi image
for n in np.arange(1., (lchi0int)+1):
    #% make a log plot
    
#% Plot qchi
H = imagesc(Q0, chi0, Qchi0log_allphi)
plt.xlabel('Q (A^-1)')
plt.ylabel('chi (deg)')
plt.colorbar
colormap(plt.jet(256.))
#%xlim([2 8]) % these values specific to your data; CHECK!!!
#%ylim([-80 30]) % these values specific to your data; CHECK!!!
caxis(np.array(np.hstack((0.5, 4.))))
#% these values specific to your data; CHECK!!!
savepath = np.array(np.hstack((dumpname, '\\', imgname, 'allphi_cropped.tif')))
saveas(H, savepath)
#% Save qchi data
qx0phiname = np.array(np.hstack((dumpname, '\\', imgname, 'qx0_allphi.mat')))
qx0logphiname = np.array(np.hstack((dumpname, '\\', imgname, 'qx0log_allphi.mat')))
plt.save(qx0phiname, 'Qchi0_allphi')
plt.save(qx0logphiname, 'Qchi0log_allphi')
toc
#% end timer
