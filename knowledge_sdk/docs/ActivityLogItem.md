# ActivityLogItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**ts** | **str** |  | 
**action** | **str** |  | 
**entity** | **str** |  | 
**entity_id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**detail** | **str** |  | [optional] 

## Example

```python
from knowledge_sdk.models.activity_log_item import ActivityLogItem

# TODO update the JSON string below
json = "{}"
# create an instance of ActivityLogItem from a JSON string
activity_log_item_instance = ActivityLogItem.from_json(json)
# print the JSON string representation of the object
print(ActivityLogItem.to_json())

# convert the object into a dict
activity_log_item_dict = activity_log_item_instance.to_dict()
# create an instance of ActivityLogItem from a dict
activity_log_item_from_dict = ActivityLogItem.from_dict(activity_log_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


