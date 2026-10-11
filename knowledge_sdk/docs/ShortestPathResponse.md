# ShortestPathResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_id** | **int** |  | 
**target_id** | **int** |  | 
**found** | **bool** |  | 
**path** | **List[int]** |  | [optional] [default to []]
**path_titles** | **List[str]** |  | [optional] [default to []]
**length** | **int** |  | [optional] [default to 0]

## Example

```python
from knowledge_sdk.models.shortest_path_response import ShortestPathResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ShortestPathResponse from a JSON string
shortest_path_response_instance = ShortestPathResponse.from_json(json)
# print the JSON string representation of the object
print(ShortestPathResponse.to_json())

# convert the object into a dict
shortest_path_response_dict = shortest_path_response_instance.to_dict()
# create an instance of ShortestPathResponse from a dict
shortest_path_response_from_dict = ShortestPathResponse.from_dict(shortest_path_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


