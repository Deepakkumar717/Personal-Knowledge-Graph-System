# TagSuggestResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query** | **str** |  | 
**suggestions** | [**List[TagSuggestion]**](TagSuggestion.md) |  | 

## Example

```python
from knowledge_sdk.models.tag_suggest_response import TagSuggestResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TagSuggestResponse from a JSON string
tag_suggest_response_instance = TagSuggestResponse.from_json(json)
# print the JSON string representation of the object
print(TagSuggestResponse.to_json())

# convert the object into a dict
tag_suggest_response_dict = tag_suggest_response_instance.to_dict()
# create an instance of TagSuggestResponse from a dict
tag_suggest_response_from_dict = TagSuggestResponse.from_dict(tag_suggest_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


