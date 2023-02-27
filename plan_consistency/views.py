from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from dicom_manager.RTDCM_manager import Manager, Verify_RTPlan, Verify_RTDose
#from DCM_manager import Manager
#from .verify_parameters import VerifyRTPlan
import os
from pydicom import dcmread


def list_patients():
    root = './Store_sSCU_test/'
    list_pacs = []

    for entry in os.listdir(root):
        search_name = True
        if os.path.isdir(root + entry): # and entry.startswith("PACS_"):
            os.chdir(root + entry)
            list_files = os.listdir('.')
            cont = 0
            while (cont < len(list_files)) and search_name:
                if list_files[cont].endswith('.dcm'):
                    try:
                        file = Manager(os.path.abspath(list_files[cont]))
                        list_pacs.append(file.get_ids())
                        search_name = False
                    except:
                        search_name = True
                cont += 1
            os.chdir("../..")
    return list_pacs # [[patient's name, patient's id]]


def list_plans(pacs):
    root = './Store_sSCU_test/'
    plan_list = []
    try:
        os.chdir(root + pacs)
        try:
            plan_list = [(os.path.abspath(file), Manager(os.path.abspath(file)).get_rtplan_name()) for file in os.listdir('.') if (file.startswith('RTPLAN') and file.endswith('.dcm'))]
            temp_dcm = Manager(plan_list[0][0])
            dcm_id = temp_dcm.get_ids()
        except:
            plan_list = None
            dcm_id = None
        os.chdir("../..") 
    except:
        plan_list = None
        dcm_id = None

    return [dcm_id, plan_list] # [[patient's name, patient's id], [plan_list]]


def load_rt_dcm(plan_path):
    rt_plan = Manager(plan_path)
    patient_id = rt_plan.get_ids()
    rtstruct_uid = rt_plan.get_referenced_rtstruct()
    rtplan_uid = rt_plan.get_sop_instance_uid()
    root = './Store_sSCU_test/' + patient_id[1]
    try:
        os.chdir(root)
        try:
            rt_dose_list = [os.path.abspath(file) for file in os.listdir('.') if (file.startswith('RTDOSE') and file.endswith('.dcm') and Manager(os.path.abspath(file)).get_referenced_rtplan()==rtplan_uid)]
            if len(rt_dose_list) != 1 : rt_dose_list = None
        except:
            rt_dose_list = None
        try:
            rt_struct_list = [os.path.abspath(file) for file in os.listdir('.') if (file.startswith('RTSTRUCT') and file.endswith('.dcm') and Manager(os.path.abspath(file)).get_sop_instance_uid()==rtstruct_uid)]
            if len(rt_struct_list) != 1 : rt_struct_list = None
        except:
            rt_struct_list = None
        os.chdir("../..")
    except:
        rt_dose_list = None
        rt_struct_list = None

    rt_dose = Manager(rt_dose_list[0]) if rt_dose_list is not None else None
    rt_struct = Manager(rt_struct_list[0]) if rt_struct_list is not None else None

    return [rt_plan, rt_dose, rt_struct]


# Create your views here.
#@login_required
@permission_required('admin.can_add_log_entry',login_url="/login_permission_error/")
def rtplan_consistency(request):
    context = {}

    if request.method == 'GET':
        context['is_PACSlist'] = True
        context['patients'] = list_patients()
    elif request.method == 'POST':
        data = request.POST
        pacs = data.get("pacs")
        rtplan_path = data.get("rtplan_path")
        if pacs is not None:
            patient_id, plan_list = list_plans(pacs)
            if plan_list is not None:
                context['is_Planlist'] = True
                context['Patient_Id'], context['PlanList'] = patient_id, plan_list
            else:
                context['is_PACSlist'] = True
                context['patients'] = list_patients()
                messages.success(request, ('Não existe nenhum plano associado ao paciente selecionado. Por Favor verifique.'))
        elif rtplan_path is not None:
            context['is_PlanData'] = True
            rt_plan, rt_dose, rt_struct = load_rt_dcm(rtplan_path)
            if rt_dose is None : messages.success(request, ('Não existe arquivo de dose associado ao plano selecionado. Por Favor verifique.'))
            if rt_struct is None : messages.success(request, ('Não existe arquivo de estruturas associado ao plano selecionado. Por Favor verifique.'))
            # rtplan_info = {'Rx-i reference number':['Rx-i name', 'Total dose Rx-i (Gy)', 'Rx-i Number of fractions', 'Rx-i Fractional Dose (Gy)', 'Rx-i Fields List']
            # Rx-i Fields List = [ID, Nome, Treatment Delivery Type, Beam Type, AL, Radiation Type, Energia, Iso, Orientacao, *DRP*, *Dose no DRP (Gy)*, *MU*]
            context['RTPLAN_info'] = rt_plan.get_rtplan_info()
            context['is_RTPLAN'] = True
            context['Patient_Id'] = rt_plan.get_ids()
            teste = Verify_RTPlan(rt_plan,rt_struct)
            grid = Verify_RTDose(rt_dose)

        else:
            context['is_PACSlist'] = True
            context['patients'] = list_patients()



    return render(request, 'plan_consistency/consistency.html', context)
