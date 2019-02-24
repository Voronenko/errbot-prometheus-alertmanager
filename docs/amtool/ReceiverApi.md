# swagger_client.ReceiverApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_receivers**](ReceiverApi.md#get_receivers) | **GET** /receivers | 


# **get_receivers**
> list[Receiver] get_receivers()



Get list of all receivers (name of notification integrations)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ReceiverApi()

try:
    api_response = api_instance.get_receivers()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReceiverApi->get_receivers: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Receiver]**](Receiver.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

