
%%%General image analysis code, 1D fitting%%%

%%note that imaages/camera are rotated by 90 degrees

%file to analyze%
parent_dir = 'G:\Shared drives\CaOH exp\Data Folder\Scans\';
date = '20191123';
%% 478.600019 phase scan
scannums = {'103140' '105211' '110938' '120721' '122435' '134501'}; 
%overall scan; scannum_1 is first parameter, etc
parameters = [8 1 2 3 4 5 6 7 9 10];
parametername = 'Configuration';
hintlow = 9; %define window for horizontal integration
hinthigh = 19;
vcut = 1;
vrangelow = 5; %plotting window for vertical profile (1st point is 1, not 0)
vrangehigh = 42;

%%
fitsfile = 1; %file in .fits format?

%analysis settings%
% hintlow = 9; %define window for horizontal  integration
% hinthigh = 29;
% vcut = 1;
% vrangelow = 17; %plotting window for vertical profile (1st point is 1, not 0)
% vrangehigh = 45;
converttodist = 1; %convert pixels to mm?
convfact = 0.0705; %mm/pixel
binning = 8; %camera binning

%averaging settings
sma = 0; %0 -> no averaging, 1 -> simple moving average
smanum = 2; %# of points to include on either side in average
fitsma = 0; %fit to smoothed data (1)? Or raw unsmoothed (0)

avgparameters = 1; %average together all points for a given parameter
avgparameterfits = 1; %do this by averaging images together and fitting
showfits2 = 1; %show these fits on plot?
avgparameteravgs = 0; %do this by averaging results of individual fits

%fitting settings
fitting = 1; %0 ->  no fit, 1 -> Gaussian fit
showfits = 0; %0 -> fit, but don't plot the fits
titlefits = 0; %0 -> none, 1 -> centers, 2 -> widths

%parameters to plot
sigmas = 1;
centers = 1;
amps = 1;
area = 1; %integrated area

%display settings%
showimages = 1;

%%%import image file%%%

close all

scans = cell(1,length(parameters)*length(scannums));
for j = 1:length(scannums)
for i = 1:length(parameters)
    scans{length(parameters)*(j-1)+i} = strcat(scannums{j},'_',num2str(i));
end
end
parameters2 = repmat(parameters,1,length(scannums));

nscans = length(scans);
imdata = cell(1,nscans);
imheight = zeros(nscans,1);
imwidth = zeros(nscans,1);
for i = 1:nscans
    dir = strcat(parent_dir,date,'\',scans{i},'\');
    if fitsfile == 0
        imfile = strcat(dir,'BKgsubtracted.txt');
    elseif fitsfile == 1
        imfile = strcat(dir,'BGsubtracted.fits');
    end
    if fitsfile == 0
        imdata{i} = importdata(imfile);
    elseif fitsfile == 1
        imdata{i} = fitsread(imfile);
    end
    imdata{i} = rot90(imdata{i}); %rotate 90 degrees ccw
    [imheight(i), imwidth(i)] = size(imdata{i});
    if showimages == 1
        figure(i+2)
        image(imdata{i})
        hold on
        plot([hintlow, hintlow], [1, imheight(i)],'r-','LineWidth',1.5)
        plot([hinthigh, hinthigh], [1, imheight(i)],'r-','LineWidth',1.5)
        if vcut == 1
        plot([1, imwidth(i)], [vrangelow, vrangelow],'r-','LineWidth',1.5)
        plot([1, imwidth(i)], [vrangehigh, vrangehigh],'r-','LineWidth',1.5)
        end
        hold off
        axis image
    end
end

%%%horizontal integration for vertical cut%%%

figmain = figure(1);

datestr = [date(5:6) '/' date(7:8) '/' date(3:4)];

hint = cell(1,nscans);
axis1 = cell(1,nscans);
hint2 = cell(1,nscans-2*smanum);
axis2 = cell(1,nscans-2*smanum);
intall = zeros(1,nscans);
if fitting ~= 0
    coeffs = cell(1,nscans);
    stds = cell(1,nscans);
    reserr = zeros(1,nscans);
    widerr = zeros(1,nscans);
    amperr = zeros(1,nscans);
    if titlefits ~= 0
        titlecell = cell(1,nscans+1);
        titlecell{1} = ['Integrated vertical profile ' datestr];
    else
        titlecell = ['Integrated vertical profile ' datestr];
    end
    gaussianfit = cell(1,nscans);
else
    titlecell = 'Integrated vertical traces';
end
for n = 1:nscans
    if vcut == 0
    hint{n} = zeros(imheight(n),1);
    axis1{n} = zeros(imheight(n),1);
    for i = 1:imheight(n)
        axis1{n}(i) = i;
        hint{n}(i) = mean(imdata{n}(i,hintlow:hinthigh));
    end
    else
      hint{n} = zeros(vrangehigh-vrangelow+1,1);
      axis1{n} = zeros(vrangehigh-vrangelow+1,1);
      for i = 1:vrangehigh-vrangelow+1
        axis1{n}(i) = vrangelow+i-1;
        hint{n}(i) = mean(imdata{n}(vrangelow+i-1,hintlow:hinthigh));
      end
    end
    
    if sma == 1
        hint2{n} = zeros(length(hint{n})-2*smanum,1);
        axis2{n} = zeros(length(axis1{n})-2*smanum,1);
        for i = 1:length(hint{n})-2*smanum
            axis2{n}(i) = axis1{n}(i+smanum);
            hint2{n}(i) = mean(hint{n}(i:i+2*smanum));
        end
    else
       hint2{n} = hint{n};
       axis2{n} = axis1{n}; 
    end
    
    plot(axis2{n},hint2{n})
    hold on
    
    if fitting == 1
        maxloc = find(hint{n} == max(hint{n}));
        maxval = hint{n}(maxloc);
        maxpos = axis1{n}(maxloc);
        
        foptions = fitoptions('Method','NonlinearLeastSquares','StartPoint',...
            [maxval maxpos 7 0]);
        gaussianmodel = fittype('a*exp(-(x-b)^2/(2*c^2)) + d','independent',...
            {'x'},'dependent',{'y'},'coefficients',{'a','b','c','d'},...
            'options',foptions);
        
        if fitsma == 0 || sma == 0
            gaussianfit{n} = fit(axis1{n},hint{n},gaussianmodel);
        elseif fitsma == 1
            gaussianfit{n} = fit(axis2{n},hint2{n},gaussianmodel);
        end
        coeffs{n} = coeffvalues(gaussianfit{n});
        stds{n} = confint(gaussianfit{n},0.68);
        reserr(n) = 0.5*(stds{n}(2,2)-stds{n}(1,2));
        widerr(n) = 0.5*(stds{n}(2,3)-stds{n}(1,3));
        amperr(n) = 0.5*(stds{n}(2,1)-stds{n}(1,1));
        
        if titlefits == 1
        titlecell{n+1} = ['center' num2str(n) ' ' num2str(coeffs{n}(2))...
            ' pixels, std ' num2str(reserr(n))];
        elseif titlefits == 2
        titlecell{n+1} = ['width' num2str(n) ' ' num2str(coeffs{n}(3))...
            ' pixels, std ' num2str(widerr(n))];
        end
            
    end
    
    if area == 1
        intall(n) = mean(hint{n});
    end
    
%     plot(axis{n},hint{n})
%     hold on 
    
end


if showfits == 1
for n = 1:nscans
    plot(gaussianfit{n},'k-.');
end
end

title(titlecell)
legend(scans)
xlabel('Position (pixels)');
ylabel('Integrated signal (arb.)');
hold off

%%%averaging together all traces for each parameter value%%%
if avgparameters == 1
    
    figure(2)
    
    hintarr = cell2mat(hint);
    hint2arr = cell2mat(hint2);

    parametervals = unique(parameters2);
    parameterinds = cell(1,length(parametervals));
    if avgparameterfits == 1
        gaussianfitavg = cell(1,length(parametervals));
        coeffsavg = cell(1,length(parametervals));
        stdsavg= cell(1,length(parametervals));
        reserravg2 = zeros(1,length(parametervals));
        widerravg2 = zeros(1,length(parametervals));
        if area == 1
            intallavg2 = zeros(1,length(parametervals));
        end
    end
    for n = 1:length(parametervals)
        parameterinds{n} = find(parameters2 == parametervals(n));
        hintavg = mean(hintarr(:,parameterinds{n}),2);
        hint2avg = mean(hint2arr(:,parameterinds{n}),2);
        plot(axis2{1},hint2avg,'LineWidth',2);
        hold on
        if avgparameterfits == 1
            maxloc = find(hintavg == max(hintavg));
            maxval = hintavg(maxloc);
            maxpos = axis1{1}(maxloc);
            
            foptions = fitoptions('Method','NonlinearLeastSquares','StartPoint',...
                [maxval maxpos 10 0]);
            gaussianmodel = fittype('a*exp(-(x-b)^2/(2*c^2)) + d','independent',...
                {'x'},'dependent',{'y'},'coefficients',{'a','b','c','d'},...
                'options',foptions);
            
            gaussianfitavg{n} = fit(axis1{1},hintavg,gaussianmodel);
            
            coeffsavg{n} = coeffvalues(gaussianfitavg{n});
            stdsavg{n} = confint(gaussianfitavg{n},0.68);
            reserravg2(n) = 0.5*(stdsavg{n}(2,2)-stdsavg{n}(1,2));
            widerravg2(n) = 0.5*(stdsavg{n}(2,3)-stdsavg{n}(1,3));
            
            if area == 1
                intallavg2(n) = mean(hintavg);
            end
        end
        
    end
    
    if showfits2 == 1
    for n = 1:length(parametervals)
        plot(gaussianfitavg{n},'k-.');
    end
    end
    
    title('Averaged traces')
    legend(string(parametervals))
    xlabel('Position (pixels)');
    ylabel('Integrated signal (arb.)');
    hold off
            
end

centerlist = zeros(1,nscans);
sigmalist = zeros(1,nscans);
amplist = zeros(1,nscans);
for n = 1:nscans
    centerlist(n) = coeffs{n}(2);
    sigmalist(n) = abs(coeffs{n}(3));
    amplist(n) = coeffs{n}(1);
end

if converttodist == 1
    centerlist = centerlist*convfact*binning;
    sigmalist = sigmalist*convfact*binning;
    widerr = widerr*convfact*binning;
    reserr = reserr*convfact*binning;
end

if area == 1
    figure()
    plot(parameters2,intall,'o');
    xlabel(parametername);
    ylabel('Integrated area (arb. units)');
end
if amps == 1
figure()
plot(parameters2,amplist,'o')
xlabel(parametername);
ylabel('Amplitude (arb)');
end
if centers == 1
figure()
errorbar(parameters2,centerlist,reserr,'o')
xlabel(parametername);
if converttodist == 0
    ylabel('Center (pixels)');
elseif converttodist == 1
    ylabel('Center (mm)');
end
end
if sigmas == 1
figure()
errorbar(parameters2,sigmalist,widerr,'o')
xlabel(parametername);
if converttodist == 0
    ylabel('Sigma (pixels)');
elseif converttodist == 1
    ylabel('Sigma (mm)');
end
end

if avgparameters == 1
    if avgparameteravgs == 1
        centerlistavg1 = zeros(1,length(parametervals));
        sigmalistavg1 = zeros(1,length(parametervals));
        amplistavg1 = zeros(1,length(parametervals));
        widerravg1 = zeros(1,length(parametervals));
        reserravg1 = zeros(1,length(parametervals));
        intallavg1 = zeros(1,length(parametervals));
        intallerravg1 = zeros(1,length(parametervals));
        for n = 1:length(parametervals)
            centerlistavg1(n) = mean(centerlist(parameterinds{n}));
            sigmalistavg1(n) = mean(sigmalist(parameterinds{n}));
            amplistavg1(n) = mean(amplist(parameterinds{n}));
            widerravg1(n) = sqrt(sum(widerr(parameterinds{n}).^2))/length(parameterinds{n});
            reserravg1(n) = sqrt(sum(reserr(parameterinds{n}).^2))/length(parameterinds{n});
            intallavg1(n) = mean(intall(parameterinds{n}));
            intallerravg1(n) = std(intall(parameterinds{n}))/sqrt(length(parameterinds{n}));
        end
    end
    if avgparameterfits == 1
        centerlistavg2 = zeros(1,length(parametervals));
        sigmalistavg2 = zeros(1,length(parametervals));
        amplistavg2 = zeros(1,length(parametervals));
        for n = 1:length(parametervals)
            centerlistavg2(n) = coeffsavg{n}(2);
            sigmalistavg2(n) = abs(coeffsavg{n}(3));
            amplistavg2(n) = coeffsavg{n}(1);
        end
        if converttodist == 1
            centerlistavg2 = centerlistavg2*convfact*binning;
            sigmalistavg2 = sigmalistavg2*convfact*binning;
            widerravg2 = widerravg2*convfact*binning;
            reserravg2 = reserravg2*convfact*binning;
        end
        
    end
if area == 1
    figure()
    if avgparameterfits == 1
        plot(parametervals,intallavg2,'ro');
        xlabel(parametername);
        ylabel('Integrated area (arb. units)');
        hold on
    end
    if avgparameteravgs == 1
        errorbar(parametervals,intallavg1,intallerravg1,'bo');
        xlabel(parametername);
        ylabel('Integrated area (arb. units)');
        hold on
    end
    if avgparameterfits == 1 && avgparameteravgs == 1
        legend('Integrated averaged trace', 'Average of individual traces');
    end
    hold off
    title('Averaged areas');
end
if amps == 1
    figure()
    if avgparameterfits == 1
        plot(parametervals,amplistavg2,'ro')
        xlabel(parametername);
        ylabel('Amplitude (arb)');
        hold on
    end
    if avgparameteravgs == 1
        plot(parametervals,amplistavg1,'bo')
        xlabel(parametername);
        ylabel('Amplitude (arb)');
    end
    if avgparameterfits == 1 && avgparameteravgs == 1
        legend('Fit to averaged trace', 'Average of individual fits');
    end
    hold off
    title('Averaged amplitudes');
end
if centers == 1
    figure()
    if avgparameterfits == 1
        errorbar(parametervals,centerlistavg2,reserravg2,'ro')
        xlabel(parametername);
        if converttodist == 0
            ylabel('Center (pixels)');
        elseif converttodist == 1
            ylabel('Center (mm)');
        end
        hold on
    end
    if avgparameteravgs == 1
        errorbar(parametervals,centerlistavg1,reserravg1,'bo')
        xlabel(parametername);
        if converttodist == 0
            ylabel('Center (pixels)');
        elseif converttodist == 1
            ylabel('Center (mm)');
        end
    end
    if avgparameterfits == 1 && avgparameteravgs == 1
        legend('Fit to averaged trace', 'Average of individual fits');
    end
    hold off
    title('Averaged centers');
end
if sigmas == 1
    figure()
    if avgparameterfits == 1
        errorbar(parametervals,sigmalistavg2,widerravg2,'ro')
        xlabel(parametername);
        if converttodist == 0
            ylabel('Sigma (pixels)');
        elseif converttodist == 1
            ylabel('Sigma (mm)');
        end
        hold on
    end
    if avgparameteravgs == 1
        errorbar(parametervals,sigmalistavg1,widerravg1,'bo')
        xlabel(parametername);
        if converttodist == 0
            ylabel('Sigma (pixels)');
        elseif converttodist == 1
            ylabel('Sigma (mm)');
        end
    end
    if avgparameterfits == 1 && avgparameteravgs == 1
        legend('Fit to averaged trace', 'Average of individual fits');
    end
    hold off
    title('Averaged widths');
end
   
end

%%%useful output values

npars = length(parameters);
remfrac = mean(intallavg1(1:npars-1))/intallavg1(npars);
remfracerr = remfrac*sqrt((std(intallavg1(1:npars-1))/mean(intallavg1(1:npars-1)))^2 +...
    (intallerravg1(npars)/intallavg1(npars))^2);
remfracerr2 = remfrac*sqrt((1/4*sqrt(sum(intallerravg1(1:npars-1).^2))/mean(intallavg1(1:npars-1)))^2 +...
    (intallerravg1(npars)/intallavg1(npars))^2);
disp(['Remaining fraction: ' num2str(remfrac) ' Err: ' num2str(remfracerr)...
    ' Err2: ' num2str(remfracerr2)]);


