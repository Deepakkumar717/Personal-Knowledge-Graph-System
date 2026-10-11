# DismissSuggestionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | 
**message** | **str** |  | 

## Example

```python
from knowledge_sdk.models.dismiss_suggestion_response import DismissSuggestionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DismissSuggestionResponse from a JSON string
dismiss_suggestion_response_instance = DismissSuggestionResponse.from_json(json)
# print the JSON string representation of the object
print(DismissSuggestionResponse.to_json())

# convert the object into a dict
dismiss_suggestion_response_dict = dismiss_suggestion_response_instance.to_dict()
# create an instance of DismissSuggestionResponse from a dict
dismiss_suggestion_response_from_dict = DismissSuggestionResponse.from_dict(dismiss_suggestion_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


