# TagSuggestionItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tag** | **str** |  | 
**reason** | **str** |  | 

## Example

```python
from knowledge_sdk.models.tag_suggestion_item import TagSuggestionItem

# TODO update the JSON string below
json = "{}"
# create an instance of TagSuggestionItem from a JSON string
tag_suggestion_item_instance = TagSuggestionItem.from_json(json)
# print the JSON string representation of the object
print(TagSuggestionItem.to_json())

# convert the object into a dict
tag_suggestion_item_dict = tag_suggestion_item_instance.to_dict()
# create an instance of TagSuggestionItem from a dict
tag_suggestion_item_from_dict = TagSuggestionItem.from_dict(tag_suggestion_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


