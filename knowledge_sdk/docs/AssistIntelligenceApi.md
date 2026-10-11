# knowledge_sdk.AssistIntelligenceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**assist_tags**](AssistIntelligenceApi.md#assist_tags) | **POST** /assist/tags | Assist Tags
[**dismiss_link_suggestion**](AssistIntelligenceApi.md#dismiss_link_suggestion) | **POST** /assist/link-suggestions/dismiss | Dismiss Link Suggestion
[**get_assist_status**](AssistIntelligenceApi.md#get_assist_status) | **GET** /assist/status | Get Status
[**get_link_suggestions**](AssistIntelligenceApi.md#get_link_suggestions) | **GET** /assist/link-suggestions | Get Link Suggestions
[**proofread_content**](AssistIntelligenceApi.md#proofread_content) | **POST** /assist/proofread | Proofread


# **assist_tags**
> TagAssistResponse assist_tags(tag_assist_request)

Assist Tags

Analyzes note tags: normalizes input, detects phrase merge opportunities,
typos, and derives smart keyword tag suggestions from note content.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.tag_assist_request import TagAssistRequest
from knowledge_sdk.models.tag_assist_response import TagAssistResponse
from knowledge_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = knowledge_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with knowledge_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = knowledge_sdk.AssistIntelligenceApi(api_client)
    tag_assist_request = knowledge_sdk.TagAssistRequest() # TagAssistRequest | 

    try:
        # Assist Tags
        api_response = api_instance.assist_tags(tag_assist_request)
        print("The response of AssistIntelligenceApi->assist_tags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssistIntelligenceApi->assist_tags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag_assist_request** | [**TagAssistRequest**](TagAssistRequest.md)|  | 

### Return type

[**TagAssistResponse**](TagAssistResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dismiss_link_suggestion**
> DismissSuggestionResponse dismiss_link_suggestion(dismiss_suggestion_request)

Dismiss Link Suggestion

Dismisses a link suggestion pair permanently so it never reappears.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.dismiss_suggestion_request import DismissSuggestionRequest
from knowledge_sdk.models.dismiss_suggestion_response import DismissSuggestionResponse
from knowledge_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = knowledge_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with knowledge_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = knowledge_sdk.AssistIntelligenceApi(api_client)
    dismiss_suggestion_request = knowledge_sdk.DismissSuggestionRequest() # DismissSuggestionRequest | 

    try:
        # Dismiss Link Suggestion
        api_response = api_instance.dismiss_link_suggestion(dismiss_suggestion_request)
        print("The response of AssistIntelligenceApi->dismiss_link_suggestion:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssistIntelligenceApi->dismiss_link_suggestion: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dismiss_suggestion_request** | [**DismissSuggestionRequest**](DismissSuggestionRequest.md)|  | 

### Return type

[**DismissSuggestionResponse**](DismissSuggestionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_assist_status**
> AssistStatusResponse get_assist_status()

Get Status

Reports whether AI assistant is enabled and the active provider information.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.assist_status_response import AssistStatusResponse
from knowledge_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = knowledge_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with knowledge_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = knowledge_sdk.AssistIntelligenceApi(api_client)

    try:
        # Get Status
        api_response = api_instance.get_assist_status()
        print("The response of AssistIntelligenceApi->get_assist_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssistIntelligenceApi->get_assist_status: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**AssistStatusResponse**](AssistStatusResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_link_suggestions**
> List[LinkSuggestionItem] get_link_suggestions(note_id)

Get Link Suggestions

Calculates multi-signal link suggestions based on text mentions, TF-IDF similarity,
shared tags, and mutual neighbours, excluding dismissed or already linked notes.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.link_suggestion_item import LinkSuggestionItem
from knowledge_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = knowledge_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with knowledge_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = knowledge_sdk.AssistIntelligenceApi(api_client)
    note_id = 56 # int | ID of the note to retrieve link suggestions for

    try:
        # Get Link Suggestions
        api_response = api_instance.get_link_suggestions(note_id)
        print("The response of AssistIntelligenceApi->get_link_suggestions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssistIntelligenceApi->get_link_suggestions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| ID of the note to retrieve link suggestions for | 

### Return type

[**List[LinkSuggestionItem]**](LinkSuggestionItem.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **proofread_content**
> List[ProofreadIssue] proofread_content(proofread_request)

Proofread

Performs deterministic offline proofreading on note text:
checks casing, repeated words, and typos while exempting code, wikilinks, and known titles.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.proofread_issue import ProofreadIssue
from knowledge_sdk.models.proofread_request import ProofreadRequest
from knowledge_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = knowledge_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with knowledge_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = knowledge_sdk.AssistIntelligenceApi(api_client)
    proofread_request = knowledge_sdk.ProofreadRequest() # ProofreadRequest | 

    try:
        # Proofread
        api_response = api_instance.proofread_content(proofread_request)
        print("The response of AssistIntelligenceApi->proofread_content:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssistIntelligenceApi->proofread_content: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **proofread_request** | [**ProofreadRequest**](ProofreadRequest.md)|  | 

### Return type

[**List[ProofreadIssue]**](ProofreadIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

