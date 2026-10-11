# AutocompleteItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**id** | **int** |  | [optional] 
**title** | **str** |  | 
**score** | **float** |  | 

## Example

```python
from knowledge_sdk.models.autocomplete_item import AutocompleteItem

# TODO update the JSON string below
json = "{}"
# create an instance of AutocompleteItem from a JSON string
autocomplete_item_instance = AutocompleteItem.from_json(json)
# print the JSON string representation of the object
print(AutocompleteItem.to_json())

# convert the object into a dict
autocomplete_item_dict = autocomplete_item_instance.to_dict()
# create an instance of AutocompleteItem from a dict
autocomplete_item_from_dict = AutocompleteItem.from_dict(autocomplete_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


