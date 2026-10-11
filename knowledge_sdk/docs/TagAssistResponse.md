# TagAssistResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**normalized** | **List[str]** |  | 
**suggestions** | [**List[TagSuggestionItem]**](TagSuggestionItem.md) |  | 
**merges** | [**List[PhraseMergeItem]**](PhraseMergeItem.md) |  | 
**corrections** | [**List[TagCorrectionItem]**](TagCorrectionItem.md) |  | 

## Example

```python
from knowledge_sdk.models.tag_assist_response import TagAssistResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TagAssistResponse from a JSON string
tag_assist_response_instance = TagAssistResponse.from_json(json)
# print the JSON string representation of the object
print(TagAssistResponse.to_json())

# convert the object into a dict
tag_assist_response_dict = tag_assist_response_instance.to_dict()
# create an instance of TagAssistResponse from a dict
tag_assist_response_from_dict = TagAssistResponse.from_dict(tag_assist_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


