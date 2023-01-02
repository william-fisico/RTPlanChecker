import pydicom
import os, datetime

ds = pydicom.dcmread('RTDOSE.dcm')

print(ds.ReferencedFrameOfReferenceSequence)
