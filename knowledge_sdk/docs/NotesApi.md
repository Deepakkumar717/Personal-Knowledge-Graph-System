# knowledge_sdk.NotesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_note**](NotesApi.md#create_note) | **POST** /notes/ | Create a new note
[**delete_note**](NotesApi.md#delete_note) | **DELETE** /notes/{note_id} | Delete a note
[**get_note**](NotesApi.md#get_note) | **GET** /notes/{note_id} | Get note details
[**get_note_backlinks**](NotesApi.md#get_note_backlinks) | **GET** /notes/{note_id}/backlinks | Get backlinks for note
[**get_note_mentions**](NotesApi.md#get_note_mentions) | **GET** /notes/{note_id}/mentions | Get unlinked mentions
[**get_note_related**](NotesApi.md#get_note_related) | **GET** /notes/{note_id}/related | Get related notes
[**link_notes**](NotesApi.md#link_notes) | **PATCH** /notes/{note_id}/link | Create manual link
[**list_notes**](NotesApi.md#list_notes) | **GET** /notes/ | List notes
[**patch_note**](NotesApi.md#patch_note) | **PATCH** /notes/{note_id} | Partial update a note
[**unlink_notes**](NotesApi.md#unlink_notes) | **DELETE** /notes/{note_id}/link/{target_id} | Remove a link
[**update_note**](NotesApi.md#update_note) | **PUT** /notes/{note_id} | Update a note


# **create_note**
> NoteDetail create_note(note_create)

Create a new note

Create a new note with title, markdown content, and optional tags.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_create import NoteCreate
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_create = knowledge_sdk.NoteCreate() # NoteCreate | 

    try:
        # Create a new note
        api_response = api_instance.create_note(note_create)
        print("The response of NotesApi->create_note:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->create_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_create** | [**NoteCreate**](NoteCreate.md)|  | 

### Return type

[**NoteDetail**](NoteDetail.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_note**
> NoteDeleteResponse delete_note(note_id)

Delete a note

Delete a note and cascade its links and tags.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_delete_response import NoteDeleteResponse
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | Positive integer note ID

    try:
        # Delete a note
        api_response = api_instance.delete_note(note_id)
        print("The response of NotesApi->delete_note:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->delete_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| Positive integer note ID | 

### Return type

[**NoteDeleteResponse**](NoteDeleteResponse.md)

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

# **get_note**
> NoteDetail get_note(note_id)

Get note details

Get full details of a note including outgoing links, backlinks, unresolved links, and related notes.

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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | Positive integer note ID

    try:
        # Get note details
        api_response = api_instance.get_note(note_id)
        print("The response of NotesApi->get_note:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->get_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| Positive integer note ID | 

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

# **get_note_backlinks**
> List[NoteBacklinkItem] get_note_backlinks(note_id)

Get backlinks for note

Get all incoming backlinks pointing to this note.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_backlink_item import NoteBacklinkItem
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | Positive integer note ID

    try:
        # Get backlinks for note
        api_response = api_instance.get_note_backlinks(note_id)
        print("The response of NotesApi->get_note_backlinks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->get_note_backlinks: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| Positive integer note ID | 

### Return type

[**List[NoteBacklinkItem]**](NoteBacklinkItem.md)

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

# **get_note_mentions**
> List[UnlinkedMentionItem] get_note_mentions(note_id)

Get unlinked mentions

Get unlinked mentions of this note title in other notes.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.unlinked_mention_item import UnlinkedMentionItem
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | Positive integer note ID

    try:
        # Get unlinked mentions
        api_response = api_instance.get_note_mentions(note_id)
        print("The response of NotesApi->get_note_mentions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->get_note_mentions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| Positive integer note ID | 

### Return type

[**List[UnlinkedMentionItem]**](UnlinkedMentionItem.md)

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

# **get_note_related**
> List[RelatedNoteItem] get_note_related(note_id, limit=limit)

Get related notes

Get TF-IDF and tag-similarity related notes.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.related_note_item import RelatedNoteItem
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | Positive integer note ID
    limit = 5 # int | Max items to return (optional) (default to 5)

    try:
        # Get related notes
        api_response = api_instance.get_note_related(note_id, limit=limit)
        print("The response of NotesApi->get_note_related:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->get_note_related: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| Positive integer note ID | 
 **limit** | **int**| Max items to return | [optional] [default to 5]

### Return type

[**List[RelatedNoteItem]**](RelatedNoteItem.md)

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

# **link_notes**
> LinkRead link_notes(note_id, link_create)

Create manual link

Create a manual directed link from source note to target note.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.link_create import LinkCreate
from knowledge_sdk.models.link_read import LinkRead
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | Positive integer source note ID
    link_create = knowledge_sdk.LinkCreate() # LinkCreate | 

    try:
        # Create manual link
        api_response = api_instance.link_notes(note_id, link_create)
        print("The response of NotesApi->link_notes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->link_notes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| Positive integer source note ID | 
 **link_create** | [**LinkCreate**](LinkCreate.md)|  | 

### Return type

[**LinkRead**](LinkRead.md)

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

# **list_notes**
> List[NoteListItem] list_notes(tag=tag, q=q, limit=limit, offset=offset, sort=sort, pinned=pinned)

List notes

List notes with filtering by tag, query, sorting, and pagination.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_list_item import NoteListItem
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    tag = 'tag_example' # str | Filter by tag name (optional)
    q = 'q_example' # str | Search query string in title or content (optional)
    limit = 50 # int | Max items to return (1-200) (optional) (default to 50)
    offset = 0 # int | Offset for pagination (optional) (default to 0)
    sort = 'updated' # str | Sort order (optional) (default to 'updated')
    pinned = True # bool | Filter by pinned status (optional)

    try:
        # List notes
        api_response = api_instance.list_notes(tag=tag, q=q, limit=limit, offset=offset, sort=sort, pinned=pinned)
        print("The response of NotesApi->list_notes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->list_notes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag** | **str**| Filter by tag name | [optional] 
 **q** | **str**| Search query string in title or content | [optional] 
 **limit** | **int**| Max items to return (1-200) | [optional] [default to 50]
 **offset** | **int**| Offset for pagination | [optional] [default to 0]
 **sort** | **str**| Sort order | [optional] [default to &#39;updated&#39;]
 **pinned** | **bool**| Filter by pinned status | [optional] 

### Return type

[**List[NoteListItem]**](NoteListItem.md)

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

# **patch_note**
> NoteDetail patch_note(note_id, note_patch)

Partial update a note

Partial update of note fields such as title, content, tags, or pinned state.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_detail import NoteDetail
from knowledge_sdk.models.note_patch import NotePatch
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | Positive integer note ID
    note_patch = knowledge_sdk.NotePatch() # NotePatch | 

    try:
        # Partial update a note
        api_response = api_instance.patch_note(note_id, note_patch)
        print("The response of NotesApi->patch_note:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->patch_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| Positive integer note ID | 
 **note_patch** | [**NotePatch**](NotePatch.md)|  | 

### Return type

[**NoteDetail**](NoteDetail.md)

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

# **unlink_notes**
> LinkDeleteResponse unlink_notes(note_id, target_id)

Remove a link

Remove a link between source note and target note.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.link_delete_response import LinkDeleteResponse
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | Positive integer source note ID
    target_id = 56 # int | Positive integer target note ID

    try:
        # Remove a link
        api_response = api_instance.unlink_notes(note_id, target_id)
        print("The response of NotesApi->unlink_notes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->unlink_notes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| Positive integer source note ID | 
 **target_id** | **int**| Positive integer target note ID | 

### Return type

[**LinkDeleteResponse**](LinkDeleteResponse.md)

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

# **update_note**
> NoteDetail update_note(note_id, note_update)

Update a note

Full update of note title, content, and tags.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_detail import NoteDetail
from knowledge_sdk.models.note_update import NoteUpdate
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | Positive integer note ID
    note_update = knowledge_sdk.NoteUpdate() # NoteUpdate | 

    try:
        # Update a note
        api_response = api_instance.update_note(note_id, note_update)
        print("The response of NotesApi->update_note:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->update_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| Positive integer note ID | 
 **note_update** | [**NoteUpdate**](NoteUpdate.md)|  | 

### Return type

[**NoteDetail**](NoteDetail.md)

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

