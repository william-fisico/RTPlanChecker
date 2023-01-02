from django.db import models

# Create your models here.

# Configurações CT
class CTSettings(models.Model):
    ctsettings_name = models.CharField('Nome da Configuração CT', max_length=50)
    ct_thickness = models.FloatField('Espessura do corte (mm)')
    ct_fov = models.CharField('FOV', max_length=50, blank=True)

    def __str__(self):
        return self.ctsettings_name


# Forma de QA para verificação de dose planar (filme, matrixx, portal dosimetry...)
class QAPlanarDose(models.Model):
    planar_name = models.CharField('Nome', max_length=50)
    planar_manufacturer = models.CharField('Fabricante', max_length = 100, blank=True)
    planar_resolution = models.CharField('Resolução', max_length=30, blank=True)

    def __str__(self):
        return self.planar_name


# Forma de QA para verificação de dose pontual (farmer, cc13, cc04, diodo..)
class QAPointDose(models.Model):
    point_name = models.CharField('Nome', max_length=50)
    point_manufacturer = models.CharField('Fabricante', max_length = 100, blank=True)
    point_volume = models.CharField('Volume Sensível', max_length=30, blank=True)

    def __str__(self):
        return self.point_name


# Forma de conferência do cálculo (RadCalc, Diamond...)
class QACalcCheck(models.Model):
    calc_check_name = models.CharField('Nome', max_length=50)
    calc_check_manufacturer = models.CharField('Fabricante', max_length = 100, blank=True)

    def __str__(self):
        return self.calc_check_name


# Linac's
class TreatmentMachine(models.Model):
    linac_name = models.CharField('Nome', max_length=50)
    linac_model = models.CharField('Modelo', max_length = 100, blank=True)
    linac_manufacturer = models.CharField('Fabricante', max_length = 100, blank=True)

    def __str__(self):
        return self.linac_name




# RT_Techniques armazena as tecnicas de tratamento que podem ser utilizadas
class RT_Techniques(models.Model):
    name = models.CharField(max_length=120) # nome da tecnica
    ct_settings = models.ForeignKey(CTSettings, null=True, on_delete=models.SET_NULL) # Configuracoes CT
    calc_grid = models.FloatField() # grade de calculo
    qa_planar_dose = models.ManyToManyField(QAPlanarDose, blank=True) # Forma de QA para verificacao de dose planar (filme, matrixx, portal dosimetry...)
    qa_point_dose = models.ManyToManyField(QAPointDose, blank=True) # Forma de QA para verificacao de dose pontual (farmer, cc13, cc04, diodo..)
    qa_calc_check = models.ManyToManyField(QACalcCheck, blank=True) # Forma de conferencia do calculo (RadCalc, Diamond...)
    treatment_machine =models.ManyToManyField(TreatmentMachine, blank=True)


    def __str__(self):
        return self.name