# GraphStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_notes** | **int** |  | 
**total_links** | **int** |  | 
**total_tags** | **int** |  | 
**orphan_count** | **int** |  | 
**orphans** | **List[str]** |  | 
**hubs** | [**List[HubStat]**](HubStat.md) |  | 
**tag_distribution** | [**List[TagDistributionStat]**](TagDistributionStat.md) |  | 

## Example

```python
from knowledge_sdk.models.graph_stats import GraphStats

# TODO update the JSON string below
json = "{}"
# create an instance of GraphStats from a JSON string
graph_stats_instance = GraphStats.from_json(json)
# print the JSON string representation of the object
print(GraphStats.to_json())

# convert the object into a dict
graph_stats_dict = graph_stats_instance.to_dict()
# create an instance of GraphStats from a dict
graph_stats_from_dict = GraphStats.from_dict(graph_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


