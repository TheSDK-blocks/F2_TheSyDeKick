#!/usr/bin/env bash

help_f()
{
cat << EOF
 INIT_SUBMODULES Release 1.1 (06.09.2018)
 Templete generator for TheSDK entities
 Written by Marko Pikkis Kosunen
 -n
 SYNOPSIS
   init_submodules.sh
 DESCRIPTION
   Initializes the submoduels with selective recursion
 -n
 OPTIONS

   -h
       Show this help.
EOF
}
INITGEN="1"
while getopts h opt
do
  case "$opt" in
    h) help_f; exit 0;;
    \?) help_f; exit 0;;
  esac
  shift
done

DIR="$( cd "$( dirname $0 )" && pwd )"
cd $DIR
git submodule sync
for module in \
    ./Entities/thesdk_helpers \
    ./Entities/thesdk \
    ./Entities/verilog \
    ./Entities/signal_generator_802_11n \
    ./Entities/halfband \
    ./Entities/halfband_interpolator \
    ./Entities/cic3 \
    ./Entities/cic3_interpolator \
    ./Entities/f2_decimator \
    ./Entities/f2_interpolator \
    ./Entities/f2_scan_controller \
    ./Entities/segmented_dac \
    ./Entities/FFT \
    ./Entities/channel_equalizer \
    ./Entities/f2_symbol_sync \
    ./Entities/f2_adc \
    ./Entities/f2_rx_dsp \
    ./Entities/f2_tx_path \
    ./Entities/f2_tx_dsp \
    ./Entities/f2_dsp \
    ./Entities/f2_chip \
    ./Entities/f2_testbench \
    ./Entities/f2_channel \
    ./Entities/modem \
    ./Entities/multirate \
    ./Entities/ofdm_rx \
    ./Simulations/Slidetemplate \
    ./Simulations/Simtemplate; do
    git submodule update --init $module
    cd ${module}
    if [ -f ./init_submodules.sh ]; then
        ./init_submodules.sh
    fi
    cd ${DIR}
done

exit 0

