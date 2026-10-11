# GroupSuggestionsApplyRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**groups** | [**List[GroupSuggestionItem]**](GroupSuggestionItem.md) |  | 

## Example

```python
from knowledge_sdk.models.group_suggestions_apply_request import GroupSuggestionsApplyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GroupSuggestionsApplyRequest from a JSON string
group_suggestions_apply_request_instance = GroupSuggestionsApplyRequest.from_json(json)
# print the JSON string representation of the object
print(GroupSuggestionsApplyRequest.to_json())

# convert the object into a dict
group_suggestions_apply_request_dict = group_suggestions_apply_request_instance.to_dict()
# create an instance of GroupSuggestionsApplyRequest from a dict
group_suggestions_apply_request_from_dict = GroupSuggestionsApplyRequest.from_dict(group_suggestions_apply_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


