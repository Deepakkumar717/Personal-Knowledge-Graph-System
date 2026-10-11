# GroupMergeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**into_id** | **int** | Target group ID to merge into | 

## Example

```python
from knowledge_sdk.models.group_merge_request import GroupMergeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GroupMergeRequest from a JSON string
group_merge_request_instance = GroupMergeRequest.from_json(json)
# print the JSON string representation of the object
print(GroupMergeRequest.to_json())

# convert the object into a dict
group_merge_request_dict = group_merge_request_instance.to_dict()
# create an instance of GroupMergeRequest from a dict
group_merge_request_from_dict = GroupMergeRequest.from_dict(group_merge_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


