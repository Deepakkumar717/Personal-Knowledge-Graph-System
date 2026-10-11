# GroupRead


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**color** | **str** |  | 
**kind** | **str** |  | 
**note_count** | **int** |  | [optional] [default to 0]
**created_at** | **str** |  | 
**updated_at** | **str** |  | 

## Example

```python
from knowledge_sdk.models.group_read import GroupRead

# TODO update the JSON string below
json = "{}"
# create an instance of GroupRead from a JSON string
group_read_instance = GroupRead.from_json(json)
# print the JSON string representation of the object
print(GroupRead.to_json())

# convert the object into a dict
group_read_dict = group_read_instance.to_dict()
# create an instance of GroupRead from a dict
group_read_from_dict = GroupRead.from_dict(group_read_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


