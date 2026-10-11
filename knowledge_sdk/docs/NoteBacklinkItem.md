# NoteBacklinkItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**origin** | **str** |  | 

## Example

```python
from knowledge_sdk.models.note_backlink_item import NoteBacklinkItem

# TODO update the JSON string below
json = "{}"
# create an instance of NoteBacklinkItem from a JSON string
note_backlink_item_instance = NoteBacklinkItem.from_json(json)
# print the JSON string representation of the object
print(NoteBacklinkItem.to_json())

# convert the object into a dict
note_backlink_item_dict = note_backlink_item_instance.to_dict()
# create an instance of NoteBacklinkItem from a dict
note_backlink_item_from_dict = NoteBacklinkItem.from_dict(note_backlink_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


