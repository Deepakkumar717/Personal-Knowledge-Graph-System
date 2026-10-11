# GroupSuggestForNoteResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**group_id** | **int** |  | [optional] 
**group_name** | **str** |  | [optional] 
**group_color** | **str** |  | [optional] 
**reason** | **str** |  | [optional] 
**score** | **float** |  | [optional] [default to 0.0]

## Example

```python
from knowledge_sdk.models.group_suggest_for_note_response import GroupSuggestForNoteResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GroupSuggestForNoteResponse from a JSON string
group_suggest_for_note_response_instance = GroupSuggestForNoteResponse.from_json(json)
# print the JSON string representation of the object
print(GroupSuggestForNoteResponse.to_json())

# convert the object into a dict
group_suggest_for_note_response_dict = group_suggest_for_note_response_instance.to_dict()
# create an instance of GroupSuggestForNoteResponse from a dict
group_suggest_for_note_response_from_dict = GroupSuggestForNoteResponse.from_dict(group_suggest_for_note_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


