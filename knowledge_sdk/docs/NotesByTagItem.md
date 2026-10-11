# NotesByTagItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tag** | **str** |  | 
**count** | **int** |  | 

## Example

```python
from knowledge_sdk.models.notes_by_tag_item import NotesByTagItem

# TODO update the JSON string below
json = "{}"
# create an instance of NotesByTagItem from a JSON string
notes_by_tag_item_instance = NotesByTagItem.from_json(json)
# print the JSON string representation of the object
print(NotesByTagItem.to_json())

# convert the object into a dict
notes_by_tag_item_dict = notes_by_tag_item_instance.to_dict()
# create an instance of NotesByTagItem from a dict
notes_by_tag_item_from_dict = NotesByTagItem.from_dict(notes_by_tag_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


