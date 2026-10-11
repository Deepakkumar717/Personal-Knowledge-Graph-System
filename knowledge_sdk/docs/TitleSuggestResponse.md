# TitleSuggestResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query** | **str** |  | 
**results** | [**List[TitleSuggestItem]**](TitleSuggestItem.md) |  | 

## Example

```python
from knowledge_sdk.models.title_suggest_response import TitleSuggestResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TitleSuggestResponse from a JSON string
title_suggest_response_instance = TitleSuggestResponse.from_json(json)
# print the JSON string representation of the object
print(TitleSuggestResponse.to_json())

# convert the object into a dict
title_suggest_response_dict = title_suggest_response_instance.to_dict()
# create an instance of TitleSuggestResponse from a dict
title_suggest_response_from_dict = TitleSuggestResponse.from_dict(title_suggest_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


