# TrashItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**original_note_id** | **int** |  | 
**title** | **str** |  | 
**deleted_at** | **str** |  | 

## Example

```python
from knowledge_sdk.models.trash_item import TrashItem

# TODO update the JSON string below
json = "{}"
# create an instance of TrashItem from a JSON string
trash_item_instance = TrashItem.from_json(json)
# print the JSON string representation of the object
print(TrashItem.to_json())

# convert the object into a dict
trash_item_dict = trash_item_instance.to_dict()
# create an instance of TrashItem from a dict
trash_item_from_dict = TrashItem.from_dict(trash_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


