##DNVGL-ST-0111 Environment Loads

Scripts to calculate <b>environment loads only</b> (wind, current and waves) as per DNVGL-ST-0111 (Assessment of station keeping capability of
dynamic positioning vessels), ed. July 2016.
There are few files in the folder:
1. Beaufort_scale.csv, as per Table 2-1 of DNVGL-ST-0111, fof Beaufort number (BN) from 0 to 11. Required for one of the scripts.
2. DNVGLST0111F.py with functions required for calculation.
3. DNVGL-ST-0111_BF - Python and Jupyter version of script to calculate environmental loads for all BN's in Beaufort_scale.csv for range of directions (0-360 deg). Both files doing the same - sending output to the folder "Results" in txt-file and creating polar plots for each BN. During input refer to DNVGL' standard.
4. DNVGL-ST-0111EnvLoadsSite - Python and Jupyter version of script to calaculate envirnment loads for "site" - speed and direction of the current, wind and waves are input. Environment loads are printed in terminal or Jupyter workbook.

###Note:

Use it on your own responsibility - no any warranties.</p>
Carefull with the input - check DNVGL-ST-0111 Standard for explanations.

Script calculate only environment forces - no stattion keeping part and no DP capability plots.