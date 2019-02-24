# swagger_client.GeneralApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_status**](GeneralApi.md#get_status) | **GET** /status | 


# **get_status**
> AlertmanagerStatus get_status()



Get current status of an Alertmanager instance and its cluster

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneralApi()

try:
    api_response = api_instance.get_status()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeneralApi->get_status: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AlertmanagerStatus**](AlertmanagerStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

