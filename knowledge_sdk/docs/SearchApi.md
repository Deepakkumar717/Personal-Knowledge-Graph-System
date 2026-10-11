# knowledge_sdk.SearchApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**autocomplete**](SearchApi.md#autocomplete) | **GET** /search/suggest | Autocomplete suggestions
[**search_notes**](SearchApi.md#search_notes) | **GET** /search/ | Search notes full-text
[**suggest_links**](SearchApi.md#suggest_links) | **GET** /suggest/links | Suggest potential links for note
[**suggest_titles**](SearchApi.md#suggest_titles) | **GET** /titles/suggest | Suggest titles for wikilink editor popup


# **autocomplete**
> AutocompleteResponse autocomplete(q, limit=limit)

Autocomplete suggestions

Fast autocomplete ranking title prefix > tag prefix > title substring > fuzzy.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.autocomplete_response import AutocompleteResponse
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
    api_instance = knowledge_sdk.SearchApi(api_client)
    q = 'q_example' # str | Autocomplete prefix query
    limit = 10 # int | Max items to return (optional) (default to 10)

    try:
        # Autocomplete suggestions
        api_response = api_instance.autocomplete(q, limit=limit)
        print("The response of SearchApi->autocomplete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->autocomplete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Autocomplete prefix query | 
 **limit** | **int**| Max items to return | [optional] [default to 10]

### Return type

[**AutocompleteResponse**](AutocompleteResponse.md)

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

# **search_notes**
> SearchResponse search_notes(q=q, tag=tag, limit=limit)

Search notes full-text

Ranked full-text search using SQLite FTS5 BM25 ranking and fuzzy fallback.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.search_response import SearchResponse
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
    api_instance = knowledge_sdk.SearchApi(api_client)
    q = '' # str | Full text search query with support for #tag (optional) (default to '')
    tag = 'tag_example' # str | Tag filter (optional)
    limit = 50 # int | Max search results (optional) (default to 50)

    try:
        # Search notes full-text
        api_response = api_instance.search_notes(q=q, tag=tag, limit=limit)
        print("The response of SearchApi->search_notes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->search_notes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Full text search query with support for #tag | [optional] [default to &#39;&#39;]
 **tag** | **str**| Tag filter | [optional] 
 **limit** | **int**| Max search results | [optional] [default to 50]

### Return type

[**SearchResponse**](SearchResponse.md)

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

# **suggest_links**
> List[SuggestedLinkRead] suggest_links(note_id, limit=limit)

Suggest potential links for note

Suggest links based on TF-IDF similarity and shared tags, excluding existing links.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.suggested_link_read import SuggestedLinkRead
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
    api_instance = knowledge_sdk.SearchApi(api_client)
    note_id = 56 # int | Note ID to find suggestions for
    limit = 5 # int | Max suggestions (optional) (default to 5)

    try:
        # Suggest potential links for note
        api_response = api_instance.suggest_links(note_id, limit=limit)
        print("The response of SearchApi->suggest_links:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->suggest_links: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| Note ID to find suggestions for | 
 **limit** | **int**| Max suggestions | [optional] [default to 5]

### Return type

[**List[SuggestedLinkRead]**](SuggestedLinkRead.md)

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

# **suggest_titles**
> TitleSuggestResponse suggest_titles(q=q, limit=limit)

Suggest titles for wikilink editor popup

Suggest existing note titles for [[ popup autocomplete during editing.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.title_suggest_response import TitleSuggestResponse
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
    api_instance = knowledge_sdk.SearchApi(api_client)
    q = '' # str | Title query prefix (optional) (default to '')
    limit = 10 # int | Max suggestions (optional) (default to 10)

    try:
        # Suggest titles for wikilink editor popup
        api_response = api_instance.suggest_titles(q=q, limit=limit)
        print("The response of SearchApi->suggest_titles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->suggest_titles: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Title query prefix | [optional] [default to &#39;&#39;]
 **limit** | **int**| Max suggestions | [optional] [default to 10]

### Return type

[**TitleSuggestResponse**](TitleSuggestResponse.md)

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

