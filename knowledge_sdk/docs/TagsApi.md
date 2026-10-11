# knowledge_sdk.TagsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_tags**](TagsApi.md#list_tags) | **GET** /tags/ | List all tags
[**suggest_tags**](TagsApi.md#suggest_tags) | **GET** /tags/suggest | Suggest tags


# **list_tags**
> List[TagUsage] list_tags()

List all tags

List all tags in the system ordered by usage count.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.tag_usage import TagUsage
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
    api_instance = knowledge_sdk.TagsApi(api_client)

    try:
        # List all tags
        api_response = api_instance.list_tags()
        print("The response of TagsApi->list_tags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TagsApi->list_tags: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[TagUsage]**](TagUsage.md)

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

# **suggest_tags**
> TagSuggestResponse suggest_tags(q=q, selected=selected, content=content, limit=limit)

Suggest tags

Suggest tags based on query prefix, fuzzy match, popularity, co-occurrence, and note content.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.tag_suggest_response import TagSuggestResponse
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
    api_instance = knowledge_sdk.TagsApi(api_client)
    q = '' # str | Tag prefix or search term (optional) (default to '')
    selected = ['selected_example'] # List[str] | Currently selected tags for co-occurrence boost (optional)
    content = 'content_example' # str | Optional note text for keyword matching (optional)
    limit = 10 # int | Max suggestions (optional) (default to 10)

    try:
        # Suggest tags
        api_response = api_instance.suggest_tags(q=q, selected=selected, content=content, limit=limit)
        print("The response of TagsApi->suggest_tags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TagsApi->suggest_tags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Tag prefix or search term | [optional] [default to &#39;&#39;]
 **selected** | [**List[str]**](str.md)| Currently selected tags for co-occurrence boost | [optional] 
 **content** | **str**| Optional note text for keyword matching | [optional] 
 **limit** | **int**| Max suggestions | [optional] [default to 10]

### Return type

[**TagSuggestResponse**](TagSuggestResponse.md)

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

