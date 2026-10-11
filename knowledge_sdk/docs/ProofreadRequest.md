# ProofreadRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** |  | 
**ignored_words** | **List[str]** |  | [optional] 

## Example

```python
from knowledge_sdk.models.proofread_request import ProofreadRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ProofreadRequest from a JSON string
proofread_request_instance = ProofreadRequest.from_json(json)
# print the JSON string representation of the object
print(ProofreadRequest.to_json())

# convert the object into a dict
proofread_request_dict = proofread_request_instance.to_dict()
# create an instance of ProofreadRequest from a dict
proofread_request_from_dict = ProofreadRequest.from_dict(proofread_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


