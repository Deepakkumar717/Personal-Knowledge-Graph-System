# LinkRead


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_id** | **int** |  | 
**target_id** | **int** |  | 
**origin** | **str** |  | 
**source_title** | **str** |  | [optional] 
**target_title** | **str** |  | [optional] 

## Example

```python
from knowledge_sdk.models.link_read import LinkRead

# TODO update the JSON string below
json = "{}"
# create an instance of LinkRead from a JSON string
link_read_instance = LinkRead.from_json(json)
# print the JSON string representation of the object
print(LinkRead.to_json())

# convert the object into a dict
link_read_dict = link_read_instance.to_dict()
# create an instance of LinkRead from a dict
link_read_from_dict = LinkRead.from_dict(link_read_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


