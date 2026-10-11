# TopConnectedItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**degree** | **int** |  | 

## Example

```python
from knowledge_sdk.models.top_connected_item import TopConnectedItem

# TODO update the JSON string below
json = "{}"
# create an instance of TopConnectedItem from a JSON string
top_connected_item_instance = TopConnectedItem.from_json(json)
# print the JSON string representation of the object
print(TopConnectedItem.to_json())

# convert the object into a dict
top_connected_item_dict = top_connected_item_instance.to_dict()
# create an instance of TopConnectedItem from a dict
top_connected_item_from_dict = TopConnectedItem.from_dict(top_connected_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


