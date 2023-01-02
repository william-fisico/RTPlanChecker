from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from dicom_manager.DCM_manager import Manager
from .verify_parameters import VerifyRTPlan
import os
from pydicom import dcmread


def list_patients():
    root = './Store_sSCU_test/'
    patient_dict = {} # patient_dict = {pacs:plan_list}

    for entry in os.listdir(root):

        if os.path.isdir(root + entry) and entry.startswith("PACS_"):
            os.chdir(root + entry)
            plan_list = [] #plan_list[(plan_name, file_path)]
            #id_list.append(entry.replace("PACS_", ""))
            for file in os.listdir('.'):
                if file.startswith('RTPLAN') and file.endswith('.dcm'):
                    temp_dcm = dcmread(file, force=True)
                    plan_name = temp_dcm[0x300A,0x0003].value
                    file_path = os.path.abspath(file)
                    plan_list.append((plan_name,file_path))
            patient_dict[entry.replace("PACS_", "")] = plan_list
            os.chdir("../..")
    return patient_dict


# Create your views here.
#@login_required
@permission_required('admin.can_add_log_entry',login_url="/login_permission_error/")
def rtplan_consistency(request):
    context = {}
    if request.method == 'POST':
        try:
            data = request.POST
            pacs = data.get("pacs")
            pacs_dic = list_patients()
            plan_list = pacs_dic[pacs]
            context['is_Planlist'] = True
            context['PlanList'] = plan_list
        except:
            plan_list = None

        if plan_list is None:
            try:
                data = request.POST
                x = Manager(data.get("rtplan_dcm"))
                temp = x.get_rtplan_info()
            except:
                temp = None
            rx_list = []
            if temp is not None:
                context = {'plan_id':temp[0]}
                y = VerifyRTPlan()
                #for k in temp[-1]:
                #temp[-1[[k] = ['Rx-k name', 'Total dose Rx-k (Gy)', 'Rx-k Number of fractions', 'Rx-k Fractional Dose (Gy)', 'Rx-k Fields List']
                for k in temp[1]:
                    position_warning = False
                    iso_warning = False
                    treatment_unit_warning = False
                    y.test_rx_field(temp[1][k][4])
                    rx_temp = [temp[1][k][i] for i in range(4)]
                    if y.unique_patient_position:
                        rx_temp.append(temp[1][k][4][0][8])
                    else:
                        rx_temp.append('PLANEJAMENTO COM INCONSISTÊNCIA NA ORIENTAÇÃO DO PACIENTE')
                        position_warning = True
                        messages.success(request, ('Prescrição ' + rx_temp[0] + ' possui inconsistência na orientação do paciente. Por favor verifique.'))
                    if y.unique_treatment_unit:
                        rx_temp.append(temp[1][k][4][0][4])
                    else:
                        rx_temp.append('ANTENCAO - CAMPOS PLANEJADOS EM DIFERENTES UNIDADES DE TRATAMENTO')
                        treatment_unit_warning = True
                        messages.success(request, ('Prescrição ' + rx_temp[0] + ' possui campos planejados em diferentes unidades de tratamento. Por favor verifique.'))
                    if y.unique_iso:
                        rx_temp.append(temp[1][k][4][0][7])
                    else:
                        rx_temp.append('ANTENCAO - CAMPOS PLANEJADOS EM ISOCENTROS DIFERENTES')
                        iso_warning = True
                        messages.success(request, ('Prescrição ' + rx_temp[0] + ' possui campos planejados em isocentros diferentes. Por favor verifique.'))

                    field_info_list = [] #[field.append([position_warning, treatment_unit_warning, iso_warning]) for field in temp[1][k][4]]
                    for field in temp[1][k][4]:
                        #field.append([treatment_unit_warning, iso_warning, position_warning])
                        field_info_list.append(field)
                    rx_temp.append(field_info_list)
                    rx_temp.append([treatment_unit_warning, iso_warning, position_warning])
                    rx_list.append(rx_temp)

                context['rx_list'] = rx_list
                context['is_RTPlan'] = True

            else:
                messages.success(request, ('Por favor selecione um arquivo válido.'))
                context['patients'] = list_patients()

    else:
        #print(request.VALUE['1'])
        context['patients'] = list_patients()
        context['is_PACSlist'] = True

    return render(request, 'plan_consistency/consistency.html', context)
    

