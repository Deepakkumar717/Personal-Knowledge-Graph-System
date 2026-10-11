# HubStat


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**link_count** | **int** |  | 

## Example

```python
from knowledge_sdk.models.hub_stat import HubStat

# TODO update the JSON string below
json = "{}"
# create an instance of HubStat from a JSON string
hub_stat_instance = HubStat.from_json(json)
# print the JSON string representation of the object
print(HubStat.to_json())

# convert the object into a dict
hub_stat_dict = hub_stat_instance.to_dict()
# create an instance of HubStat from a dict
hub_stat_from_dict = HubStat.from_dict(hub_stat_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


