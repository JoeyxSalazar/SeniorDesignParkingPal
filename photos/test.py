import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from firebase_admin import storage
import os
import matplotlib.pyplot as plt

#Initialize Back End
cred = credentials.Certificate('parkingpal_admin.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': ''
})
os.chdir('C:/Users/Joey/OneDrive - University of Miami/Seventh Semester/Senior Design/SeniorDesignParkingPal/photos')
bucket = storage.bucket()
blob = bucket.blob('1.png')
print('Attempting photo upload')
blob.upload_from_filename('C:/Users/Joey/OneDrive - University of Miami/Seventh Semester/Senior Design/SeniorDesignParkingPal/photos/1.png')


"""Error:
Attempting photo upload
Traceback (most recent call last):
  File "C:\Users\Joey\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\google\cloud\storage\blob.py", line 2540, in upload_from_file
    created_json = self._do_upload(
                   ^^^^^^^^^^^^^^^^
  File "C:\Users\Joey\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\google\cloud\storage\blob.py", line 2355, in _do_upload
    response = self._do_multipart_upload(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Joey\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\google\cloud\storage\blob.py", line 1890, in _do_multipart_upload
    response = upload.transmit(
               ^^^^^^^^^^^^^^^^
  File "C:\Users\Joey\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\google\resumable_media\requests\upload.py", line 153, in transmit
    return _request_helpers.wait_and_retry(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Joey\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\google\resumable_media\reqpy", line 2684, in upload_from_filename
    self.upload_from_file(
  File "C:\Users\Joey\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\google\cloud\storage\blob.py", line 2557, in upload_from_file    _raise_from_invalid_response(exc)
  File "C:\Users\Joey\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\google\cloud\storage\blob.py", line 4369, in _raise_from_invalid_response    raise exceptions.from_http_status(response.status_code, message, response=response)
google.api_core.exceptions.NotFound: 404 POST https://storage.googleapis.com/upload/storage/v1/b/parking-pal-bdde9.appspot.com/Grey_Lot/o?uploadType=multipart: Not Found: ('Request failed with status code', 404, 'Expected one of', <HTTPStatus.OK: 200>)

"""