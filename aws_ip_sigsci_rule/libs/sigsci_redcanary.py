import requests
import pysigsci

class SigSciApiRedCanary(object):
    """
        RedCanary SigSci Integration
        Note:::
            No Delete methods are present on purpose
            No Overwrite methods are present on purpose

            This reduces risk of doing something stupid!

        Class for Signal Sciences API, Credit given to the open source PySigSci lib,
        as much of the structure was copied. The reason we are not relying on the opensource version
        is the methods were not designed to take site names. For this reason it was much more simple
        to copy over just the components we need, add in new ones, and push forward.
    """
    base_url = "https://dashboard.signalsciences.net/api/"
    api_version = "v0"
    bearer_token = None
    api_user = None
    api_token = None
    headers = dict()
    cookies = None
    corp = None
    site = None

    # endpoints
    ep_auth = "/auth"
    ep_auth_logout = ep_auth + "/logout"
    ep_corps = "/corps"

    def __init__(self, email=None, password=None, api_token=None):
        """
        sigsciapi
        """
        if email is not None and password is not None:
            self.auth(email, password)
        elif email is not None and api_token is not None:
            self.api_user = email
            self.api_token = api_token

    def _make_request(self,
                      endpoint,
                      params=None,
                      data=None,
                      json=None,
                      method="GET"):
        headers = self.headers
        cookies = None

        if endpoint != self.ep_auth and self.bearer_token is not None:
            headers["Authorization"] = "Bearer {}".format(self.bearer_token['token'])
        elif endpoint != self.ep_auth:
            headers["X-Api-User"] = self.api_user
            headers['X-Api-Token'] = self.api_token

        headers["Content-Type"] = "application/json"
        headers['User-Agent'] = 'pysigsci v' + pysigsci.VERSION

        if self.cookies is not None:
            cookies = self.cookies

        url = self.base_url + self.api_version + endpoint

        result = None
        if method == "GET":
            result = requests.get(url, params=params, headers=headers, cookies=cookies)
        elif method == "POST":
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            result = requests.post(url, data=data, headers=headers, cookies=cookies)
        elif method == "POST_JSON":
            headers["Content-Type"] = "application/json"
            result = requests.post(url, json=json, headers=headers, cookies=cookies)
        elif method == "PUT":
            headers["Content-Type"] = "application/json"
            result = requests.put(url, json=json, headers=headers, cookies=cookies)
        elif method == "PATCH":
            headers["Content-Type"] = "application/json"
            result = requests.patch(url, json=json, headers=headers, cookies=cookies)
        elif method == "DELETE":
            headers["Content-Type"] = "application/json"
            result = requests.delete(url, params=params, headers=headers, cookies=cookies)
        else:
            raise Exception("InvalidRequestMethod: " + str(method))

        if result.status_code == 204:
            return dict({'message': '{} {}'.format(method, 'successful.')})

        if result.status_code == 400:
            raise Exception('400 Bad Request: {}'.format(result.json()['message']))

        return result.json()

    # Auth
    def auth(self, email, password):
        """
        Log into the API
        https://docs.signalsciences.net/api/#_auth_post
        POST /auth
        """
        data = {"email": email, "password": password}
        self.bearer_token = self._make_request(
            endpoint=self.ep_auth,
            data=data,
            method="POST")
        return True

    # CORPS
    def get_corps(self):
        """
        List corps
        https://docs.signalsciences.net/api/#_corps_get
        GET /corps/
        """
        return self._make_request(endpoint=self.ep_corps)

    # GET AGENT KEYS
    def get_agent_keys(self, site_name):
        """
        List agent Keys
        GET /corps/{corpName}/sites/{siteName}/agentKeys
        :return:
        """

        endpoint = "{}/{}/sites/{}/agentKeys".format(self.ep_corps,
                                                         self.corp,
                                                         site_name)

        return self._make_request(endpoint)

    #CREATE SITE
    def create_corp_site(self, data):
        """
        Create site in corp
        https://docs.signalsciences.net/api/#_corps__corpName__sites_post
        POST /corps/{corpName}/sites
        """
        return self._make_request(
            endpoint="{}/{}/sites".format(self.ep_corps,
                                          self.corp),
            json=data,
            method="POST_JSON")

    #Get Site Signals
    def get_site_signals(self, site_name):
        """
        Get Site Signals
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/tags
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/tags".format(self.ep_corps,
                                                  self.corp,
                                                  site_name))

    # Put Site Signals
    def add_site_signals(self, data, site_name):
        """
        Add custom signal
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        POST /corps/{corpName}/sites/{siteName}/tags
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/tags".format(
                self.ep_corps, self.corp, site_name),
            json=data,
            method="POST_JSON")

    #Put Site Rules
    def add_site_rules(self, data, site_name):
        """
        Create site rule
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__rules_post
        POST /corps/{corpName}/sites/{siteName}/rules
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/rules".format(self.ep_corps,
                                                   self.corp,
                                                   site_name),
            json=data,
            method="POST_JSON")

    #Add Site Integration
    def add_integration(self, data, site_name):
        """
        Add to integrations
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__integrations_post
        POST /corps/{corpName}/sites/{siteName}/integrations
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/integrations".format(
                self.ep_corps, self.corp, site_name),
            json=data,
            method="POST_JSON")

    # SITES
    def get_corp_sites(self):
        """
        List sites in corp
        https://docs.signalsciences.net/api/#_corps__corpName__sites_get
        GET /corps/{corpName}/sites
        """
        return self._make_request(
            endpoint="{}/{}/sites".format(self.ep_corps, self.corp))

    # GET SITE SIGNALS
    def get_site_signals(self, site_name):
        """
        Get Site Signals
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/tags
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/tags".format(self.ep_corps,
                                                  self.corp,
                                                  site_name))

    #GET SITE RULES
    def get_site_rules(self, site_name, rule_type=""):
        """
        List rules in site
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__rules_get
        GET /corps/{corpName}/sites/{siteName}/rules
        """
        type_parameter = ""
        if rule_type in ['request', 'signal', 'rateLimit']:
            type_parameter = "?type={}".format(rule_type)

        return self._make_request(
            endpoint="{}/{}/sites/{}/rules{}".format(self.ep_corps,
                                                     self.corp,
                                                     site_name,
                                                     type_parameter))



    #TEMPLATED RULES
    def get_templated_rules(self, site_name):
        """
        Get Templated Rules
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/configuredtemplates
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/configuredtemplates".format(self.ep_corps,
                                                             self.corp,
                                                             site_name))

    def update_templated_rule(self, site_name, template_id, data):
        """
        Get Templated Rules
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        POST /corps/{corpName}/sites/{siteName}/configuredtemplates/{id}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/configuredtemplates/{}".format(self.ep_corps, self.corp, site_name, template_id),
            json=data,
            method="POST_JSON"
        )

    #Site Alerts
    def add_site_alert(self, data, site_name):
        """
        Create site alert
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__alerts_post
        POST /corps/{corpName}/sites/{siteName}/alerts
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/alerts".format(
                self.ep_corps, self.corp, site_name),
            json=data,
            method="POST_JSON")

    def get_site_alerts(self,site_name):
        """
        List site alerts
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__alerts_get
        GET /corps/{corpName}/sites/{siteName}/alerts
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/alerts".format(self.ep_corps,
                                                    self.corp,
                                                    site_name))

    def get_site_members(self,site_name):
        """
        List site members
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__members_get
        GET /corps/{corpName}/sites/{siteName}/members
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/members".format(self.ep_corps,
                                                     self.corp,
                                                     site_name))

    def add_members_to_site(self, data, site_name):
        """
        Add members to site
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__members_post
        POST /corps/{corpName}/sites/{siteName}/members
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/members".format(self.ep_corps,
                                                     self.corp,
                                                     site_name),
            json=data,
            method="POST_JSON")

    def delete_site_member(self, email, site_name):
        """
        Delete from site members
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__members__siteMemberEmail__delete
        DELETE /corps/{corpName}/sites/{siteName}/members/{siteMemberEmail}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/members/{}".format(
                self.ep_corps, self.corp, site_name, email),
            method="DELETE")

    def add_site_member(self, email, data, site_name):
        """
        Invite a site member
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__members__siteMemberEmail__invite_post
        POST /corps/{corpName}/sites/{siteName}/members/{siteMemberEmail}/invite
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/members/{}/invite".format(self.ep_corps,
                                                               self.corp,
                                                               site_name,
                                                               email),
            json=data,
            method="POST_JSON")

    # CORP/SITE LISTS
    def get_site_rule_lists(self, site_name):
        """
        Get Rule Lists
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__lists_get
        GET /corps/{corpName}/sites/{siteName}/lists
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/lists".format(self.ep_corps,
                                                   self.corp,
                                                   site_name))

    def get_site_rule_list(self, identifier, site_name):
        """
        Get Rule List by ID
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__lists__id__get
        GET /corps/{corpName}/sites/{siteName}/lists/{id}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/lists/{}".format(self.ep_corps,
                                                      self.corp,
                                                      site_name,
                                                      identifier))

    def add_site_rule_lists(self, data, site_name):
        """
        Add Site Rule Lists
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__lists_post
        POST /corps/{corpName}/sites/{siteName}/lists
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/lists".format(self.ep_corps,
                                                   self.corp,
                                                   site_name),
            json=data,
            method="POST_JSON")

    def update_site_rule_lists(self, identifier, data, site_name):
        """
        Update a site list by ID
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__lists__id__patch
        PATCH /corps/{corpName}/sites/{siteName}/lists/{id}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/lists/{}".format(
                self.ep_corps, self.corp, site_name, identifier),
            json=data,
            method="PUT")