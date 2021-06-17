from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from dicom_manager.DCM_manager import Manager
from .verify_parameters import VerifyRTPlan


# Create your views here.
#@login_required
@permission_required('admin.can_add_log_entry',login_url="/login_permission_error/")
def rtplan_consistency(request):
    context = {}
    if request.method == 'POST':
        x = Manager(request.FILES['rtplan_dcm'])
        temp = x.get_rtplan_info()
        rx_list = []
        if temp is not None:
            y = VerifyRTPlan()
            #for k in temp[-1]:
            #temp[-1[[k] = ['Rx-k name', 'Total dose Rx-k (Gy)', 'Rx-k Number of fractions', 'Rx-k Fractional Dose (Gy)', 'Rx-k Fields List']
            for k in temp[1]:
                y.test_rx_field(temp[1][k][4])
                rx_temp = [temp[1][k][i] for i in range(4)]
                if y.unique_patient_position:
                    rx_temp.append(temp[1][k][4][0][8])
                else:
                    rx_temp.append('PLANEJAMENTO COM INCONSISTÊNCIA NA ORIENTAÇÃO DO PACIENTE')
                if y.unique_treatment_unit:
                    rx_temp.append(temp[1][k][4][0][4])
                else:
                    rx_temp.append('ANTENCAO - CAMPOS PLANEJADOS EM DIFERENTES UNIDADES DE TRATAMENTO')
                if y.unique_iso:
                    rx_temp.append(temp[1][k][4][0][7])
                else:
                    rx_temp.append('ANTENCAO - CAMPOS PLANEJADOS EM ISOCENTROS DIFERENTES')

                rx_list.append(rx_temp)


            context = {'plan_id':temp[0], 'rx_list':rx_list, 'is_RTPlan':True}


            '''for rx in rx_list:
                y.test_rx_field(rx[4])
                #print('===================')
                #print('Nome da prescrição: ' + rx[0])
                #print('\tDose Total (cGy): ' + str(rx[1]))
                #print('\tNúmero de Frações: ' + str(rx[2]))
                #print('\tDose Diária (cGy): ' + str(rx[3]))
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
            '''

        

    return render(request, 'plan_consistency/consistency.html', context)
    

