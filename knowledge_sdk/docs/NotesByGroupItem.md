# NotesByGroupItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**group** | **str** |  | 
**count** | **int** |  | 

## Example

```python
from knowledge_sdk.models.notes_by_group_item import NotesByGroupItem

# TODO update the JSON string below
json = "{}"
# create an instance of NotesByGroupItem from a JSON string
notes_by_group_item_instance = NotesByGroupItem.from_json(json)
# print the JSON string representation of the object
print(NotesByGroupItem.to_json())

# convert the object into a dict
notes_by_group_item_dict = notes_by_group_item_instance.to_dict()
# create an instance of NotesByGroupItem from a dict
notes_by_group_item_from_dict = NotesByGroupItem.from_dict(notes_by_group_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


