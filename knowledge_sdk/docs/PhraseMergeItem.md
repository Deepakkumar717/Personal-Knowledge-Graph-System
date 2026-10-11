# PhraseMergeItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_from** | **List[str]** |  | 
**to** | **str** |  | 

## Example

```python
from knowledge_sdk.models.phrase_merge_item import PhraseMergeItem

# TODO update the JSON string below
json = "{}"
# create an instance of PhraseMergeItem from a JSON string
phrase_merge_item_instance = PhraseMergeItem.from_json(json)
# print the JSON string representation of the object
print(PhraseMergeItem.to_json())

# convert the object into a dict
phrase_merge_item_dict = phrase_merge_item_instance.to_dict()
# create an instance of PhraseMergeItem from a dict
phrase_merge_item_from_dict = PhraseMergeItem.from_dict(phrase_merge_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


