import os, datetime
from pathlib import Path

from pynetdicom import AE, evt, AllStoragePresentationContexts, debug_logger

server_ip = "10.65.237.159"
server_port = 11112
debug_logger()

# Implement a handler for evt.EVT_C_STORE
def handle_store(event):
    """Handle a C-STORE request event."""
    # Decode the C-STORE request's *Data Set* parameter to a pydicom Dataset
    ds = event.dataset

    # Add the File Meta Information
    ds.file_meta = event.file_meta

    # Nome do diretório será o PACS do paciente
    #directory_name = "PACS_" + ds.PatientID
    directory_name = ds.PatientID

    # Cria um diretório com o PACS do paciente
    Path(directory_name).mkdir(parents=True, exist_ok=True)

    # Verifica se o diretório com o PACS do paciente existe
    if(os.path.isdir(directory_name)):

        os.chdir(directory_name)

        # Save the dataset using the SOP Instance UID as the filename
        ds.save_as(ds.Modality + "." + ds.PatientID + "." + ds.SOPInstanceUID + ".dcm", write_like_original=False)

        os.chdir("..")

    # Return a 'Success' status
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]

# Initialise the Application Entity
ae = AE()

# Support presentation contexts for all storage SOP Classes
ae.supported_contexts = AllStoragePresentationContexts

print("Starting DICOM Server ...")
print("Listening to " + server_ip + ":" + str(server_port))

# Start listening for incoming association requests
ae.start_server((server_ip, server_port), evt_handlers=handlers, block=True)

