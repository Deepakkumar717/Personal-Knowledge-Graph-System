# GraphResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**nodes** | [**List[GraphNode]**](GraphNode.md) |  | 
**edges** | [**List[GraphEdge]**](GraphEdge.md) |  | 
**adjacency_list** | **Dict[str, List[str]]** |  | 
**outgoing_ids** | **List[str]** |  | [optional] [default to []]
**backlink_ids** | **List[str]** |  | [optional] [default to []]
**mutual_ids** | **List[str]** |  | [optional] [default to []]

## Example

```python
from knowledge_sdk.models.graph_response import GraphResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GraphResponse from a JSON string
graph_response_instance = GraphResponse.from_json(json)
# print the JSON string representation of the object
print(GraphResponse.to_json())

# convert the object into a dict
graph_response_dict = graph_response_instance.to_dict()
# create an instance of GraphResponse from a dict
graph_response_from_dict = GraphResponse.from_dict(graph_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


