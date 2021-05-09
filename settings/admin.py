from django.contrib import admin
from .models import CTSettings
from .models import QAPlanarDose
from .models import QAPointDose
from .models import QACalcCheck
from .models import TreatmentMachine
from .models import RT_Techniques

admin.site.register(CTSettings)
admin.site.register(QAPlanarDose)
admin.site.register(QAPointDose)
admin.site.register(QACalcCheck)
admin.site.register(TreatmentMachine)
admin.site.register(RT_Techniques)
