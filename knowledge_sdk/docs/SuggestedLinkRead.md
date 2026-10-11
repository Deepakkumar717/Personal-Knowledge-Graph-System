# SuggestedLinkRead


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**target_id** | **int** |  | 
**target_title** | **str** |  | 
**similarity_score** | **float** |  | 
**shared_tags** | **List[str]** |  | [optional] [default to []]

## Example

```python
from knowledge_sdk.models.suggested_link_read import SuggestedLinkRead

# TODO update the JSON string below
json = "{}"
# create an instance of SuggestedLinkRead from a JSON string
suggested_link_read_instance = SuggestedLinkRead.from_json(json)
# print the JSON string representation of the object
print(SuggestedLinkRead.to_json())

# convert the object into a dict
suggested_link_read_dict = suggested_link_read_instance.to_dict()
# create an instance of SuggestedLinkRead from a dict
suggested_link_read_from_dict = SuggestedLinkRead.from_dict(suggested_link_read_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


