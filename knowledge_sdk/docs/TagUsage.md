# TagUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**count** | **int** |  | 

## Example

```python
from knowledge_sdk.models.tag_usage import TagUsage

# TODO update the JSON string below
json = "{}"
# create an instance of TagUsage from a JSON string
tag_usage_instance = TagUsage.from_json(json)
# print the JSON string representation of the object
print(TagUsage.to_json())

# convert the object into a dict
tag_usage_dict = tag_usage_instance.to_dict()
# create an instance of TagUsage from a dict
tag_usage_from_dict = TagUsage.from_dict(tag_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


