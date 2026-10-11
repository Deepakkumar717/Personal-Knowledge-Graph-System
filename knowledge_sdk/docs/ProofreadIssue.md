# ProofreadIssue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **int** |  | 
**end** | **int** |  | 
**original** | **str** |  | 
**suggestion** | **str** |  | 
**reason** | **str** |  | 

## Example

```python
from knowledge_sdk.models.proofread_issue import ProofreadIssue

# TODO update the JSON string below
json = "{}"
# create an instance of ProofreadIssue from a JSON string
proofread_issue_instance = ProofreadIssue.from_json(json)
# print the JSON string representation of the object
print(ProofreadIssue.to_json())

# convert the object into a dict
proofread_issue_dict = proofread_issue_instance.to_dict()
# create an instance of ProofreadIssue from a dict
proofread_issue_from_dict = ProofreadIssue.from_dict(proofread_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


