# UnlinkedMentionItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**note_id** | **int** |  | 
**note_title** | **str** |  | 
**snippet** | **str** |  | 

## Example

```python
from knowledge_sdk.models.unlinked_mention_item import UnlinkedMentionItem

# TODO update the JSON string below
json = "{}"
# create an instance of UnlinkedMentionItem from a JSON string
unlinked_mention_item_instance = UnlinkedMentionItem.from_json(json)
# print the JSON string representation of the object
print(UnlinkedMentionItem.to_json())

# convert the object into a dict
unlinked_mention_item_dict = unlinked_mention_item_instance.to_dict()
# create an instance of UnlinkedMentionItem from a dict
unlinked_mention_item_from_dict = UnlinkedMentionItem.from_dict(unlinked_mention_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


