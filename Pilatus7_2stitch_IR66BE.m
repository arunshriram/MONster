tic % start timer; this takes XX seconds as written
%% User inputs
% ECHEM %
dumpname = 'StitchedImgs_all'; % location for dumping images
basename = 'Pilatus\Processed\b_mehta_glass_scan'; % start of filename to load
midname = '_'; % middle of filename to load
endname = '_Qchi.mat'; % end of filename to load
imgname = 'glass_zalignment_'; % for naming output images
firstind = 1; % first scan file index
lastind = 9; % last scan file index
firstphi = 0; % first phi index
numphi = 1; % number of phi scans to process
dphi = 1; % spacing between phis

rq = 250; % #pts/q; range of real data is appx 244.5 to 818.5
rchi = 5; % # pts/chi; range of real data is 5.97 to 21.25


%% Generate phi names

phis = cell(1,numphi);
for i = 1:numphi
    phival = firstphi + (i-1)*dphi;
    if phival <10
        phis{i} = ['000',num2str(phival)];
    elseif phival <100
        phis{i} = ['00',num2str(phival)];
    else
        phis{i} = ['0',num2str(phival)];
    end
end

mkdir(dumpname) % makes folder for dumping files


%% Create final Q0, chi0, Qchi0 arrays

firstfile = [basename,num2str(firstind),midname,phis{1},endname];
load(firstfile) % loads first file, should be one with lowest delta/tth
minq = min(Q(:));
minchi = min(chi(:));
maxchi = max(chi(:));
lastfile = [basename,num2str(lastind),midname,phis{1},endname]; % loads last file, should be one with highest delta/tth
load(lastfile)
maxq = max(Q(:));
lq0int = ceil(rq*(maxq - minq));
lchi0int = ceil(rchi*(maxchi - minchi));

% making q array
dQ0 = 1/rq; % fixed spacing in q
Q0min = round(rq*minq)/rq; % set min value of fixed q array (Q0) from Q1
Q0max = Q0min + (lq0int - 1)*dQ0; % set max value of fixed q array (Q0)
Q0 = Q0min:dQ0:Q0max; % make full fixed q array (Q0)

% making chi array
dchi0 = 1/rchi; % fixed spacing in chi
chi0min = round(rchi*minchi)/rchi; % set min value of fixed chi array (chi0) from chi1
chi0max = chi0min + (lchi0int - 1)*dchi0; % set max value of fixed chi array (chi0)
chi0 = chi0min:dchi0:chi0max; % make full fixed chi array (chi0)

% make all-phi qchi arrays
Qchi0_allphi = zeros(lchi0int,lq0int); % empty array for combined phi image
Qchi0log_allphi = zeros(lchi0int,lq0int); % empty array for combined log phi image

%% Stitch together all the files!
% for phi
for p = 1:numphi
    % make qchi arrays
    Qchi0raw = zeros(lchi0int,lq0int); % make full fixed qchi array for non-normalized data
    Qchi0 = zeros(lchi0int,lq0int); % make full fixed qchi array for normalized data
    count = Qchi0raw; % make counter to keep track of duplicate images
        
for x = firstind:lastind % picks which range of files to stitch
    fullname = [basename,num2str(x),midname,phis{p},endname];
    load(fullname)
%% Fix spacing mismatch

% q spacing
lq = rq*(max(Q) - min(Q)); % new number of pts in q
lqint = ceil(lq); % rounds lq up to integer
Q1 = imresize(Q,[1 lqint]); % resize q

% chi spacing
lchi = rchi*(max(chi) - min(chi)); % new number of pts in chi
lchiint = ceil(lchi); % rounds lchi up to integer
chi1 = imresize(chi,[1 lchiint]); % resize chi

% qchi spacing
Qchi1 = imresize(cake,[lchiint lqint]); % resize Qchi


%% Fix offset

% q offset
Q0i = round(rq*min(Q1))/rq; % find the closest Q0 to the min of Q1
delQ = Q0i - min(Q1);
Q2raw = Q1 + delQ; % shift Q1 to be near Q0
Q2 = round(rq*Q2raw)/rq; % round Q2raw to allowed values from Q0

% chi offset
chi0i = round(rchi*min(chi1))/rchi; % find the closest chi0 to the min of chi1
delchi = chi0i - min(chi1);
chi2raw = chi1 + delchi; % shift chi1 to be near chi0
chi2 = round(rchi*chi2raw)/rchi; % round chi2raw to allowed values from chi0

% qchi offset
Qchi2 = zeros(lchiint,lqint);

% q correction to qchi
for n = 1:lchiint % for loop to make new Qchi2 value at proper offset by linear interpolation value between adjacent Qchi1's
    for m = 1:lqint
        if Qchi1(n,m) <= 0 % set Qchi2 0 if Qchi1 or adj is <=0 to avoid generating fake data
            Qchi2(n,m) = 0;
        elseif m + 1 > lqint % if at the end of the array, enter no value to avoid generating fake data
            Qchi2(n,m) = 0;
        elseif Qchi1(n,m+1) <= 0 % set Qchi2 0 if Qchi1 or adj is <=0 to avoid generating fake data
            Qchi2(n,m) = 0;
        else
            mi = (Qchi1(n,m) - Qchi1(n,m+1))/(Q1(m) - Q1(m+1)); % q slope between adjacent Qchi1
            Qchi2(n,m) = Qchi1(n,m) + mi*(Q2(m) - Q1(m)); % create new Qchi2 on a line between adjacent Qchi1
        end
    end
end

% chi correction to qchi
for n = 1:lchiint % for loop to make new Qchi2 value at proper offset by linear interpolation value between adjacent Qchi1's
    for m = 1:lqint
        if Qchi1(n,m) <= 0 % set Qchi2 0 if Qchi1 or adj is <=0 to avoid generating fake data
            Qchi2(n,m) = 0;
        elseif n + 1 > lchiint % if at the end of the array, enter no value to avoid generating fake data
            Qchi2(n,m) = 0;
        elseif Qchi1(n+1,m) <= 0 % set Qchi2 0 if Qchi1 or adj is <=0 to avoid generating fake data
            Qchi2(n,m) = 0;
        else
            mi = (Qchi1(n,m) - Qchi1(n+1,m))/(chi1(n) - chi1(n+1)); % chi slope between adjacent Qchi1
            Qchi2(n,m) = Qchi1(n,m) + mi*(chi2(n) - chi1(n)); % create new Qchi2 on a line between adjacent Qchi1
        end
    end
end


%% Adding individual images to full array

% position Qchi2 in Qchi0 array
indq = find(Q0 > min(Q2)-1/(4*rq),1); % had issues with find(Q0 == min(Q2),1) so switch to this method
indchi = find(chi0 > min(chi2)-1/(4*rchi),1);

for n = 1:lchiint
    for m = 1:lqint
        if (Qchi2(n,m) > 0) && (m+indq-1 <= lq0int)
            Qchi0raw(n+indchi-1,m+indq-1) = Qchi0raw(n+indchi-1,m+indq-1) + Qchi2(n,m); % add Qchi2 to Qchi0
            count(n+indchi-1,m+indq-1) = count(n+indchi-1,m+indq-1) + 1; % increment counter
        end
    end
end

end


%% Normalize where multiple images added together

for n = 1:lchi0int
    for m = 1:lq0int
        if count(n,m) > 0
            Qchi0(n,m) = Qchi0raw(n,m)/count(n,m);
        end
    end
end


%% Make log plot and combined phi

Qchi0log = zeros(lchi0int,lq0int); % make a log plot
for n = 1:lchi0int
    for m = 1:lq0int
        if Qchi0(n,m) > 0
                Qchi0log(n,m) = log10(Qchi0(n,m));
        end
    end
end

Qchi0_allphi = Qchi0_allphi + Qchi0; % adds image to totalled phi image


%% Save images and datafiles
H = imagesc(Q0,chi0,Qchi0log); 
xlabel('Q (A^-1)')
ylabel('chi (deg)')
colorbar
colormap(jet(256))
%xlim([2 8]) % these values specific to your data; CHECK!!!
%ylim([-80 30]) % these values specific to your data; CHECK!!!
caxis([0 3.5]) % these values specific to your data; CHECK!!!
savepath = [dumpname,'\',imgname,phis{p},'_cropped.tif'];
saveas(H,savepath)

% save qchi and log(qchi) data files
qchi0name = [dumpname,'\',imgname,phis{p},'_Qchi0.mat'];
qchi0logname = [dumpname,'\',imgname,phis{p},'_Qchi0log.mat'];
save(qchi0name,'Qchi0')
save(qchi0logname,'Qchi0log')
end

% save q and chi data files
chi0name = [dumpname,'\',imgname,'chi0.mat'];
q0name = [dumpname,'\',imgname,'Q0.mat'];
save(q0name,'Q0')
save(chi0name,'chi0')


%% Normalize and save qchi with all phis

Qchi0_allphi = Qchi0_allphi/numphi; % normalize the combined-phi image

for n = 1:lchi0int % make a log plot
    for m = 1:lq0int
        if Qchi0_allphi(n,m) > 0
                Qchi0log_allphi(n,m) = log10(Qchi0_allphi(n,m));
        end
    end
end

% Plot qchi
H = imagesc(Q0,chi0,Qchi0log_allphi);
xlabel('Q (A^-1)')
ylabel('chi (deg)')
colorbar
colormap(jet(256))
%xlim([2 8]) % these values specific to your data; CHECK!!!
%ylim([-80 30]) % these values specific to your data; CHECK!!!
caxis([0.5 4]) % these values specific to your data; CHECK!!!
savepath = [dumpname,'\',imgname,'allphi_cropped.tif'];
saveas(H,savepath)

% Save qchi data
qx0phiname = [dumpname,'\',imgname,'qx0_allphi.mat'];
qx0logphiname = [dumpname,'\',imgname,'qx0log_allphi.mat'];
save(qx0phiname,'Qchi0_allphi')
save(qx0logphiname,'Qchi0log_allphi')


toc % end timer
