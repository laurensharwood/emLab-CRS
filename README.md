# CRS report with conda environment.yml

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/laurensharwood/CRS/master?labpath=CRS_report.ipynb)

https://mybinder.org/v2/gh/laurensharwood/CRS/master?labpath=CRS_report.ipynb

# 2016-2019 time series of vegetation indices to identify cover crops (CC) and crop residue (CR) on ASA plots (treatment) vs Test plots (control):  
- Vegetation Indices: maximize separation of features of interest.  
- Limited to indices using wavelengths/bands covered by Sentinel AND Landsat (can't use Sentinel's red-edge bands).  

## <b>Cover crops:</b> identify CC on ASA plots (with standing CR) from Test plots without CC (with grazed CR)  
- <b>Temporal window:</b> NOV to FEB - After postrera harvest around November, cover crops are planted on ASA plots and die off by February in dry years, but can last as long as May.  
- <b>Spectral window:</b> The dominant factors controlling live cover crop vegetation reflectance are chlorophyll, absorption of red and blue light, reflection of NIR light in the spongy mesophyll that comprises the leaf's internal structure, and increased absorption of visible and SWIR light from increased leaf moisture content. 
1) <b>Enhanced Vegetation Index 2 (EVI2)</b> = 2.5 * ( NIR - RED) / ( NIR + 2.4 * RED + 1.0 )    
2) <b>Green-Chlorophyll Vegetation Index (GCVI)</b> = (NIR – GREEN) / (NIR + GREEN)  

In ASA plots around November to February, crops should exhibit higher EVI2 and GCVI values than standing residue, as the slope of red and green to NIR is steeper for cover crops, caused by chlorophyll absorption of visible light and reflecting of NIR light in the spongy mesophyll. When cover crops are planted on ASA plots after postrera harvest, ASA EVI2 should see less of an EVI2 drop than Testigo, which shouldn't have any green vegetation. As the cover crops die near the end of the cover crop visibility window, ASA's EVI2 values should near Testigo values.


## <b>Crop residue:</b> differentiate ASA plots with standing crop residue from Test plots with grazed residue (leaving soil)  
- <b>Temporal window:</b> FEB to MAY - CR is left on both Test and ASA plots. Grazing occurs on Test, so once residue has been grazed on Test & CC dies on ASA around Feb, Test plot should have soil and ASA plot should have standing residue  
- <b>Spectral window:</b>  Soil and dry vegetation look similar in visible and NIR wavelengths. However, cellulose in dry vegetation absorbs SWIR2 light more than soil, leading to lower reflectance in ASA's standing residue in the SWIR2 band than Testigo's soil.  
1) <b>Normalized Difference Tillage Index (NDTI)</b> = (SWIR1-SWIR2) / (SWIR1+SWIR2) First, the most prominent spectral difference between NPV and soil is the cellulose absorption feature in SWIR 2 wavelengths.   
2) <b>Normalized Burn Ratio (NBR)</b> = (NIR1-SWIR2) / (NIR1+SWIR2) 

In ASA plots around February to May, standing residue's cellulose absorption from the SWIR2 band should show a steeper slope between SWIR1 to SWIR2 bands and produce higher NDTI as well as NBR values in ASA plot pixels. Within this broad crop residue visibility window, as grazing occurs on Testigo plots, Testigo NDTI values should drop at a higher rate and reach a lower minimum NDTI value than ASA plots.