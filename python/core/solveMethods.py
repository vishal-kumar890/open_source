from .sqlConnector import celery_app
import oci
from datetime import datetime,timedelta
from ..config import settings


def solve(conn,filename,solver):
    print('data',filename,solver)
    user_id = 8
    result = celery_app.send_task("solve_task",
                                    args=[user_id,filename])

    delete_upload_request(filename)                        
    return {'msg':'Success'}

def get_upload_url(filename):
    current_datetime = datetime.utcnow()
    tomorrow_datetime = current_datetime + timedelta(days=1)
    config = oci.config.from_file()
    object_storage = oci.object_storage.ObjectStorageClient(config)
    bucket_name = settings.bucket_name
    namespace=settings.namespace_name
    par_details = oci.object_storage.models.CreatePreauthenticatedRequestDetails(
    
        name=f"upload_{filename}",
        object_name=filename,
        access_type=oci.object_storage.models.CreatePreauthenticatedRequestDetails.ACCESS_TYPE_OBJECT_WRITE,
        time_expires=tomorrow_datetime.strftime("%Y-%m-%dT00:00:00Z")
    )

    par_response = object_storage.create_preauthenticated_request(
        bucket_name=bucket_name,
        namespace_name=namespace,
        create_preauthenticated_request_details=par_details
    )

    return {'upload_url':par_response.data.full_path}

def delete_upload_request(filename):
    config = oci.config.from_file()
    object_storage = oci.object_storage.ObjectStorageClient(config)
    list_par_response = object_storage.list_preauthenticated_requests(settings.namespace_name,settings.bucket_name)

    par_id = None
    for par in list_par_response.data:
        id_name = str(par.id).split(":")
        
        if len(id_name)>1:
            if id_name[1] == filename:
                par_id = par.id

    if par_id:
        object_storage.delete_preauthenticated_request(
        bucket_name=settings.bucket_name,
        namespace_name=settings.namespace_name,
        par_id=par_id
)




