from pydicom import dcmread

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

        modality_list = ['RTSTRUCT', 'RTDOSE', 'RTPLAN', 'CT', 'RTIMAGE']
        self.is_valid = False
        try:
            temp_dcm = dcmread(file, force=True)
            self.modality = temp_dcm[0x0008,0x0060].value
            if self.modality in modality_list:
                self.is_valid = True
                self.dcm_file = temp_dcm
                self.ids = [self.dcm_file[0x0010,0x0010].value, self.dcm_file[0x0010,0x0020].value]
                if self.modality == 'RTPLAN' : self.set_rx_prescription()
            else:
                self.dcm_file = None
                self.ids = None
        except:
            self.dcm_file = None
            self.ids = None


    def get_ids(self):
        return self.ids


    def get_sop_instance_uid(self):
        if self.is_valid:
            if self.modality == 'RTPLAN' or self.modality == 'RTSTRUCT':
                return self.dcm_file[0x0008,0x0018].value
            elif self.modality == 'CT':
                return self.dcm_file[0x0020,0x000D].value
            else:
                return None
        else:
            return None


    def get_referenced_rtplan(self):
        if self.is_valid and (self.modality=='RTDOSE' or self.modality=='RTIMAGE'):
            return self.dcm_file[0x300C,0x0002][0][0x0008,0x1155].value
        else:
            return None


    def get_referenced_rtstruct(self):
        if self.is_valid and (self.modality=='RTDOSE' or self.modality=='RTPLAN'):
            return self.dcm_file[0x300C,0x0060][0][0x0008,0x1155].value
        else:
            return None


    def get_rtplan_name(self):
        if self.is_valid and self.modality=='RTPLAN':
            return self.dcm_file[0x300a,0x0003].value
        else:
            return None


    def get_rtplan_info(self):
        if self.is_valid and self.modality=='RTPLAN':
            return self.rx_prescription
        else:
            return None


    def set_grid_calc(self):
        self.grid_calc = max(self.dcm_file[0x0028,0x0030])


    def set_rx_prescription(self):
        #rx_name_list = {'Rx-i reference number':['Rx-i name', 'Total dose Rx-i (Gy)', 'Rx-i Number of fractions', 'Rx-i Fractional Dose (Gy)', 'Rx-i Fields List']

        patient_setup_list = {} # {'patient_setup_number':'Patient Position'} ==> Patient Position: HFS, FFS, HFP, FFP...
        for setup_sequence in self.dcm_file[0x300a,0x0180]:
            patient_setup_list[setup_sequence[0x300a,0x0182].value] = setup_sequence[0x0018,0x5100].value
        

        ### Adicionar campos de tratamento
        fields = {}
        for x in self.dcm_file[0x300a,0x00b0]:
            t = [x[0x300a,0x00c2].value, x[0x300a,0x00c3].value, x[0x300a,0x00ce].value, x[0x300a,0x00c4].value, x[0x300a,0x00b2].value, x[0x300a,0x00c6].value, x[0x300a,0x0111][0][0x300a,0x0114].value, x[0x300a,0x0111][0][0x300a,0x012c].value, patient_setup_list[x[0x300c,0x006a].value]]# [ID, Nome, Treatment Delivery Type, Beam Type, AL, Radiation Type, Energia, Iso, Orientacao, *DRP*, *Dose no DRP (Gy)*, *MU*]
            fields[x[0x300a,0x00c0].value] = t

        rx_name_list = {} # rx_name_list = {'Rx1 reference number':['Rx1 name', 'Total dose Rx1 (Gy)'],...,'RxN reference number':['RxN name', 'Total dose RxN (Gy)']}
        for rx in self.dcm_file[0x300a,0x0010]: #(300a, 0010) Dose Reference Sequence
            if (rx[0x300a,0x0014].value == 'SITE'): #(300a, 0012) Dose Reference Number 
                rx_name_list[rx[0x300a,0x0012].value] = [rx[0x300a,0x0016].value, rx[0x300a,0x0026].value]

        for x in self.dcm_file[0x300a,0x0070]: #loop dentro do grupo de parametros de cada prescricao
            rx_field_list = []

            for y in x[0x300c,0x0004]: #(300c, 0004)  Referenced Beam Sequence ==> encontra os campos de cada prescrição
                fields[y[0x300c,0x0006].value].append(y[0x300a,0x0082].value) #DRP
                fields[y[0x300c,0x0006].value].append(y[0x300a,0x0084].value) #Dose no DRP (Gy)
                try:
                    fields[y[0x300c,0x0006].value].append(str(round(y[0x300a,0x0086].value, 1))) #MU
                except:
                    fields[y[0x300c,0x0006].value].append(str(0.0))  #MU
                rx_field_list.append(fields[y[0x300c,0x0006].value])

            for y in x[0x300c,0x0050]: #encontra a prescricao de referencia
                rx_name_list[y[0x300c,0x0051].value].append(x[0x300a,0x0078].value) # adiciona numero de frações ao rx_name_list['Rx-i reference nunber']
                daily_dose = float(rx_name_list[y[0x300c,0x0051].value][1])/float(x[0x300a,0x0078].value)
                rx_name_list[y[0x300c,0x0051].value].append(daily_dose) # adiciona dose diaria ao rx_name_list['Rx-i reference nunber']
                rx_name_list[y[0x300c,0x0051].value].append(rx_field_list) # adiciona a lista de campos ao rx_name_list['Rx-i reference nunber']

        self.rx_prescription = rx_name_list






    def print_dicom(self):
        print(self.dcm_file)
