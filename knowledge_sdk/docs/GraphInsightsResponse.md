# GraphInsightsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**notes_by_tag** | [**List[NotesByTagItem]**](NotesByTagItem.md) |  | 
**notes_by_group** | [**List[NotesByGroupItem]**](NotesByGroupItem.md) |  | 
**notes_per_day** | [**List[NotesPerDayItem]**](NotesPerDayItem.md) |  | 
**top_connected** | [**List[TopConnectedItem]**](TopConnectedItem.md) |  | 
**connected_vs_orphans** | [**ConnectedVsOrphans**](ConnectedVsOrphans.md) |  | 
**link_types** | [**LinkTypes**](LinkTypes.md) |  | 

## Example

```python
from knowledge_sdk.models.graph_insights_response import GraphInsightsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GraphInsightsResponse from a JSON string
graph_insights_response_instance = GraphInsightsResponse.from_json(json)
# print the JSON string representation of the object
print(GraphInsightsResponse.to_json())

# convert the object into a dict
graph_insights_response_dict = graph_insights_response_instance.to_dict()
# create an instance of GraphInsightsResponse from a dict
graph_insights_response_from_dict = GraphInsightsResponse.from_dict(graph_insights_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


