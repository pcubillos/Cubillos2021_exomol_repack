# Define topdir (in your top working directory) to make your life easier:
topdir=`pwd`

# Clone (download) the necessary code:
pip install lbl-repack==1.4.2

# Download Exomol data:
cd $topdir/inputs
wget -i wget_exomol_H2O_pokazatel.txt
wget -i wget_exomol_CH4_yt34to10.txt
wget -i wget_exomol_CO2_ucl4000.txt
wget -i wget_exomol_NH3_coyute.txt
wget -i wget_exomol_NH3_byte15.txt
wget -i wget_exomol_HCN_harris-larner.txt
wget -i wget_exomol_TiO_toto.txt
wget -i wget_exomol_VO_vomyt.txt
wget -i wget_exomol_C2H2_acety.txt
wget -i wget_exomol_C2H4_mayty.txt

# Partition functions:
# Use TIPS partition functions for molecules with Exomol PFs lower
# than 3000 K:
cd $topdir/inputs
pbay -pf tips NH3  as_exomol
pbay -pf tips C2H4 as_exomol
pbay -pf tips CH4  as_exomol


# Resort MARVELised datasets:
cd $topdir
repack -sort repack_exomol_H2O_pokazatel.cfg
repack -sort repack_exomol_NH3_coyute.cfg

# Compress LBL databases:
cd $topdir/runs
repack repack_exomol_H2O_pokazatel.cfg
repack repack_exomol_CO2_ucl4000.cfg
repack repack_exomol_CH4_yt34to10.cfg
repack repack_exomol_HCN_harris-larner.cfg
repack repack_exomol_NH3_coyute-byte.cfg
repack repack_exomol_TiO_toto.cfg
repack repack_exomol_VO_vomyt.cfg
repack repack_exomol_C2H2_acety.cfg
repack repack_exomol_C2H4_mayty.cfg


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Benchmark:

# Make a generic hot-Jupiter atmospheric profile:
cd $topdir/benchmark
pbay -c atm_hot_jupiter.cfg

# Format partition functions and line lists for use in pyratbay:
cd $topdir/benchmark
pbay -pf exomol ../inputs/51V-16O__VOMYT.pf
pbay -pf exomol ../inputs/1H2-16O__POKAZATEL.pf

cd $topdir/benchmark
pbay -c tli_repacked_VO.cfg
pbay -c tli_repacked_H2O.cfg
pbay -c tli_exomol_H2O.cfg

# VO opacity spectrum benchmark:
cd $topdir/benchmark
python ../code/fig_VO_opacity.py

# H2O transmission spectrum benchmark:
cd $topdir/benchmark
python ../code/fig_H2O_spectra.py

