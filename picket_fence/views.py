from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import pydicom

def create_image():
    img_path = './Test_Images/Y2_pfDicom.dcm'
    ds = pydicom.filereader.read_file(img_path)
    image_array = ds.pixel_array

    sad = ds[0x3002, 0x0022].value
    sid = ds[0x3002,0x0026].value
    x_res = (ds[0x3002,0x0011].value[0])*(sad/sid)
    y_res = (ds[0x3002,0x0011].value[1])*(sad/sid)

    dx = 0
    dy = 0

    x_axis = [(x*x_res/10)-dx for x in range(np.shape(image_array)[0])]
    y_axis = [(y*y_res/10)-dy for y in range(np.shape(image_array)[1])]

    #fig = go.Figure()

    fig = px.imshow(image_array, x=x_axis, y=y_axis, origin='lower')

    '''fig.add_trace(
            go.Heatmap(z=image_array, x=x_axis, y=y_axis, visible=True)
        )'''

    fig.update_layout(coloraxis_showscale=False)

    graph = fig.to_html(full_html=False, default_height=500, default_width=700)

    return graph

# Create your views here.

# Create your views here.
#@login_required
@permission_required('admin.can_add_log_entry',login_url="/login_permission_error/")
def picket_fence(request):
    context = {'img':create_image}
    if request.method == 'POST':
        mlc_model = data.get("mlc")
        print(mlc_model)

    return render(request, 'picket_fence/picketfence.html', context)