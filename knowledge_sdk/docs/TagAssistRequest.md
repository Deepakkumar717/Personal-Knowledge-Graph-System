# TagAssistRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**content** | **str** |  | [optional] 
**tags** | **List[str]** |  | [optional] 

## Example

```python
from knowledge_sdk.models.tag_assist_request import TagAssistRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TagAssistRequest from a JSON string
tag_assist_request_instance = TagAssistRequest.from_json(json)
# print the JSON string representation of the object
print(TagAssistRequest.to_json())

# convert the object into a dict
tag_assist_request_dict = tag_assist_request_instance.to_dict()
# create an instance of TagAssistRequest from a dict
tag_assist_request_from_dict = TagAssistRequest.from_dict(tag_assist_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


