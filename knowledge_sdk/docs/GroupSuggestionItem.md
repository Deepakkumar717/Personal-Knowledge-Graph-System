# GroupSuggestionItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**color** | **str** |  | 
**note_ids** | **List[int]** |  | 
**reasons** | **List[str]** |  | 
**cohesion** | **float** |  | 

## Example

```python
from knowledge_sdk.models.group_suggestion_item import GroupSuggestionItem

# TODO update the JSON string below
json = "{}"
# create an instance of GroupSuggestionItem from a JSON string
group_suggestion_item_instance = GroupSuggestionItem.from_json(json)
# print the JSON string representation of the object
print(GroupSuggestionItem.to_json())

# convert the object into a dict
group_suggestion_item_dict = group_suggestion_item_instance.to_dict()
# create an instance of GroupSuggestionItem from a dict
group_suggestion_item_from_dict = GroupSuggestionItem.from_dict(group_suggestion_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


