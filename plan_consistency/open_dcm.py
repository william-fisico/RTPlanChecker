import pydicom
from pydicom import dcmread
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
import numpy as np
from datetime import datetime

def verifica_grade(grade, tecnica):
    global limites_grade_calculo

    limites_grade_calculo = {'3D':3.0, 'VMAT':3.0, 'SBRT':2.0, 'SRS':1.0}
    tecnica = tecnica.upper()
    if grade <= limites_grade_calculo[tecnica]:
        return True
    else:
        return False


class OpenRTPlan():

    def OpenRTPlanDCM(self, rtplan_file):
        global plan_parameters
        #rtplan_file = '../' + rtplan_file
        rtplan = pydicom.filereader.read_file(rtplan_file, force=True)

        plan_parameters = dict()

        plan_parameters['Nome do paciente'] = rtplan[0x0010,0x0010].value
        plan_parameters['ID do paciente'] = rtplan[0x0010,0x0020].value
        plan_parameters['Nome do plano'] = rtplan[0x300a,0x0003].value
        plan_parameters['Grade de calculo (mm)'] = 3.0 # (max(rtdose[0x0028,0x0030])) grade de calculo esta no arquivo dicom de dose (rtdose)
        limites_grade_calculo = {'3D':3.0, 'VMAT':3.0, 'SBRT':2.0, 'SRS':1.0}

        campos = {}
        for x in rtplan[0x300a,0x00b0]:
            t = {'ID do campo':x[0x300a,0x00c2].value, 'Nome do campo':x[0x300a,0x00c3].value, 'Acelerador linear':x[0x300a,0x00b2].value, 'Energia':x[0x300a,0x0111][0][0x300a,0x0114].value, 'Isocentro':x[0x300a,0x0111][0][0x300a,0x012c].value, 'Orientacao':x[0x300c,0x006a].value}# [ID, Nome, AL, Energia, Iso, Orientacao, *DRP*, *Dose no DRP (Gy)*, *MU*]
            campos[x[0x300a,0x00c0].value] = t

        dose_ref_seq = rtplan[0x300a,0x0010] #(300a, 0010) Dose Reference Sequence
        rx_dict = {} # dict de prescrições
        for rx in dose_ref_seq:
            if (rx[0x300a,0x0014].value == 'SITE'):
                rx_dict = {}
                plan_parameter_rx = 'Prescricao ' + str(rx[0x300a,0x0012].value)
                rx_dict['Nome Rx'] = rx[0x300a,0x0016].value
                rx_dict['Dose Total (Gy)'] = rx[0x300a,0x0026].value
                plan_parameters[plan_parameter_rx] = rx_dict


        for x in rtplan[0x300a,0x0070]:
            for y in x[0x300c,0x0050]:
                rx_ref_nome = 'Prescricao ' + str(y[0x300c,0x0051].value) 
                rx_ref = plan_parameters[rx_ref_nome]
            rx_ref['Numero de fracoes'] = x[0x300a,0x0078].value
            d_total = float(rx_ref['Dose Total (Gy)'])
            n_fracoes = float(rx_ref['Numero de fracoes'])
            d_dia = d_total/n_fracoes
            rx_ref['Dose por fracao (Gy)'] = d_dia
            rx_ref['Numero de campos'] = x[0x300a,0x0080].value
            rx_ref['Campos'] = {}

            for y in x[0x300c,0x0004]:
                temp = campos[y[0x300c,0x0006].value]
                temp['DRP'] = y[0x300a,0x0082].value
                temp['Dose no DRP (Gy)'] = y[0x300a,0x0084].value
                try:
                    temp['MU'] = str(y[0x300a,0x0086].value)
                except:
                    temp['MU'] = str(0.0)
                campos[y[0x300c,0x0006].value] = temp
                rx_ref['Campos'][y[0x300c,0x0006].value] = temp   #Continua na seção Campos de tratamento


            plan_parameters[rx_ref_nome] = rx_ref

        plan_parameters['Autor'] = 'William A. P. dos Santos'
        plan_parameters['Data'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        return plan_parameters

    def PrintPlanParameter(self):
        outuput_text = []
        id = []
        id_repetido = False
        for parametro in plan_parameters:
            if 'Prescricao' in parametro:
                for x in plan_parameters[parametro]:
                    if 'Nome Rx' in x:
                        outuput_text.append(x + ': ' + str(plan_parameters[parametro][x]))
                    else:
                        if not 'Campos' in x:                # [ID, Nome, AL, Energia, Iso, Orientacao, *DRP*, *Dose no DRP (Gy)*, *MU*]
                            outuput_text.append('\t' + x + ': ' + str(plan_parameters[parametro][x]))
                        else:
                            temp = plan_parameters[parametro][x]
                            primeiro_campo = True
                            iso_unico = True
                            al_unico = True
                            for y in temp:
                                temp_list = temp[y]
                                outuput_text.append('\tCampo ' + str(y) + ':')
                                for z in temp_list:
                                    outuput_text.append('\t\t' + str(z) + ': ' + str(temp_list[z]))
                                    if 'Isocentro' in z:
                                        if primeiro_campo:
                                            iso = temp_list[z]
                                        else:
                                            if iso != temp_list[z]:
                                                iso_unico = False
                                    elif 'Acelerador' in z:
                                        if primeiro_campo:
                                            al = temp_list[z]
                                        else:
                                            if al != temp_list[z]:
                                                al_unico = False
                                    elif 'ID' in z:
                                        if primeiro_campo:
                                            id.append(temp_list[z])
                                        else:
                                            if temp_list[z] in id:
                                                id_repetido = True
                                            else:
                                                id.append(temp_list[z])
                                primeiro_campo = False
                            if iso_unico:
                                outuput_text.append('Todos os campos com mesmo isocentro')
                            else:
                                outuput_text.append('ANTENCAO: CAMPOS COM DIFERENTES ISOCENTROS')
                            if al_unico:
                                outuput_text.append('Todos os campos planejados no mesmo acelerador linear')
                            else:
                                outuput_text.append('ANTENCAO: CAMPOS PLANEJADOS EM DIFERENTES ACELERADORES LINEAR')
            else:
                outuput_text.append(parametro + ': ' + str(plan_parameters[parametro]))
        if id_repetido:
            outuput_text.append('ATENCAO: PLANO COM ID DOS CAMPOS REPETIDOS')

        # verificação da grade nao esta pronta, é apenas teste
        grade_ok = verifica_grade(float(plan_parameters['Grade de calculo (mm)']), '3D')
        if grade_ok:
            outuput_text.append('Grade de cálculo correta')
        else:
            outuput_text.append('VERIFIQUE A GRADE DE CÁLCULO')

        return outuput_text
