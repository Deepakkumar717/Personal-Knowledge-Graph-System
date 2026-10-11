# AssistStatusResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** |  | 
**provider** | **str** |  | 
**model** | **str** |  | [optional] 

## Example

```python
from knowledge_sdk.models.assist_status_response import AssistStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AssistStatusResponse from a JSON string
assist_status_response_instance = AssistStatusResponse.from_json(json)
# print the JSON string representation of the object
print(AssistStatusResponse.to_json())

# convert the object into a dict
assist_status_response_dict = assist_status_response_instance.to_dict()
# create an instance of AssistStatusResponse from a dict
assist_status_response_from_dict = AssistStatusResponse.from_dict(assist_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


