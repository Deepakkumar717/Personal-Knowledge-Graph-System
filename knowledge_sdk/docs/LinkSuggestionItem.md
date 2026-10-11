# LinkSuggestionItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**note_id** | **int** |  | 
**title** | **str** |  | 
**score** | **float** |  | 
**reasons** | **List[str]** |  | 

## Example

```python
from knowledge_sdk.models.link_suggestion_item import LinkSuggestionItem

# TODO update the JSON string below
json = "{}"
# create an instance of LinkSuggestionItem from a JSON string
link_suggestion_item_instance = LinkSuggestionItem.from_json(json)
# print the JSON string representation of the object
print(LinkSuggestionItem.to_json())

# convert the object into a dict
link_suggestion_item_dict = link_suggestion_item_instance.to_dict()
# create an instance of LinkSuggestionItem from a dict
link_suggestion_item_from_dict = LinkSuggestionItem.from_dict(link_suggestion_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


