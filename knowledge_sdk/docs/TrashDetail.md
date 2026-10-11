# TrashDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**original_note_id** | **int** |  | 
**title** | **str** |  | 
**deleted_at** | **str** |  | 
**payload** | **Dict[str, object]** |  | 

## Example

```python
from knowledge_sdk.models.trash_detail import TrashDetail

# TODO update the JSON string below
json = "{}"
# create an instance of TrashDetail from a JSON string
trash_detail_instance = TrashDetail.from_json(json)
# print the JSON string representation of the object
print(TrashDetail.to_json())

# convert the object into a dict
trash_detail_dict = trash_detail_instance.to_dict()
# create an instance of TrashDetail from a dict
trash_detail_from_dict = TrashDetail.from_dict(trash_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


