# Define topdir (in your top working directory) to make your life easier:
topdir=`pwd`

# Clone (download) the necessary code:
pip install lbl-repack==1.4.2

# Download Exomol data:
cd $topdir/inputs
wget -i wget_exomol_H2O_pokazatel.txt
wget -i wget_exomol_C2H2_acety.txt
wget -i wget_exomol_CH4_yt10to10.txt
wget -i wget_exomol_NH3_coyute.txt
wget -i wget_exomol_NH3_byte15.txt
wget -i wget_exomol_HCN_harris-larner.txt
wget -i wget_exomol_TiO_toto.txt
wget -i wget_exomol_VO_vomyt.txt

# Partition functions:
pbay -pf exomol ../inputs/46Ti-16O__Toto.pf \
                ../inputs/47Ti-16O__Toto.pf \
                ../inputs/48Ti-16O__Toto.pf \
                ../inputs/49Ti-16O__Toto.pf \
                ../inputs/50Ti-16O__Toto.pf

pbay -pf exomol ../inputs/51V-16O__VOMYT.pf

# Exomol PFs for these molecules stop at temps too low (< 3000K),
# use HITRAN/TIPS PFs instead:
pbay -pf tips NH3  as_exomol
pbay -pf tips C2H4 as_exomol


# Resort MARVELised datasets:
cd $topdir
repack -sort repack_exomol_H2O_pokazatel.cfg
repack -sort repack_exomol_NH3_coyute.cfg

# Compress LBL databases:
cd $topdir/runs
repack repack_exomol_H2O_pokazatel.cfg
repack repack_exomol_CO2_ucl4000.cfg
repack repack_exomol_CH4_yt10to10.cfg
repack repack_exomol_HCN_harris-larner.cfg
repack repack_exomol_NH3_coyute-byte.cfg
repack repack_exomol_TiO_toto.cfg
repack repack_exomol_VO_vomyt.cfg
repack repack_exomol_C2H2_acety.cfg
repack repack_exomol_C2H4_mayty.cfg
#repack repack_exomol_H2S_ayt2.cfg


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Validation:
pbay -c tli_repacked_VO.cfg
pbay -c tli_repacked_H2O.cfg
pbay -c tli_exomol_H2O.cfg



