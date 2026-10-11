# knowledge_sdk.SystemApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**events_stream**](SystemApi.md#events_stream) | **GET** /events | Subscribe to SSE events
[**export_graph_data**](SystemApi.md#export_graph_data) | **GET** /export | Export knowledge graph data
[**get_activity_log**](SystemApi.md#get_activity_log) | **GET** /system/activity | Get recent activity log
[**health_check**](SystemApi.md#health_check) | **GET** /health | Health check
[**import_graph_data**](SystemApi.md#import_graph_data) | **POST** /import | Import knowledge graph data
[**list_backups**](SystemApi.md#list_backups) | **GET** /system/backups | List database backups
[**reset_database**](SystemApi.md#reset_database) | **DELETE** /system/reset | Reset database to empty state
[**restore_backup**](SystemApi.md#restore_backup) | **POST** /system/backups/restore | Restore database backup


# **events_stream**
> object events_stream()

Subscribe to SSE events

Server-Sent Events (SSE) stream broadcasting real-time graph mutations.

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
    api_instance = knowledge_sdk.SystemApi(api_client)

    try:
        # Subscribe to SSE events
        api_response = api_instance.events_stream()
        print("The response of SystemApi->events_stream:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->events_stream: %s\n" % e)
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

# **export_graph_data**
> object export_graph_data()

Export knowledge graph data

Export all notes, tags, and links as a JSON file.

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
    api_instance = knowledge_sdk.SystemApi(api_client)

    try:
        # Export knowledge graph data
        api_response = api_instance.export_graph_data()
        print("The response of SystemApi->export_graph_data:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->export_graph_data: %s\n" % e)
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

# **get_activity_log**
> List[ActivityLogItem] get_activity_log(limit=limit)

Get recent activity log

Fetch recent system activity log items.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.activity_log_item import ActivityLogItem
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
    api_instance = knowledge_sdk.SystemApi(api_client)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get recent activity log
        api_response = api_instance.get_activity_log(limit=limit)
        print("The response of SystemApi->get_activity_log:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->get_activity_log: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[ActivityLogItem]**](ActivityLogItem.md)

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

# **health_check**
> HealthResponse health_check()

Health check

Health check endpoint exposing service status, resolved absolute database path, and backups count.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.health_response import HealthResponse
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
    api_instance = knowledge_sdk.SystemApi(api_client)

    try:
        # Health check
        api_response = api_instance.health_check()
        print("The response of SystemApi->health_check:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->health_check: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**HealthResponse**](HealthResponse.md)

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

# **import_graph_data**
> object import_graph_data(request_body)

Import knowledge graph data

Import notes, tags, and links from a JSON payload.

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
    api_instance = knowledge_sdk.SystemApi(api_client)
    request_body = None # Dict[str, Optional[object]] | 

    try:
        # Import knowledge graph data
        api_response = api_instance.import_graph_data(request_body)
        print("The response of SystemApi->import_graph_data:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->import_graph_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**Dict[str, Optional[object]]**](object.md)|  | 

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

# **list_backups**
> List[BackupItem] list_backups()

List database backups

List all available database backup files.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.backup_item import BackupItem
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
    api_instance = knowledge_sdk.SystemApi(api_client)

    try:
        # List database backups
        api_response = api_instance.list_backups()
        print("The response of SystemApi->list_backups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->list_backups: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[BackupItem]**](BackupItem.md)

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

# **reset_database**
> object reset_database(reset_database_request)

Reset database to empty state

Clear all notes, tags, links, and groups. Requires explicit confirmation 'DELETE ALL'. Takes automatic backup first.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.reset_database_request import ResetDatabaseRequest
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
    api_instance = knowledge_sdk.SystemApi(api_client)
    reset_database_request = knowledge_sdk.ResetDatabaseRequest() # ResetDatabaseRequest | 

    try:
        # Reset database to empty state
        api_response = api_instance.reset_database(reset_database_request)
        print("The response of SystemApi->reset_database:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->reset_database: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **reset_database_request** | [**ResetDatabaseRequest**](ResetDatabaseRequest.md)|  | 

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

# **restore_backup**
> object restore_backup(restore_backup_request)

Restore database backup

Restores database from specified backup. Requires confirm: 'RESTORE'.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.restore_backup_request import RestoreBackupRequest
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
    api_instance = knowledge_sdk.SystemApi(api_client)
    restore_backup_request = knowledge_sdk.RestoreBackupRequest() # RestoreBackupRequest | 

    try:
        # Restore database backup
        api_response = api_instance.restore_backup(restore_backup_request)
        print("The response of SystemApi->restore_backup:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->restore_backup: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **restore_backup_request** | [**RestoreBackupRequest**](RestoreBackupRequest.md)|  | 

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

