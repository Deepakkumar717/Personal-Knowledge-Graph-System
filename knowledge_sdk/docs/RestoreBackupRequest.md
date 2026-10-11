# RestoreBackupRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filename** | **str** |  | 
**confirm** | **str** | Confirmation phrase; must be exactly &#39;RESTORE&#39; | 

## Example

```python
from knowledge_sdk.models.restore_backup_request import RestoreBackupRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RestoreBackupRequest from a JSON string
restore_backup_request_instance = RestoreBackupRequest.from_json(json)
# print the JSON string representation of the object
print(RestoreBackupRequest.to_json())

# convert the object into a dict
restore_backup_request_dict = restore_backup_request_instance.to_dict()
# create an instance of RestoreBackupRequest from a dict
restore_backup_request_from_dict = RestoreBackupRequest.from_dict(restore_backup_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


