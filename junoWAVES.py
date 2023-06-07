import cdflib
from astropy.time import Time, TimeDelta
import numpy as np

def PlotData(fig, ax, timeFrame, plotEphemeris=False):
    # Takes one of the subplot axes as input
    # NOTE: Functionality to automatically download the data would be useful
    
    print("Retrieving waves data...")

    wavesPath = "./data/waves/data/l3a_v02/data/cdf/2022/01/jno_wav_cdr_lesia_20220101_v02.cdf"

    wavesCDF = cdflib.CDF(wavesPath)
    
    epoch = wavesCDF.varget("Epoch")
    epochUnit = wavesCDF.varinq("Epoch")["Data_Type_Description"] # Time since 2000-01-01 in nanoseconds

    time = Time(epoch, format="cdf_tt2000")
    time.format = "isot"

    # Check if WAVES time matches overall timeFrame
    if time[0] >= timeFrame[0] or time[-1] <= timeFrame[1]:
        print("WARNING: Waves epoch from file is shorter than that provided time frame")
        print(f"WARNING: Waves start time: {time[0]}, waves end time: {time[-1]}")
        print(f"WARNING: Timeframe: {timeFrame}")

    frequency = wavesCDF.varget("Frequency")

    wavesData = np.transpose(wavesCDF.varget("Data"))
    print(np.shape(wavesData))

    # Adapted code taken from Corentin
    index_array = range(len(time))

    image = ax.pcolormesh(index_array, frequency, wavesData, cmap="Spectral_r")

    # cax = divider.append_axes("right", size=0.15, pad=0.2)

    fig.colorbar(image, extend='both', shrink=0.9,ax=ax)
