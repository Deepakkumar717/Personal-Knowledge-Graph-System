# TitleSuggestItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 

## Example

```python
from knowledge_sdk.models.title_suggest_item import TitleSuggestItem

# TODO update the JSON string below
json = "{}"
# create an instance of TitleSuggestItem from a JSON string
title_suggest_item_instance = TitleSuggestItem.from_json(json)
# print the JSON string representation of the object
print(TitleSuggestItem.to_json())

# convert the object into a dict
title_suggest_item_dict = title_suggest_item_instance.to_dict()
# create an instance of TitleSuggestItem from a dict
title_suggest_item_from_dict = TitleSuggestItem.from_dict(title_suggest_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


