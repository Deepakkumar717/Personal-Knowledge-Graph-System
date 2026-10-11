# LinkCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**target_id** | **int** | Target note ID to link to | 

## Example

```python
from knowledge_sdk.models.link_create import LinkCreate

# TODO update the JSON string below
json = "{}"
# create an instance of LinkCreate from a JSON string
link_create_instance = LinkCreate.from_json(json)
# print the JSON string representation of the object
print(LinkCreate.to_json())

# convert the object into a dict
link_create_dict = link_create_instance.to_dict()
# create an instance of LinkCreate from a dict
link_create_from_dict = LinkCreate.from_dict(link_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


