from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .open_dcm import OpenRTPlan

# Create your views here.

def rtplan_consistency(request):
    context = {}
    if request.method == 'POST':
        upload_dcm = request.FILES['rtplan_dcm']
        rtplan = OpenRTPlan()
        rtplan.OpenRTPlanDCM(upload_dcm)
        context['output_text'] = rtplan.PrintPlanParameter()
        #fs = FileSystemStorage()
        #file_name = fs.save(upload_dcm.name, upload_dcm)
        #file_url = fs.url(file_name)
        #context['file_url'] = fs.url(file_name)
    return render(request, 'plan_consistency/consistency.html', context)

