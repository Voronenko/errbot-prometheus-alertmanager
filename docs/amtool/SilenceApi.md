# swagger_client.SilenceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_silence**](SilenceApi.md#delete_silence) | **DELETE** /silence/{silenceID} | 
[**get_silence**](SilenceApi.md#get_silence) | **GET** /silence/{silenceID} | 
[**get_silences**](SilenceApi.md#get_silences) | **GET** /silences | 
[**post_silences**](SilenceApi.md#post_silences) | **POST** /silences | 


# **delete_silence**
> delete_silence(silence_id)



Delete a silence by its ID

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SilenceApi()
silence_id = 'silence_id_example' # str | ID of the silence to get

try:
    api_instance.delete_silence(silence_id)
except ApiException as e:
    print("Exception when calling SilenceApi->delete_silence: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **silence_id** | [**str**](.md)| ID of the silence to get | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_silence**
> GettableSilence get_silence(silence_id)



Get a silence by its ID

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SilenceApi()
silence_id = 'silence_id_example' # str | ID of the silence to get

try:
    api_response = api_instance.get_silence(silence_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SilenceApi->get_silence: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **silence_id** | [**str**](.md)| ID of the silence to get | 

### Return type

[**GettableSilence**](GettableSilence.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_silences**
> GettableSilences get_silences(filter=filter)



Get a list of silences

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SilenceApi()
filter = ['filter_example'] # list[str] | A list of matchers to filter silences by (optional)

try:
    api_response = api_instance.get_silences(filter=filter)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SilenceApi->get_silences: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | [**list[str]**](str.md)| A list of matchers to filter silences by | [optional] 

### Return type

[**GettableSilences**](GettableSilences.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_silences**
> InlineResponse200 post_silences(silence)



Post a new silence or update an existing one

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SilenceApi()
silence = swagger_client.PostableSilence() # PostableSilence | The silence to create

try:
    api_response = api_instance.post_silences(silence)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SilenceApi->post_silences: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **silence** | [**PostableSilence**](PostableSilence.md)| The silence to create | 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

