# GroupCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Group name (1-60 characters) | 
**color** | **str** | Hex color string, e.g. #8B5CF6 | 
**kind** | **str** | &#39;manual&#39; or &#39;auto&#39; | [optional] [default to 'manual']

## Example

```python
from knowledge_sdk.models.group_create import GroupCreate

# TODO update the JSON string below
json = "{}"
# create an instance of GroupCreate from a JSON string
group_create_instance = GroupCreate.from_json(json)
# print the JSON string representation of the object
print(GroupCreate.to_json())

# convert the object into a dict
group_create_dict = group_create_instance.to_dict()
# create an instance of GroupCreate from a dict
group_create_from_dict = GroupCreate.from_dict(group_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


