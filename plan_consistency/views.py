from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Create your views here.

def rtplan_consistency(request):
    context = {}
    if request.method == 'POST':
        upload_dcm = request.FILES['document']
        fs = FileSystemStorage()
        file_name = fs.save(upload_dcm.name, upload_dcm)
        context['file_url'] = fs.url(file_name)
    return render(request, 'plan_consistency/consistency.html', context)
