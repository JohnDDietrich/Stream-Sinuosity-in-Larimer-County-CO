# Stream-Sinuosity-in-Larimer-County-CO



<h2>Description</h2>
This final project for a GIS programing courese evaluated the stream network in Larimer County Colorado.  Minor streams were removed and then sinuosity and slope calculations were performed on the more significant of the Cache la Poudre watershed within Larimer County.  Further the code was designed so that anyone could perform the same calculations in their area if they provide a stream file and the appropriate DEM files.

<br />


<h2>Workflow overview</h2>

- <b>Take user input for calculations</b> 
- <b>Select significant stream reaches</b>
- <b>Find endpoints</b>
- <b>Performe calculations, strait ling slope, stream slope, and sinuosity</b>

<h2>Python code written using PyCharm IDE </h2>


<h2>C</h2>

<p align="center">
Code:

<img src="https://github.com/JohnDDietrich/GISMontenegro/blob/main/Classify.PNG" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />
<br />
Add in water features  <br/>
<img src="https://github.com/JohnDDietrich/GISMontenegro/blob/main/buffer1.PNG" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />
<br />
Create a 1km buffer around water features  <br/>
<img src="https://github.com/JohnDDietrich/GISMontenegro/blob/main/Buffer2.PNG" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />
<br />
Find intersection between water buffer and 1500+ elevation polygons <br/>
<img src="https://github.com/JohnDDietrich/GISMontenegro/blob/main/MNE_intersect.PNG" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />
<br />
Add in hillshade for visual effect  <br/>
<img src="https://github.com/JohnDDietrich/GISMontenegro/blob/main/MNE_map.PNG" height="80%" width="80%" alt="Disk Sanitization Steps"/>

<!--
 ```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
--!>
