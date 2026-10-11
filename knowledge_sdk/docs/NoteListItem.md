# NoteListItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**content_snippet** | **str** |  | 
**tags** | **List[str]** |  | 
**outgoing_link_count** | **int** |  | 
**backlink_count** | **int** |  | 
**pinned** | **bool** |  | 
**created_at** | **str** |  | [optional] 
**updated_at** | **str** |  | [optional] 

## Example

```python
from knowledge_sdk.models.note_list_item import NoteListItem

# TODO update the JSON string below
json = "{}"
# create an instance of NoteListItem from a JSON string
note_list_item_instance = NoteListItem.from_json(json)
# print the JSON string representation of the object
print(NoteListItem.to_json())

# convert the object into a dict
note_list_item_dict = note_list_item_instance.to_dict()
# create an instance of NoteListItem from a dict
note_list_item_from_dict = NoteListItem.from_dict(note_list_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


