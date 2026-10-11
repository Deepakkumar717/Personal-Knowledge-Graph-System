# RelatedNoteItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**score** | **float** |  | 
**shared_tags** | **List[str]** |  | [optional] [default to []]

## Example

```python
from knowledge_sdk.models.related_note_item import RelatedNoteItem

# TODO update the JSON string below
json = "{}"
# create an instance of RelatedNoteItem from a JSON string
related_note_item_instance = RelatedNoteItem.from_json(json)
# print the JSON string representation of the object
print(RelatedNoteItem.to_json())

# convert the object into a dict
related_note_item_dict = related_note_item_instance.to_dict()
# create an instance of RelatedNoteItem from a dict
related_note_item_from_dict = RelatedNoteItem.from_dict(related_note_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


