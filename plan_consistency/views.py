from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from dicom_manager.DCM_manager import Manager

# Create your views here.
@login_required
@permission_required('admin.can_add_log_entry',login_url="/login_permission_error/")
def rtplan_consistency(request):
    context = {}
    if request.method == 'POST':
        x = Manager(request.FILES['rtplan_dcm'])
        if x.get_dcm_file() is not None:
            context = {'output_text':x.get_dcm_file}
        else:
            context = {'output_text':'Falhou'}

    return render(request, 'plan_consistency/consistency.html', context)

