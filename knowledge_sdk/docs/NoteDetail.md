# NoteDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**content** | **str** |  | 
**tags** | **List[str]** |  | 
**pinned** | **bool** |  | 
**created_at** | **str** |  | [optional] 
**updated_at** | **str** |  | [optional] 
**outgoing_links** | [**List[LinkRead]**](LinkRead.md) |  | 
**backlinks** | [**List[NoteBacklinkItem]**](NoteBacklinkItem.md) |  | 
**unresolved_links** | **List[str]** |  | 
**related_notes** | [**List[RelatedNoteItem]**](RelatedNoteItem.md) |  | 

## Example

```python
from knowledge_sdk.models.note_detail import NoteDetail

# TODO update the JSON string below
json = "{}"
# create an instance of NoteDetail from a JSON string
note_detail_instance = NoteDetail.from_json(json)
# print the JSON string representation of the object
print(NoteDetail.to_json())

# convert the object into a dict
note_detail_dict = note_detail_instance.to_dict()
# create an instance of NoteDetail from a dict
note_detail_from_dict = NoteDetail.from_dict(note_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


