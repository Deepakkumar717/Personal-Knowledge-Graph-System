# NotePatch


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**content** | **str** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**pinned** | **bool** |  | [optional] 

## Example

```python
from knowledge_sdk.models.note_patch import NotePatch

# TODO update the JSON string below
json = "{}"
# create an instance of NotePatch from a JSON string
note_patch_instance = NotePatch.from_json(json)
# print the JSON string representation of the object
print(NotePatch.to_json())

# convert the object into a dict
note_patch_dict = note_patch_instance.to_dict()
# create an instance of NotePatch from a dict
note_patch_from_dict = NotePatch.from_dict(note_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


