class VerifyRTPlan():

    def __init__(self):
        self.id_list = []
        self.unique_id = True
        pass


    def test_grid(self,grid,limit):
        if grid <= limit:
            self.grid = True
            return  self.grid
        else:
            self.grid = False
            return self.grid

    
    def test_rx_field(self, rx): 
        #['Field ID', 'Field Name', 'Treatment Unit', 'Energy', 'Isocenter', 'Patient Setup', 'DRP', 'DRP Dose (cGy)', 'MU'] 
        self.unique_name = True
        self.unique_iso = True
        self.unique_treatment_unit = True
        self.unique_patient_position = True
        name_list = []
        iso_list = []
        treatment_unit_list = []
        patient_position_list = []

        for j in rx:
            if j[0] in self.id_list:
                self.unique_id = False
            else:
                self.id_list.append(j[0])
            
            if j[1] in name_list:
                self.unique_name = False
            else:
                name_list.append(j[1])

            if not j[4] in treatment_unit_list:
                treatment_unit_list.append(j[4])

            if not j[7] in iso_list:
                iso_list.append(j[7])

            if not j[8] in patient_position_list:
                patient_position_list.append(j[8])


            '''print('*********************************')
            print('\t--> ID do campo: ' + j[0]) # [ID, Nome, Treatment Delivery Type, Beam Type, AL, Radiation Type, Energia, Iso, Orientacao, *DRP*, *Dose no DRP (Gy)*, *MU*]
            print('\t\t\tNome do campo: ' + j[1])
            print('\t\t\tTipo de campo: ' + j[2])
            print('\t\t\tTécnica de tratamento: ' + j[3])
            print('\t\t\tAL: ' + j[4])
            print('\t\t\tTipo de feixe: ' + j[5])
            print('\t\t\tEnergia: ' + str(j[6]))
            print('\t\t\tIsocentro: ' + str(j[7]))
            print('\t\t\tOrientação do paciente: ' + str(j[8]))
            print('\t\t\tDRP: ' + str(j[9]))
            print('\t\t\tDose no DRP (Gy): ' + str(j[10]))
            print('\t\t\tMU: ' + j[11])
            print('*********************************')'''
        
        if len(iso_list) != 1:
            self.unique_iso = False
        if len(treatment_unit_list) != 1:
            self.unique_treatment_unit = False
        if len(patient_position_list) != 1:
            self.unique_patient_position = False