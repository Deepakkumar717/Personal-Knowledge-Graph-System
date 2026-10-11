# NoteUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Unique title of the note | 
**content** | **str** | Markdown content of the note | [optional] 
**tags** | **List[str]** | List of tags for the note | [optional] 

## Example

```python
from knowledge_sdk.models.note_update import NoteUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of NoteUpdate from a JSON string
note_update_instance = NoteUpdate.from_json(json)
# print the JSON string representation of the object
print(NoteUpdate.to_json())

# convert the object into a dict
note_update_dict = note_update_instance.to_dict()
# create an instance of NoteUpdate from a dict
note_update_from_dict = NoteUpdate.from_dict(note_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


