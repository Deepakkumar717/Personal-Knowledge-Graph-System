# DismissSuggestionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**note_id** | **int** |  | 
**other_id** | **int** |  | 

## Example

```python
from knowledge_sdk.models.dismiss_suggestion_request import DismissSuggestionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DismissSuggestionRequest from a JSON string
dismiss_suggestion_request_instance = DismissSuggestionRequest.from_json(json)
# print the JSON string representation of the object
print(DismissSuggestionRequest.to_json())

# convert the object into a dict
dismiss_suggestion_request_dict = dismiss_suggestion_request_instance.to_dict()
# create an instance of DismissSuggestionRequest from a dict
dismiss_suggestion_request_from_dict = DismissSuggestionRequest.from_dict(dismiss_suggestion_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


