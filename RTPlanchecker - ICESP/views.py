from DCM_manager import Manager
from verify_parameters import VerifyRTPlan



context = {}
#x = Manager('./files/RTPlan.dcm')
#x = Manager('./files/RTPlan_TESTEIMRT.dcm')
x = Manager('./files/RTPlan_2Rx.dcm')
#x = Manager('./files/RTPlan_isocentro.dcm')
#x = Manager('./files/teste_erro_iso.pdf')
temp = x.get_rtplan_info()
texto = []
if temp is not None:
    for k in temp[-1]:
        texto.append(temp[-1][k])
    context = {'output_text':texto}
    print('Nome: ' + str(temp[0][0]))
    print('ID: ' + str(temp[0][1]))
    print('Nome do plano: ' + str(temp[0][2]))
    y = VerifyRTPlan()


    for rx in context['output_text']:
        y.test_rx_field(rx[4])
        print('===================')
        print('Nome da prescrição: ' + rx[0])
        print('\tDose Total (cGy): ' + str(rx[1]))
        print('\tNúmero de Frações: ' + str(rx[2]))
        print('\tDose Diária (cGy): ' + str(rx[3]))
        if y.unique_patient_position:
            print('\tOrientação do paciente: ' + str(rx[4][0][8]))
        if y.unique_treatment_unit:
            print('\tIsocentro: ' + str(rx[4][0][7]))
        else:
            print('\tANTENCAO: CAMPOS PLANEJADOS EM ISOCENTROS DIFERENTES')
        if y.unique_iso:
            print('\tAL: ' + rx[4][0][4])
        else:
            print('\tANTENCAO: CAMPOS PLANEJADOS EM DIFERENTES UNIDADES DE TRATAMENTO')
        if not y.unique_id:
            print('\tANTENCAO: CAMPOS COM IDS REPETIDOS')
        if not y.unique_name:
            print('\tANTENCAO: CAMPOS COM NOMES REPETIDOS')
        for j in rx[4]:
            print('\t--> ID do campo: ' + j[0]) # [ID, Nome, Treatment Delivery Type, Beam Type, AL, Radiation Type, Energia, Iso, Orientacao, *DRP*, *Dose no DRP (Gy)*, *MU*]
            print('\t\t\tNome do campo: ' + j[1])
            print('\t\t\tTipo de campo: ' + j[2])
            print('\t\t\tTécnica de tratamento: ' + j[3])
            if not y.unique_treatment_unit:
                print('\t\t\tAL: ' + j[4])
            print('\t\t\tTipo de feixe: ' + j[5])
            print('\t\t\tEnergia: ' + str(j[6]))
            if not y.unique_iso:
                print('\t\t\tIsocentro: ' + str(j[7]))
            if not y.unique_patient_position:
                print('\t\t\tOrientação do paciente: ' + str(j[8]))
            print('\t\t\tDRP: ' + str(j[9]))
            print('\t\t\tDose no DRP (Gy): ' + str(j[10]))
            print('\t\t\tMU: ' + j[11])


else:
    context = {'output_text':'Falhou'}
    print(context['output_text'])