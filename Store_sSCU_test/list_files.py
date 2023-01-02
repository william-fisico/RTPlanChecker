import os
from pydicom import dcmread


root = './'
patient_dict = {} # patient_dict = {pacs:plan_list}

for entry in os.listdir(root):

    if os.path.isdir(entry) and entry.startswith("PACS_"):
        os.chdir(entry)
        plan_list = []
        #id_list.append(entry.replace("PACS_", ""))
        for file in os.listdir('.'):
            if file.startswith('RTPLAN') and file.endswith('.dcm'):
                temp_dcm = dcmread(file, force=True)
                file_name = temp_dcm[0x300A,0x0003].value
                plan_list.append((file_name,file))
        patient_dict[entry.replace("PACS_", "")] = plan_list
        os.chdir('..')

print(patient_dict)