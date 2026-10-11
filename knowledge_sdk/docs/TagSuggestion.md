# TagSuggestion


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**count** | **int** |  | 
**score** | **float** |  | 

## Example

```python
from knowledge_sdk.models.tag_suggestion import TagSuggestion

# TODO update the JSON string below
json = "{}"
# create an instance of TagSuggestion from a JSON string
tag_suggestion_instance = TagSuggestion.from_json(json)
# print the JSON string representation of the object
print(TagSuggestion.to_json())

# convert the object into a dict
tag_suggestion_dict = tag_suggestion_instance.to_dict()
# create an instance of TagSuggestion from a dict
tag_suggestion_from_dict = TagSuggestion.from_dict(tag_suggestion_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


