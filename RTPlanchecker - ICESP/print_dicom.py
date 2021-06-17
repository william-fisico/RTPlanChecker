from DCM_manager import Manager

#x = Manager('./files/RTPlan.dcm')
#x = Manager('./files/RTPlan_TESTEIMRT.dcm')
x = Manager('./files/RTPlan_2Rx.dcm')
#x = Manager('./files/RTPlan_isocentro.dcm')
#x = Manager('./files/WL_2021-05-11a.pdf')

x.print_dicom()