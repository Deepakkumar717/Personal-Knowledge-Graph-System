# GroupAddNotesRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**note_ids** | **List[int]** | List of note IDs to add or move into group | 

## Example

```python
from knowledge_sdk.models.group_add_notes_request import GroupAddNotesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GroupAddNotesRequest from a JSON string
group_add_notes_request_instance = GroupAddNotesRequest.from_json(json)
# print the JSON string representation of the object
print(GroupAddNotesRequest.to_json())

# convert the object into a dict
group_add_notes_request_dict = group_add_notes_request_instance.to_dict()
# create an instance of GroupAddNotesRequest from a dict
group_add_notes_request_from_dict = GroupAddNotesRequest.from_dict(group_add_notes_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


