# GroupSuggestionsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**suggestions** | [**List[GroupSuggestionItem]**](GroupSuggestionItem.md) |  | 

## Example

```python
from knowledge_sdk.models.group_suggestions_response import GroupSuggestionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GroupSuggestionsResponse from a JSON string
group_suggestions_response_instance = GroupSuggestionsResponse.from_json(json)
# print the JSON string representation of the object
print(GroupSuggestionsResponse.to_json())

# convert the object into a dict
group_suggestions_response_dict = group_suggestions_response_instance.to_dict()
# create an instance of GroupSuggestionsResponse from a dict
group_suggestions_response_from_dict = GroupSuggestionsResponse.from_dict(group_suggestions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


