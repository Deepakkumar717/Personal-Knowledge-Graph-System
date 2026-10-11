# LinkDeleteResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_id** | **int** |  | 
**target_id** | **int** |  | 
**message** | **str** |  | 

## Example

```python
from knowledge_sdk.models.link_delete_response import LinkDeleteResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LinkDeleteResponse from a JSON string
link_delete_response_instance = LinkDeleteResponse.from_json(json)
# print the JSON string representation of the object
print(LinkDeleteResponse.to_json())

# convert the object into a dict
link_delete_response_dict = link_delete_response_instance.to_dict()
# create an instance of LinkDeleteResponse from a dict
link_delete_response_from_dict = LinkDeleteResponse.from_dict(link_delete_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


