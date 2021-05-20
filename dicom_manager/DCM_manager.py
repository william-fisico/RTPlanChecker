import pydicom
from pydicom import dcmread
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
import numpy as np
from datetime import datetime

'''
Manger: classe para gerenciar os arquivos DICOM.
Ao inicializar a classe, o construtor carrega o arquivo informado no argumento da classe e verifica se este é válido
'''
class Manager:

    def __init__(self, file):
        #Ao inicializar a classe, o construtor carrega o arquivo informado no argumento da classe e verifica se este é válido

        #self.ids = None
        #self.grid_calc = None
        #self.rx_prescription = None #lista com todas as precirções do plano

        modality_list = ['RTSTRUCT', 'RTDOSE', 'RTPLAN']
        try:
            temp_dcm = pydicom.filereader.read_file(file, force=True)
            modality = temp_dcm[0x0008,0x0060].value
            if modality in modality_list:
                self.dcm_file = temp_dcm
                self.set_dcm_info(modality)
            else:
                self.dcm_file = None

        except:
            self.dcm_file = None

    def get_dcm_file(self):
        return self.rx_prescription

    def set_ids(self, is_rtplan = False):
        #define a identificação de paciente e plano ==> self.ids = ['patient_name','patient_id','plan_id ']
        if is_rtplan:
            self.ids = [self.dcm_file[0x0010,0x0010].value, self.dcm_file[0x0010,0x0020].value, self.dcm_file[0x300a,0x0003].value]
        else:
            self.ids = [self.dcm_file[0x0010,0x0010].value, self.dcm_file[0x0010,0x0020].value]

    def set_grid_calc(self):
        self.grid_calc = max(self.dcm_file[0x0028,0x0030])

    def set_rx_prescription(self):

        rx_name_list = {} # rx_name_list = {'Rx1 reference number':['Rx1 name', 'Total dose Rx1 (Gy)'],...,'Rx1 reference number':['RxN name', 'Total dose RxN (Gy)']}
        for rx in self.dcm_file[0x300a,0x0010]: #(300a, 0010) Dose Reference Sequence
            if (rx[0x300a,0x0014].value == 'SITE'): #(300a, 0012) Dose Reference Number 
                rx_name_list[rx[0x300a,0x0012].value] = [rx[0x300a,0x0016].value, rx[0x300a,0x0026].value]
        self.rx_prescription = rx_name_list

        for x in self.dcm_file[0x300a,0x0070]: #loop dentro do grupo de parametros de cada prescricao
            print('====')
            print(x[0x300c,0x0050][0])

    def set_dcm_info(self, modality):
        if modality == 'RTPLAN':
            self.set_ids(is_rtplan=True)
            self.set_rx_prescription()
        elif modality== 'RTDOSE':
            self.set_grid_calc()
            self.set_ids()
        elif modality == 'RTSTRUCT':
            self.set_ids()
