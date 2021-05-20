from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from dicom_manager.DCM_manager import Manager

# Create your views here.
#@login_required
@permission_required('admin.can_add_log_entry',login_url="/login_permission_error/")
def rtplan_consistency(request):
    context = {}
    if request.method == 'POST':
        x = Manager(request.FILES['rtplan_dcm'])
        temp = x.get_dcm_file()
        texto = []
        if temp is not None:
            for k in temp:
                texto.append(temp[k])
            context = {'output_text':texto}
        else:
            context = {'output_text':'Falhou'}

    return render(request, 'plan_consistency/consistency.html', context)

