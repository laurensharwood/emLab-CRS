# CRS report with conda environment.yml

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/laurensharwood/CRS/master?labpath=CRS_report.ipynb)


https://mybinder.org/v2/gh/laurensharwood/CRS/master?labpath=CRS_report.ipynb


# 2016-2019 time series of vegetation indices to identify cover crops (CC) and crop residue (CR) on ASA plots (treatment) vs Test plots (control):  
- Vegetation Indices: maximize separation of features of interest. Broadband vs narrowband.  
- Limited to indices using wavelengths/bands covered by Sentinel AND Landsat (can't use Sentinel's red-edge bands).  

## <b>Cover crops:</b> identify CC on ASA plots (with standing CR) from Test plots without CC (with grazed CR)  
- <b>Temporal window:</b> NOV to FEB - after postrera harvest, CC is planted and dies off by February in dry years (can last as long as May?)  
- <b>Spectral window:</b> choose bands-> indices measuring green/live/photosynthetically active vegetation vs brown/dead/non-photosynthetically active vegetation  
1) <b>Enhanced Vegetation Index 2 (EVI2)</b> = 2.5 * ( NIR - RED) / ( NIR + (2.4 * RED + 1.0 )    
2) <b>Green-Chlorophyll Vegetation Index (GCVI)</b> = (NIR – GREEN) / (NIR + GREEN)  
2) <b>Normalized Burn Ratio (NBR)</b> = (SWIR2-NIR1) / (SWIR2+NIR) 

<b> ASA with CC should have higher EVI & GCVI & NBR values than Test plots sans CC from NOV to FEB </b>


## <b>Crop residue:</b> differentiate ASA plots with standing crop residue from Test plots with grazed residue (leaving soil)  
- <b>Temporal window:</b> FEB to MAY - CR is left on both Test and ASA plots. Grazing occurs on Test, so once residue has been grazed on Test & CC dies on ASA around Feb, Test plot should have soil and ASA plot should have standing residue  
- <b>Spectral window:</b> soil and dead/dry veg look similar in visible and NIR parts of the spectrum, but lignin and cellulose in standing residue absorb SWIR2 light  
1) <b>Normalized Difference Tillage Index (NDTI)</b> = (SWIR1-SWIR2) / (SWIR1+SWIR2) First, the most prominent spectral difference between NPV and soil is the cellulose absorption feature in SWIR 2 wavelengths.   
2) <b>Normalized Burn Ratio (NBR)</b> = (SWIR2-NIR1) / (SWIR2+NIR) 

<b> ASA with CR should have higher NDTI & NBR values than Test plots sans CR from FEB to MAY </b>
