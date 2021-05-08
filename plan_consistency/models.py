from django.db import models

# RT_Techniques armazena as tecnicas de tratamento que podem ser utilizadas
class RT_Techniques(models.Model):
    name = models.CharField(max_length=120) # nome da tecnica
    ct_thickness = models.FloatField() # espessura de corte da tomo
    calc_grid = models.FloatField() # grade de calculo
    qa_planar_dose = models.CharField(max_length=50) # Forma de QA para verificação de dose planar (filme, matrixx, portal dosimetry...)
    qa_point_dose = models.CharField(max_length=50) # Forma de QA para verificação de dose pontual (farmer, cc13, cc04, diodo..)
    qa_calc_check = models.CharField(max_length=50) # Forma de conferência do cálculo (RadCalc, Diamond...)


    def __str__(self):
        return self.name