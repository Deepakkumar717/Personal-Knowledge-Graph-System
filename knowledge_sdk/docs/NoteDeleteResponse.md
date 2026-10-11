# NoteDeleteResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**message** | **str** |  | 

## Example

```python
from knowledge_sdk.models.note_delete_response import NoteDeleteResponse

# TODO update the JSON string below
json = "{}"
# create an instance of NoteDeleteResponse from a JSON string
note_delete_response_instance = NoteDeleteResponse.from_json(json)
# print the JSON string representation of the object
print(NoteDeleteResponse.to_json())

# convert the object into a dict
note_delete_response_dict = note_delete_response_instance.to_dict()
# create an instance of NoteDeleteResponse from a dict
note_delete_response_from_dict = NoteDeleteResponse.from_dict(note_delete_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


