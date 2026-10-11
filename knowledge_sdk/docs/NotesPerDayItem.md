# NotesPerDayItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **str** |  | 
**count** | **int** |  | 

## Example

```python
from knowledge_sdk.models.notes_per_day_item import NotesPerDayItem

# TODO update the JSON string below
json = "{}"
# create an instance of NotesPerDayItem from a JSON string
notes_per_day_item_instance = NotesPerDayItem.from_json(json)
# print the JSON string representation of the object
print(NotesPerDayItem.to_json())

# convert the object into a dict
notes_per_day_item_dict = notes_per_day_item_instance.to_dict()
# create an instance of NotesPerDayItem from a dict
notes_per_day_item_from_dict = NotesPerDayItem.from_dict(notes_per_day_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


