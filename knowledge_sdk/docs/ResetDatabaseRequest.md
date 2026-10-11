# ResetDatabaseRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**confirm** | **str** | Confirmation phrase; must be exactly &#39;DELETE ALL&#39; | 

## Example

```python
from knowledge_sdk.models.reset_database_request import ResetDatabaseRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ResetDatabaseRequest from a JSON string
reset_database_request_instance = ResetDatabaseRequest.from_json(json)
# print the JSON string representation of the object
print(ResetDatabaseRequest.to_json())

# convert the object into a dict
reset_database_request_dict = reset_database_request_instance.to_dict()
# create an instance of ResetDatabaseRequest from a dict
reset_database_request_from_dict = ResetDatabaseRequest.from_dict(reset_database_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


