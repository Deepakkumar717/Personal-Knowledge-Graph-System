# knowledge_sdk.GroupsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_notes_to_group**](GroupsApi.md#add_notes_to_group) | **PUT** /groups/{group_id}/notes | Add or move notes to group
[**apply_group_suggestions**](GroupsApi.md#apply_group_suggestions) | **POST** /groups/suggestions/apply | Apply group suggestions
[**create_group**](GroupsApi.md#create_group) | **POST** /groups/ | Create a new group
[**delete_group**](GroupsApi.md#delete_group) | **DELETE** /groups/{group_id} | Delete a group
[**dismiss_group_suggestion_for_note**](GroupsApi.md#dismiss_group_suggestion_for_note) | **POST** /groups/suggest-for-note/{note_id}/dismiss/{group_id} | Dismiss group suggestion for note
[**get_group_suggestions**](GroupsApi.md#get_group_suggestions) | **GET** /groups/suggestions | Get group suggestions
[**list_groups**](GroupsApi.md#list_groups) | **GET** /groups/ | List all groups
[**merge_groups**](GroupsApi.md#merge_groups) | **POST** /groups/{group_id}/merge | Merge group into another
[**remove_note_from_group**](GroupsApi.md#remove_note_from_group) | **DELETE** /groups/{group_id}/notes/{note_id} | Remove note from group
[**suggest_group_for_note**](GroupsApi.md#suggest_group_for_note) | **GET** /groups/suggest-for-note/{note_id} | Suggest group for note
[**update_group**](GroupsApi.md#update_group) | **PATCH** /groups/{group_id} | Update a group


# **add_notes_to_group**
> object add_notes_to_group(group_id, group_add_notes_request)

Add or move notes to group

Add or move note IDs to this group.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.group_add_notes_request import GroupAddNotesRequest
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
    api_instance = knowledge_sdk.GroupsApi(api_client)
    group_id = 56 # int | 
    group_add_notes_request = knowledge_sdk.GroupAddNotesRequest() # GroupAddNotesRequest | 

    try:
        # Add or move notes to group
        api_response = api_instance.add_notes_to_group(group_id, group_add_notes_request)
        print("The response of GroupsApi->add_notes_to_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->add_notes_to_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **int**|  | 
 **group_add_notes_request** | [**GroupAddNotesRequest**](GroupAddNotesRequest.md)|  | 

### Return type

**object**

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

# **apply_group_suggestions**
> object apply_group_suggestions(group_suggestions_apply_request)

Apply group suggestions

Apply chosen group suggestions to automatically organize notes into groups.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.group_suggestions_apply_request import GroupSuggestionsApplyRequest
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
    api_instance = knowledge_sdk.GroupsApi(api_client)
    group_suggestions_apply_request = knowledge_sdk.GroupSuggestionsApplyRequest() # GroupSuggestionsApplyRequest | 

    try:
        # Apply group suggestions
        api_response = api_instance.apply_group_suggestions(group_suggestions_apply_request)
        print("The response of GroupsApi->apply_group_suggestions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->apply_group_suggestions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_suggestions_apply_request** | [**GroupSuggestionsApplyRequest**](GroupSuggestionsApplyRequest.md)|  | 

### Return type

**object**

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

# **create_group**
> GroupRead create_group(group_create)

Create a new group

Create a new topic group with name and hex color.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.group_create import GroupCreate
from knowledge_sdk.models.group_read import GroupRead
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
    api_instance = knowledge_sdk.GroupsApi(api_client)
    group_create = knowledge_sdk.GroupCreate() # GroupCreate | 

    try:
        # Create a new group
        api_response = api_instance.create_group(group_create)
        print("The response of GroupsApi->create_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->create_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_create** | [**GroupCreate**](GroupCreate.md)|  | 

### Return type

[**GroupRead**](GroupRead.md)

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

# **delete_group**
> object delete_group(group_id)

Delete a group

Delete a topic group. Member notes remain safe and become ungrouped.

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
    api_instance = knowledge_sdk.GroupsApi(api_client)
    group_id = 56 # int | 

    try:
        # Delete a group
        api_response = api_instance.delete_group(group_id)
        print("The response of GroupsApi->delete_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->delete_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **int**|  | 

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

# **dismiss_group_suggestion_for_note**
> object dismiss_group_suggestion_for_note(note_id, group_id)

Dismiss group suggestion for note

Remember that the user declined assigning note to this group.

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
    api_instance = knowledge_sdk.GroupsApi(api_client)
    note_id = 56 # int | 
    group_id = 56 # int | 

    try:
        # Dismiss group suggestion for note
        api_response = api_instance.dismiss_group_suggestion_for_note(note_id, group_id)
        print("The response of GroupsApi->dismiss_group_suggestion_for_note:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->dismiss_group_suggestion_for_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**|  | 
 **group_id** | **int**|  | 

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

# **get_group_suggestions**
> GroupSuggestionsResponse get_group_suggestions()

Get group suggestions

Detect natural topic clusters using community detection on the multi-signal graph.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.group_suggestions_response import GroupSuggestionsResponse
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
    api_instance = knowledge_sdk.GroupsApi(api_client)

    try:
        # Get group suggestions
        api_response = api_instance.get_group_suggestions()
        print("The response of GroupsApi->get_group_suggestions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->get_group_suggestions: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GroupSuggestionsResponse**](GroupSuggestionsResponse.md)

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

# **list_groups**
> List[GroupRead] list_groups()

List all groups

List all topic groups with member note counts.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.group_read import GroupRead
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
    api_instance = knowledge_sdk.GroupsApi(api_client)

    try:
        # List all groups
        api_response = api_instance.list_groups()
        print("The response of GroupsApi->list_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->list_groups: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[GroupRead]**](GroupRead.md)

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

# **merge_groups**
> object merge_groups(group_id, group_merge_request)

Merge group into another

Merge group into target group and delete this group.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.group_merge_request import GroupMergeRequest
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
    api_instance = knowledge_sdk.GroupsApi(api_client)
    group_id = 56 # int | 
    group_merge_request = knowledge_sdk.GroupMergeRequest() # GroupMergeRequest | 

    try:
        # Merge group into another
        api_response = api_instance.merge_groups(group_id, group_merge_request)
        print("The response of GroupsApi->merge_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->merge_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **int**|  | 
 **group_merge_request** | [**GroupMergeRequest**](GroupMergeRequest.md)|  | 

### Return type

**object**

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

# **remove_note_from_group**
> object remove_note_from_group(group_id, note_id)

Remove note from group

Remove a note from this group, returning it to ungrouped.

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
    api_instance = knowledge_sdk.GroupsApi(api_client)
    group_id = 56 # int | 
    note_id = 56 # int | 

    try:
        # Remove note from group
        api_response = api_instance.remove_note_from_group(group_id, note_id)
        print("The response of GroupsApi->remove_note_from_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->remove_note_from_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **int**|  | 
 **note_id** | **int**|  | 

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

# **suggest_group_for_note**
> GroupSuggestForNoteResponse suggest_group_for_note(note_id)

Suggest group for note

Suggest an existing topic group for a specific note.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.group_suggest_for_note_response import GroupSuggestForNoteResponse
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
    api_instance = knowledge_sdk.GroupsApi(api_client)
    note_id = 56 # int | 

    try:
        # Suggest group for note
        api_response = api_instance.suggest_group_for_note(note_id)
        print("The response of GroupsApi->suggest_group_for_note:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->suggest_group_for_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**|  | 

### Return type

[**GroupSuggestForNoteResponse**](GroupSuggestForNoteResponse.md)

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

# **update_group**
> GroupRead update_group(group_id, group_update)

Update a group

Rename or recolor an existing group.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.group_read import GroupRead
from knowledge_sdk.models.group_update import GroupUpdate
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
    api_instance = knowledge_sdk.GroupsApi(api_client)
    group_id = 56 # int | 
    group_update = knowledge_sdk.GroupUpdate() # GroupUpdate | 

    try:
        # Update a group
        api_response = api_instance.update_group(group_id, group_update)
        print("The response of GroupsApi->update_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->update_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **int**|  | 
 **group_update** | [**GroupUpdate**](GroupUpdate.md)|  | 

### Return type

[**GroupRead**](GroupRead.md)

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

