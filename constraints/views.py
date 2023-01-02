from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from dicom_manager.RTDCM_manager import Manager
from dicompylercore import dicomparser, dvh, dvhcalc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io, base64

def constraints(request):
    context = {}
    is_RTDose = False
    is_RTStructure = False
    if request.method == 'POST':
        try:
            rtdose_file = Manager(request.FILES['rtdose_dcm'])
            rtstructure_file = Manager(request.FILES['rtdose_dcm'])
            if rtdose_file.modality == 'RTDOSE':
                is_RTDose = True
            if rtstructure_file.modality == 'RTSTRUCT':
                is_RTStructure = True
        except:
            messages.success(request, ('Por favor selecione um arquivo de dose válido.'))

        try:
            rtstructure_file = Manager(request.FILES['rtstructure_dcm'])
            if rtstructure_file.modality == 'RTSTRUCT':
                is_RTStructure = True
        except:
            messages.success(request, ('Por favor selecione um arquivo de estruturas válido.'))

        if is_RTStructure is True:
            dp = dicomparser.DicomParser(rtstructure_file.dcm_file)
            structures = dp.GetStructures()
            structures_list = []
            for st in structures:
                structures_list.append(structures[st])
            context['structures'] = structures_list
            '''for st in structures:
                print(structures[st])'''



        if is_RTDose is True:
            rtdoseDVH = dicomparser.DicomParser(rtdose_file.dcm_file)
            fig, ax = plt.subplots()
            error_list = []
            for st in structures_list:
                try:
                    roi = st['id']
                    ptvDVH = dvh.DVH.from_dicom_dvh(rtdoseDVH.ds, roi)
                    ax.plot(ptvDVH.bincenters, ptvDVH.counts, label=st['name'])
                except:
                    error_list.append(st)

            '''ptvDVH.describe()
            print(ptvDVH.D90)
            print(ptvDVH.D93)
            print(ptvDVH.D95)
            print(ptvDVH.V40Gy)
            print(f"{ptvDVH.V40Gy.value:.0f}%")
            print(f"{ptvDVH.V40Gy.value:.1f}%")
            print(f"{ptvDVH.V40Gy.value:.2f}%")
            print(f"{ptvDVH.V40Gy.value:.3f}%")
            print(f"{ptvDVH.V40Gy.value:.4f}%")
            print(f"{ptvDVH.V40Gy.value:.10f}%")

            print(ptvDVH.volume_constraint(40.05, dose_units="Gy").value)
            teste = ptvDVH.dose_constraint(87.35, volume_units="%").value
            print(f"{teste:.2f}%")'''          
            
            plt.xlabel('Dose [%s]' % ptvDVH.dose_units)
            plt.ylabel('Volume [%s]' % ptvDVH.volume_units)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
            fig.set_size_inches(10, 5)
            plt.tight_layout()
            #plt.show()

            '''The save and convert to base64 part follows: A new file like object is created using io.BytesIO() and the figure is saved there
            (fig.savefig(flike)). Then it is converted to a base64 string using the b64 = base64.b64encode(flike.getvalue()).decode().
            Finally it is just passed to the context of the template as chart.
            Fonte: https://spapas.github.io/2021/02/08/django-matplotlib/'''
            flike = io.BytesIO()
            fig.savefig(flike)
            b64 = base64.b64encode(flike.getvalue()).decode()
            context['chart'] = b64

    return render(request, 'constraints/constraints.html', context)