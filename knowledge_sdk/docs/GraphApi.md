# knowledge_sdk.GraphApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_graph**](GraphApi.md#get_graph) | **GET** /graph/ | Get full graph
[**get_graph_neighbors**](GraphApi.md#get_graph_neighbors) | **GET** /graph/neighbors/{note_id} | Get BFS neighborhood of a note
[**get_graph_stats**](GraphApi.md#get_graph_stats) | **GET** /graph/stats | Get knowledge graph statistics
[**get_insights**](GraphApi.md#get_insights) | **GET** /graph/insights | Get knowledge graph insights and analytics
[**get_shortest_path**](GraphApi.md#get_shortest_path) | **GET** /graph/path | Find shortest path between two notes


# **get_graph**
> GraphResponse get_graph(tag=tag)

Get full graph

Retrieve graph nodes, directed edges, and adjacency list for visualization.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.graph_response import GraphResponse
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
    api_instance = knowledge_sdk.GraphApi(api_client)
    tag = 'tag_example' # str | Optional tag filter for graph nodes (optional)

    try:
        # Get full graph
        api_response = api_instance.get_graph(tag=tag)
        print("The response of GraphApi->get_graph:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GraphApi->get_graph: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag** | **str**| Optional tag filter for graph nodes | [optional] 

### Return type

[**GraphResponse**](GraphResponse.md)

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

# **get_graph_neighbors**
> GraphResponse get_graph_neighbors(note_id, depth=depth)

Get BFS neighborhood of a note

Retrieve neighborhood subgraph around a note using BFS up to depth.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.graph_response import GraphResponse
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
    api_instance = knowledge_sdk.GraphApi(api_client)
    note_id = 56 # int | Center note ID
    depth = 1 # int | BFS exploration depth (1-4) (optional) (default to 1)

    try:
        # Get BFS neighborhood of a note
        api_response = api_instance.get_graph_neighbors(note_id, depth=depth)
        print("The response of GraphApi->get_graph_neighbors:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GraphApi->get_graph_neighbors: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| Center note ID | 
 **depth** | **int**| BFS exploration depth (1-4) | [optional] [default to 1]

### Return type

[**GraphResponse**](GraphResponse.md)

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

# **get_graph_stats**
> GraphStats get_graph_stats()

Get knowledge graph statistics

Get network statistics: total notes, links, tags, orphans, hub nodes, tag distribution.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.graph_stats import GraphStats
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
    api_instance = knowledge_sdk.GraphApi(api_client)

    try:
        # Get knowledge graph statistics
        api_response = api_instance.get_graph_stats()
        print("The response of GraphApi->get_graph_stats:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GraphApi->get_graph_stats: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GraphStats**](GraphStats.md)

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

# **get_insights**
> GraphInsightsResponse get_insights()

Get knowledge graph insights and analytics

Retrieve comprehensive graph analytics: top tags, groups, activity over 30 days, hubs, orphans, and link types.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.graph_insights_response import GraphInsightsResponse
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
    api_instance = knowledge_sdk.GraphApi(api_client)

    try:
        # Get knowledge graph insights and analytics
        api_response = api_instance.get_insights()
        print("The response of GraphApi->get_insights:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GraphApi->get_insights: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GraphInsightsResponse**](GraphInsightsResponse.md)

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

# **get_shortest_path**
> ShortestPathResponse get_shortest_path(source, target)

Find shortest path between two notes

Find the shortest directed path between two notes using BFS.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.shortest_path_response import ShortestPathResponse
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
    api_instance = knowledge_sdk.GraphApi(api_client)
    source = 56 # int | Source note ID
    target = 56 # int | Target note ID

    try:
        # Find shortest path between two notes
        api_response = api_instance.get_shortest_path(source, target)
        print("The response of GraphApi->get_shortest_path:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GraphApi->get_shortest_path: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **source** | **int**| Source note ID | 
 **target** | **int**| Target note ID | 

### Return type

[**ShortestPathResponse**](ShortestPathResponse.md)

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

