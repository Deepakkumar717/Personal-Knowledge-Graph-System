# knowledge_sdk.TrashApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_trash_item**](TrashApi.md#delete_trash_item) | **DELETE** /trash/{trash_id} | Permanently delete trash item
[**empty_trash**](TrashApi.md#empty_trash) | **DELETE** /trash/ | Empty trash
[**get_trash_item**](TrashApi.md#get_trash_item) | **GET** /trash/{trash_id} | Get trash item details
[**list_trash**](TrashApi.md#list_trash) | **GET** /trash/ | List trash items
[**restore_note_from_trash**](TrashApi.md#restore_note_from_trash) | **POST** /trash/{trash_id}/restore | Restore note from trash


# **delete_trash_item**
> object delete_trash_item(trash_id)

Permanently delete trash item

Permanently delete a note snapshot from trash.

### Example


```python
import knowledge_sdk
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
    api_instance = knowledge_sdk.TrashApi(api_client)
    trash_id = 56 # int | 

    try:
        # Permanently delete trash item
        api_response = api_instance.delete_trash_item(trash_id)
        print("The response of TrashApi->delete_trash_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrashApi->delete_trash_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trash_id** | **int**|  | 

### Return type

**object**

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

# **empty_trash**
> object empty_trash()

Empty trash

Permanently delete all items from trash.

### Example


```python
import knowledge_sdk
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
    api_instance = knowledge_sdk.TrashApi(api_client)

    try:
        # Empty trash
        api_response = api_instance.empty_trash()
        print("The response of TrashApi->empty_trash:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrashApi->empty_trash: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

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

# **get_trash_item**
> TrashDetail get_trash_item(trash_id)

Get trash item details

View details and snapshot payload of a deleted note in trash.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.trash_detail import TrashDetail
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
    api_instance = knowledge_sdk.TrashApi(api_client)
    trash_id = 56 # int | 

    try:
        # Get trash item details
        api_response = api_instance.get_trash_item(trash_id)
        print("The response of TrashApi->get_trash_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrashApi->get_trash_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trash_id** | **int**|  | 

### Return type

[**TrashDetail**](TrashDetail.md)

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

# **list_trash**
> List[TrashItem] list_trash()

List trash items

List deleted notes currently stored in trash (snapshots kept for 30 days).

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.trash_item import TrashItem
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
    api_instance = knowledge_sdk.TrashApi(api_client)

    try:
        # List trash items
        api_response = api_instance.list_trash()
        print("The response of TrashApi->list_trash:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrashApi->list_trash: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[TrashItem]**](TrashItem.md)

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

# **restore_note_from_trash**
> NoteDetail restore_note_from_trash(trash_id)

Restore note from trash

Recreate note from trash snapshot, restoring tags, links, and group. Returns 409 if title is taken.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_detail import NoteDetail
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
    api_instance = knowledge_sdk.TrashApi(api_client)
    trash_id = 56 # int | 

    try:
        # Restore note from trash
        api_response = api_instance.restore_note_from_trash(trash_id)
        print("The response of TrashApi->restore_note_from_trash:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrashApi->restore_note_from_trash: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trash_id** | **int**|  | 

### Return type

[**NoteDetail**](NoteDetail.md)

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

