# swagger_client.ScanEngineApi

All URIs are relative to *https://localhost:3780*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_scan_engine_pool_scan_engine**](ScanEngineApi.md#add_scan_engine_pool_scan_engine) | **PUT** /api/3/scan_engine_pools/{id}/engines/{engineId} | Engine Pool Engines
[**create_scan_engine**](ScanEngineApi.md#create_scan_engine) | **POST** /api/3/scan_engines | Scan Engines
[**create_scan_engine_pool**](ScanEngineApi.md#create_scan_engine_pool) | **POST** /api/3/scan_engine_pools | Engine Pools
[**create_shared_secret**](ScanEngineApi.md#create_shared_secret) | **POST** /api/3/scan_engines/shared_secret | Scan Engine Shared Secret
[**delete_scan_engine**](ScanEngineApi.md#delete_scan_engine) | **DELETE** /api/3/scan_engines/{id} | Scan Engine
[**delete_shared_secret**](ScanEngineApi.md#delete_shared_secret) | **DELETE** /api/3/scan_engines/shared_secret | Scan Engine Shared Secret
[**get_assigned_engine_pools**](ScanEngineApi.md#get_assigned_engine_pools) | **GET** /api/3/scan_engines/{id}/scan_engine_pools | Assigned Engine Pools
[**get_current_shared_secret**](ScanEngineApi.md#get_current_shared_secret) | **GET** /api/3/scan_engines/shared_secret | Scan Engine Shared Secret
[**get_current_shared_secret_time_to_live**](ScanEngineApi.md#get_current_shared_secret_time_to_live) | **GET** /api/3/scan_engines/shared_secret/time_to_live | Scan Engine Shared Secret Time to live
[**get_engine_pool**](ScanEngineApi.md#get_engine_pool) | **GET** /api/3/scan_engine_pools/{id} | Engine Pool
[**get_scan_engine**](ScanEngineApi.md#get_scan_engine) | **GET** /api/3/scan_engines/{id} | Scan Engine
[**get_scan_engine_pool_scan_engines**](ScanEngineApi.md#get_scan_engine_pool_scan_engines) | **GET** /api/3/scan_engine_pools/{id}/engines | Engine Pool Engines
[**get_scan_engine_pool_sites**](ScanEngineApi.md#get_scan_engine_pool_sites) | **GET** /api/3/scan_engine_pools/{id}/sites | Engine Pool Sites
[**get_scan_engine_pools**](ScanEngineApi.md#get_scan_engine_pools) | **GET** /api/3/scan_engine_pools | Engine Pools
[**get_scan_engine_scans**](ScanEngineApi.md#get_scan_engine_scans) | **GET** /api/3/scan_engines/{id}/scans | Scan Engine Scans
[**get_scan_engine_sites**](ScanEngineApi.md#get_scan_engine_sites) | **GET** /api/3/scan_engines/{id}/sites | Scan Engine Sites
[**get_scan_engines**](ScanEngineApi.md#get_scan_engines) | **GET** /api/3/scan_engines | Scan Engines
[**remove_scan_engine_pool**](ScanEngineApi.md#remove_scan_engine_pool) | **DELETE** /api/3/scan_engine_pools/{id} | Engine Pool
[**remove_scan_engine_pool_scan_engine**](ScanEngineApi.md#remove_scan_engine_pool_scan_engine) | **DELETE** /api/3/scan_engine_pools/{id}/engines/{engineId} | Engine Pool Engines
[**set_scan_engine_pool_scan_engines**](ScanEngineApi.md#set_scan_engine_pool_scan_engines) | **PUT** /api/3/scan_engine_pools/{id}/engines | Engine Pool Engines
[**update_scan_engine**](ScanEngineApi.md#update_scan_engine) | **PUT** /api/3/scan_engines/{id} | Scan Engine
[**update_scan_engine_pool**](ScanEngineApi.md#update_scan_engine_pool) | **PUT** /api/3/scan_engine_pools/{id} | Engine Pool


# **add_scan_engine_pool_scan_engine**
> Links add_scan_engine_pool_scan_engine(id, engine_id)

Engine Pool Engines

Add an engine to the engine pool.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the engine pool.
engine_id = 56 # int | The identifier of the scan engine.

try:
    # Engine Pool Engines
    api_response = api_instance.add_scan_engine_pool_scan_engine(id, engine_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->add_scan_engine_pool_scan_engine: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the engine pool. | 
 **engine_id** | **int**| The identifier of the scan engine. | 

### Return type

[**Links**](Links.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_scan_engine**
> ReferenceWithEngineIDLink create_scan_engine(scan_engine=scan_engine)

Scan Engines

Creates a new scan engine.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
scan_engine = swagger_client.ScanEngine() # ScanEngine | The specification of a scan engine. (optional)

try:
    # Scan Engines
    api_response = api_instance.create_scan_engine(scan_engine=scan_engine)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->create_scan_engine: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scan_engine** | [**ScanEngine**](ScanEngine.md)| The specification of a scan engine. | [optional] 

### Return type

[**ReferenceWithEngineIDLink**](ReferenceWithEngineIDLink.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_scan_engine_pool**
> CreatedReferenceEngineIDLink create_scan_engine_pool(engine_pool=engine_pool)

Engine Pools

Creates a new engine pool.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
engine_pool = swagger_client.EnginePool() # EnginePool | The details for the scan engine to update. (optional)

try:
    # Engine Pools
    api_response = api_instance.create_scan_engine_pool(engine_pool=engine_pool)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->create_scan_engine_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **engine_pool** | [**EnginePool**](EnginePool.md)| The details for the scan engine to update. | [optional] 

### Return type

[**CreatedReferenceEngineIDLink**](CreatedReferenceEngineIDLink.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_shared_secret**
> str create_shared_secret()

Scan Engine Shared Secret

Returns the current valid shared secret or generates a new shared secret. The endpoint returns an existing shared secret if one was previously generated and it has not yet expired. Conversely, the endpoint will generate and return a new shared secret for either of the following conditions: a shared secret was not previously generated or the previously-generated shared secret has expired. The shared secret is valid for 60 minutes from the moment it is generated.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()

try:
    # Scan Engine Shared Secret
    api_response = api_instance.create_shared_secret()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->create_shared_secret: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_scan_engine**
> Links delete_scan_engine(id)

Scan Engine

Deletes the specified scan engine.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the scan engine.

try:
    # Scan Engine
    api_response = api_instance.delete_scan_engine(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->delete_scan_engine: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the scan engine. | 

### Return type

[**Links**](Links.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_shared_secret**
> Links delete_shared_secret()

Scan Engine Shared Secret

Revokes the current valid shared secret, if one exists.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()

try:
    # Scan Engine Shared Secret
    api_response = api_instance.delete_shared_secret()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->delete_shared_secret: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Links**](Links.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_assigned_engine_pools**
> ResourcesEnginePool get_assigned_engine_pools(id)

Assigned Engine Pools

Retrieves the list of engine pools the scan engine is currently assigned to.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the scan engine.

try:
    # Assigned Engine Pools
    api_response = api_instance.get_assigned_engine_pools(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->get_assigned_engine_pools: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the scan engine. | 

### Return type

[**ResourcesEnginePool**](ResourcesEnginePool.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_current_shared_secret**
> str get_current_shared_secret()

Scan Engine Shared Secret

Returns the current valid shared secret, if one has been previously generated and it has not yet expired; otherwise the endpoint will respond with a 404 status code. Use this endpoint to detect whether a previously-generated shared secret is still valid.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()

try:
    # Scan Engine Shared Secret
    api_response = api_instance.get_current_shared_secret()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->get_current_shared_secret: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_current_shared_secret_time_to_live**
> int get_current_shared_secret_time_to_live()

Scan Engine Shared Secret Time to live

Returns the number of seconds remaining for the current shared secret before it expires, if one has been previously generated and it has not yet expired; otherwise the endpoint will respond with a 404 status code.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()

try:
    # Scan Engine Shared Secret Time to live
    api_response = api_instance.get_current_shared_secret_time_to_live()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->get_current_shared_secret_time_to_live: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**int**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_engine_pool**
> EnginePool get_engine_pool(id)

Engine Pool

Retrieves the details for an engine pool.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the engine pool.

try:
    # Engine Pool
    api_response = api_instance.get_engine_pool(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->get_engine_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the engine pool. | 

### Return type

[**EnginePool**](EnginePool.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scan_engine**
> ScanEngine get_scan_engine(id)

Scan Engine

Retrieves the details for a scan engine.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the scan engine.

try:
    # Scan Engine
    api_response = api_instance.get_scan_engine(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->get_scan_engine: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the scan engine. | 

### Return type

[**ScanEngine**](ScanEngine.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scan_engine_pool_scan_engines**
> ReferencesWithEngineIDLink get_scan_engine_pool_scan_engines(id)

Engine Pool Engines

Get the engines in the engine pool.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the engine pool.

try:
    # Engine Pool Engines
    api_response = api_instance.get_scan_engine_pool_scan_engines(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->get_scan_engine_pool_scan_engines: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the engine pool. | 

### Return type

[**ReferencesWithEngineIDLink**](ReferencesWithEngineIDLink.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scan_engine_pool_sites**
> ReferencesWithSiteIDLink get_scan_engine_pool_sites(id)

Engine Pool Sites

Returns links to the sites associated with this engine pool.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the engine pool.

try:
    # Engine Pool Sites
    api_response = api_instance.get_scan_engine_pool_sites(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->get_scan_engine_pool_sites: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the engine pool. | 

### Return type

[**ReferencesWithSiteIDLink**](ReferencesWithSiteIDLink.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scan_engine_pools**
> ResourcesEnginePool get_scan_engine_pools()

Engine Pools

Returns engine pools available to use for scanning.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()

try:
    # Engine Pools
    api_response = api_instance.get_scan_engine_pools()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->get_scan_engine_pools: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ResourcesEnginePool**](ResourcesEnginePool.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scan_engine_scans**
> PageOfScan get_scan_engine_scans(id, page=page, size=size, sort=sort)

Scan Engine Scans

Returns the scans that have been run on a scan engine.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the scan engine.
page = 0 # int | The index of the page (zero-based) to retrieve. (optional) (default to 0)
size = 10 # int | The number of records per page to retrieve. (optional) (default to 10)
sort = ['sort_example'] # list[str] | The criteria to sort the records by, in the format: `property[,ASC|DESC]`. The default sort order is ascending. Multiple sort criteria can be specified using multiple sort query parameters. (optional)

try:
    # Scan Engine Scans
    api_response = api_instance.get_scan_engine_scans(id, page=page, size=size, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->get_scan_engine_scans: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the scan engine. | 
 **page** | **int**| The index of the page (zero-based) to retrieve. | [optional] [default to 0]
 **size** | **int**| The number of records per page to retrieve. | [optional] [default to 10]
 **sort** | [**list[str]**](str.md)| The criteria to sort the records by, in the format: &#x60;property[,ASC|DESC]&#x60;. The default sort order is ascending. Multiple sort criteria can be specified using multiple sort query parameters. | [optional] 

### Return type

[**PageOfScan**](PageOfScan.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scan_engine_sites**
> PageOfSite get_scan_engine_sites(id, page=page, size=size, sort=sort)

Scan Engine Sites

Retrieves the list of sites the specified scan engine is assigned to.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the scan engine.
page = 0 # int | The index of the page (zero-based) to retrieve. (optional) (default to 0)
size = 10 # int | The number of records per page to retrieve. (optional) (default to 10)
sort = ['sort_example'] # list[str] | The criteria to sort the records by, in the format: `property[,ASC|DESC]`. The default sort order is ascending. Multiple sort criteria can be specified using multiple sort query parameters. (optional)

try:
    # Scan Engine Sites
    api_response = api_instance.get_scan_engine_sites(id, page=page, size=size, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->get_scan_engine_sites: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the scan engine. | 
 **page** | **int**| The index of the page (zero-based) to retrieve. | [optional] [default to 0]
 **size** | **int**| The number of records per page to retrieve. | [optional] [default to 10]
 **sort** | [**list[str]**](str.md)| The criteria to sort the records by, in the format: &#x60;property[,ASC|DESC]&#x60;. The default sort order is ascending. Multiple sort criteria can be specified using multiple sort query parameters. | [optional] 

### Return type

[**PageOfSite**](PageOfSite.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scan_engines**
> ResourcesScanEngine get_scan_engines()

Scan Engines

Returns scan engines available to use for scanning.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()

try:
    # Scan Engines
    api_response = api_instance.get_scan_engines()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->get_scan_engines: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ResourcesScanEngine**](ResourcesScanEngine.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_scan_engine_pool**
> Links remove_scan_engine_pool(id)

Engine Pool

Deletes the specified engine pool.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the engine pool.

try:
    # Engine Pool
    api_response = api_instance.remove_scan_engine_pool(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->remove_scan_engine_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the engine pool. | 

### Return type

[**Links**](Links.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_scan_engine_pool_scan_engine**
> Links remove_scan_engine_pool_scan_engine(id, engine_id)

Engine Pool Engines

Remove the specified engine from the engine pool.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the engine pool.
engine_id = 56 # int | The identifier of the scan engine.

try:
    # Engine Pool Engines
    api_response = api_instance.remove_scan_engine_pool_scan_engine(id, engine_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->remove_scan_engine_pool_scan_engine: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the engine pool. | 
 **engine_id** | **int**| The identifier of the scan engine. | 

### Return type

[**Links**](Links.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_scan_engine_pool_scan_engines**
> Links set_scan_engine_pool_scan_engines(id, engines=engines)

Engine Pool Engines

Set the engines in the engine pool.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the engine pool.
engines = [swagger_client.list[int]()] # list[int] | The identifiers of the scan engines to place into the engine pool. (optional)

try:
    # Engine Pool Engines
    api_response = api_instance.set_scan_engine_pool_scan_engines(id, engines=engines)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->set_scan_engine_pool_scan_engines: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the engine pool. | 
 **engines** | **list[int]**| The identifiers of the scan engines to place into the engine pool. | [optional] 

### Return type

[**Links**](Links.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_scan_engine**
> Links update_scan_engine(id, scan_engine=scan_engine)

Scan Engine

Updates the specified scan engine.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the scan engine.
scan_engine = swagger_client.ScanEngine() # ScanEngine | The specification of the scan engine to update. (optional)

try:
    # Scan Engine
    api_response = api_instance.update_scan_engine(id, scan_engine=scan_engine)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->update_scan_engine: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the scan engine. | 
 **scan_engine** | [**ScanEngine**](ScanEngine.md)| The specification of the scan engine to update. | [optional] 

### Return type

[**Links**](Links.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_scan_engine_pool**
> Links update_scan_engine_pool(id, engine_pool=engine_pool)

Engine Pool

Updates the specified engine pool.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ScanEngineApi()
id = 56 # int | The identifier of the engine pool.
engine_pool = swagger_client.EnginePool() # EnginePool | The details for the scan engine to update. (optional)

try:
    # Engine Pool
    api_response = api_instance.update_scan_engine_pool(id, engine_pool=engine_pool)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScanEngineApi->update_scan_engine_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The identifier of the engine pool. | 
 **engine_pool** | [**EnginePool**](EnginePool.md)| The details for the scan engine to update. | [optional] 

### Return type

[**Links**](Links.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json;charset=UTF-8

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

