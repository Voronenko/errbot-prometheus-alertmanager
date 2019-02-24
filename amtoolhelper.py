from __future__ import print_function
import re
import swagger_client
from swagger_client import Configuration, ApiClient, api, PostableSilence
from swagger_client.rest import ApiException


class AmtoolHelper(object):

    def __init__(self, alertmanager_address):
        self.configuration = Configuration()
        self.configuration.host = alertmanager_address
        api_client = ApiClient(configuration=self.configuration)
        self.general_api = swagger_client.GeneralApi(api_client=api_client)
        self.alerts_api = swagger_client.AlertApi(api_client=api_client)
        self.receiver_api = swagger_client.ReceiverApi(api_client=api_client)
        self.silence_api = swagger_client.SilenceApi(api_client=api_client)

    def get_status(self):
        try:
            api_response = self.general_api.get_status()
            return {
                "cluster": {
                    "name": api_response.cluster.name,
                    "status": api_response.cluster.status,
                    #          "peers": api_response.cluster.peers
                },
                "config": api_response.config.original,
                "uptime": api_response.uptime,
                "version": {
                    "branch": api_response.version_info.branch,
                    "build_date": api_response.version_info.build_date,
                    "version": api_response.version_info.version,
                    "revision": api_response.version_info.revision,

                }
            }
        except ApiException as e:
            print("Exception when calling GeneralApi->get_status: %s\n" % e)
            raise

    #        active = true # bool | Show active alerts (optional) (default to true)
    #        silenced = true # bool | Show silenced alerts (optional) (default to true)
    #        inhibited = true # bool | Show inhibited alerts (optional) (default to true)
    #        unprocessed = true # bool | Show unprocessed alerts (optional) (default to true)
    #        filter = ['filter_example'] # list[str] | A list of matchers to filter alerts by (optional)
    #        receiver = 'receiver_example' # str | A regex matching receivers to filter alerts by (optional)
    def get_alerts(self, active=True, silenced=True, inhibited=True,
        unprocessed=True, filter=[], receiver=""):
        try:
            api_response = self.alerts_api.get_alerts(active=active,
                                                      silenced=silenced,
                                                      inhibited=inhibited,
                                                      unprocessed=unprocessed,
                                                      filter=filter,
                                                      receiver=receiver
                                                      )
            return {
                "count": len(api_response),
                "alerts": api_response,
                "criteria": {
                    "active": active,
                    "silenced": silenced,
                    "inhibited": inhibited,
                    "unprocessed": unprocessed,
                    "filter": filter,
                    "receiver": receiver
                }
            }
        except ApiException as e:
            print("Exception when cal"
                  "ling AlertApi->get_alerts: {}\n".format(e))
            raise

    def get_alert(self, fingerprint):
        alerts = self.alerts_api.get_alerts(active=True,
                                            silenced=True,
                                            inhibited=True,
                                            unprocessed=True,
                                            filter=[],
                                            receiver=""
                                            )
        for alert in alerts:
            if alert["fingerprint"] == fingerprint:
                return alert
        return None

    def get_silences(self, filter=[]):
        try:
            api_response = self.silence_api.get_silences(filter=filter)
            return api_response
        except ApiException as e:
            print("Exception when calling silence_api->get_silences: %s\n" % e)
            raise

    def get_silence(self, silence_id):
        try:
            api_response = self.silence_api.get_silence(silence_id)
            return api_response
        except ApiException as e:
            print("Exception when calling silence_api->get_silence: %s\n" % e)
            raise

    def delete_silence(self, silence_id):
        try:
            api_response = self.silence_api.delete_silence(silence_id)
            return api_response
        except ApiException as e:
            print(
                "Exception when calling silence_api->delete_silence(: %s\n" % e)
            raise

    def post_silence(self, matchers=None, starts_at=None, ends_at=None,
        created_by=None, comment=None):
        try:
            silence = PostableSilence(
                matchers=matchers,
                starts_at=starts_at,
                ends_at=ends_at,
                created_by=created_by,
                comment=comment
            )
            api_response = self.silence_api.post_silences(silence)
            return api_response
        except ApiException as e:
            print("Exception when calling silence_api->post_silence: %s\n" % e)
            raise

    def get_receivers(self):
        try:
            api_response = self.receiver_api.get_receivers()
            return api_response
        except ApiException as e:
            print(
                "Exception when calling receiver_api->get_receivers: %s\n" % e)
            raise

    @staticmethod
    def get_matchers_by_alert(alert, ignore_terms=["severity", "monitor"],
        include_terms=None):
        matchers = []
        for name, value in alert["labels"].items():
            if name in ignore_terms:
                continue
            if include_terms and not name in include_terms:
                continue
            matchers.append(
                {
                    "IsRegex": False,
                    "name": name,
                    "value": value
                }
            )
        return matchers

    @staticmethod
    def get_matchers_by_terms(terms=[], ignore_terms=[], include_terms=None):
        matchers = []
        for term in terms:
            match_regex = False
            elements = term.split("=")
            if len(elements) == 1:
                value = elements[0]
                name = "alertname"
            else:
                name = elements[0]
                value = elements[1]
                if name in ignore_terms:
                    continue
                if include_terms and not name in include_terms:
                    continue
            if value.startswith("~") or "." in value or "*" in value:
                try:
                    re.compile(value)
                    match_regex = True
                except re.error:
                    match_regex = False
            matchers.append(
                {
                    "IsRegex": match_regex,
                    "name": name,
                    "value": value
                }
            )
        return matchers

    @staticmethod
    def get_filters_by_terms(terms=[]):
        matchers = []
        for term in terms:
            elements = term.split("=")
            if len(elements) == 1:
                value = elements[0]
                name = "alertname"
            else:
                name = elements[0]
                value = elements[1]
            matchers.append("{0}={1}".format(name,value))
        return matchers
