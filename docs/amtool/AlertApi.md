# swagger_client.AlertApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_alerts**](AlertApi.md#get_alerts) | **GET** /alerts | 
[**post_alerts**](AlertApi.md#post_alerts) | **POST** /alerts | 


# **get_alerts**
> GettableAlerts get_alerts(active=active, silenced=silenced, inhibited=inhibited, unprocessed=unprocessed, filter=filter, receiver=receiver)



Get a list of alerts

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AlertApi()
active = true # bool | Show active alerts (optional) (default to true)
silenced = true # bool | Show silenced alerts (optional) (default to true)
inhibited = true # bool | Show inhibited alerts (optional) (default to true)
unprocessed = true # bool | Show unprocessed alerts (optional) (default to true)
filter = ['filter_example'] # list[str] | A list of matchers to filter alerts by (optional)
receiver = 'receiver_example' # str | A regex matching receivers to filter alerts by (optional)

try:
    api_response = api_instance.get_alerts(active=active, silenced=silenced, inhibited=inhibited, unprocessed=unprocessed, filter=filter, receiver=receiver)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlertApi->get_alerts: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **active** | **bool**| Show active alerts | [optional] [default to true]
 **silenced** | **bool**| Show silenced alerts | [optional] [default to true]
 **inhibited** | **bool**| Show inhibited alerts | [optional] [default to true]
 **unprocessed** | **bool**| Show unprocessed alerts | [optional] [default to true]
 **filter** | [**list[str]**](str.md)| A list of matchers to filter alerts by | [optional] 
 **receiver** | **str**| A regex matching receivers to filter alerts by | [optional] 

### Return type

[**GettableAlerts**](GettableAlerts.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_alerts**
> post_alerts(alerts)



Create new Alerts

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AlertApi()
alerts = swagger_client.PostableAlerts() # PostableAlerts | The alerts to create

try:
    api_instance.post_alerts(alerts)
except ApiException as e:
    print("Exception when calling AlertApi->post_alerts: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **alerts** | [**PostableAlerts**](PostableAlerts.md)| The alerts to create | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

