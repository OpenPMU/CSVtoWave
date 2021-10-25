# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 17:31:39 2021

@author: OpenPMU.org
@license: GPLv3
"""

import csv
import soundfile as sf
import numpy as np
import os

def gen_chunks(reader, chunksize):
    """ 
    Chunk generator. Take a CSV `reader` and yield
    `chunksize` sized slices. 
    """
    chunk = []
    for index, line in enumerate(reader):
        if (index % chunksize == 0 and index > 0):
            yield chunk
            del chunk[:]
        chunk.append(line)
    yield chunk

# https://stackoverflow.com/questions/56058997/append-data-to-a-wave-soundfile-without-loading-its-currrent-content

if __name__ == "__main__":
    
    csvFilePath  = 'VI Snapshot.csv'
    waveFilePath = 'Output2.wav'
    sampleRate   = 12800
    Channels     = 2
    
    csvReader = csv.reader(open(csvFilePath, 'r'))    
        
    with sf.SoundFile(waveFilePath, 'w+', sampleRate, Channels) as waveFile:
        
        waveFile.seek(0,sf.SEEK_END)
        
        for chunk in gen_chunks(csvReader, chunksize=128):
            samples = (np.array(chunk).astype(np.float32) * 32767/5.0 ).astype(np.int16)
            fs=12800
            waveFile.write(samples)
                