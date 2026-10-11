# GroupUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**color** | **str** |  | [optional] 

## Example

```python
from knowledge_sdk.models.group_update import GroupUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of GroupUpdate from a JSON string
group_update_instance = GroupUpdate.from_json(json)
# print the JSON string representation of the object
print(GroupUpdate.to_json())

# convert the object into a dict
group_update_dict = group_update_instance.to_dict()
# create an instance of GroupUpdate from a dict
group_update_from_dict = GroupUpdate.from_dict(group_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


