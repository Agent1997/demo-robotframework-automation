from RequestsLibrary.SessionKeywords import SessionKeywords
from jsonpath_ng import parse
from requests import Response

from autocore.api.APIResponse import APIResponse


class APIRequest:

    def __init__(self):
        self.__request = SessionKeywords()
        self.__request_args: dict = {}
        self.__headers: dict = {}
        self.__data: object = None
        self.__url: str = ""
        self.__base_url: str = ""
        self.__endpoint: str = ""
        self.__path_params: dict = {}
        self.__query_params: dict = {}
        self.__cookies: dict = {}
        self.__files: object = None
        self.__json: object = None

    def set_base_url(self, base_url: str):
        self.__base_url = base_url
        return self

    def set_endpoint(self, endpoint: str):
        self.__endpoint = endpoint
        return self

    def set_header(self, key: str, value: object):
        self.__headers[key] = value
        return self

    def set_ws_token(self, token: str):
        self.__headers["wstoken"] = token
        return self

    def set_bearer_token(self, token: str):
        self.__headers["Authorization"] = f"Bearer {token}"
        return self

    def set_cookie(self, key: str, value: object):
        self.__cookies[key] = value
        return self

    def set_data(self, body: object):
        if self.__data is None:
            self.__data = body
        return self

    def set_json(self, body: object):
        if self.__json is None:
            self.__json = body
        return self

    def set_files(self, files: object):
        if self.__files is None:
            self.__files = files
        return self

    def set_path_param(self, path_param: str, value: str):
        self.__path_params[path_param] = value
        return self

    def set_query_param(self, query_param: str, value: str):
        self.__query_params[query_param] = value
        return self

    def __prepare_request_url(self):
        self.__url = f"{self.__base_url}{self.__endpoint}"

        if len(self.__path_params) > 0:
            for key, value in self.__path_params.items():
                path_param = "{" + key + "}"
                if self.__url.__contains__(path_param):
                    self.__url = self.__url.replace(path_param, value)

        if len(self.__query_params) > 0:
            query = "?"
            for key, value in self.__query_params.items():
                query = query + key + "=" + value + "&"

            query = query.removesuffix("&")
            self.__url = self.__url + query

    def __prepare_request_args(self):
        if self.__json is not None:
            self.__request_args['json'] = self.__json

        if self.__data is not None:
            self.__request_args['data'] = self.__data

        if self.__files is not None:
            self.__request_args['files'] = self.__files

        if len(self.__cookies) > 0:
            self.__request_args['cookies'] = self.__cookies

        if len(self.__headers) > 0:
            self.__request_args['headers'] = self.__headers

    def __validate_request_spec(self):
        if len(self.__base_url) == 0:
            raise Exception("Error in Request Specifications. Please provide the base url.")
        if len(self.__endpoint) == 0:
            raise Exception("Error in Request Specifications. Please provide the endpoint.")

    def send_get_request(self) -> APIResponse:
        self.__prepare_request_url()
        self.__prepare_request_args()
        self.__validate_request_spec()

        response: Response
        if len(self.__request_args) > 0:
            response = self.__request.session_less_get(url=self.__url, **self.__request_args)
        else:
            response = self.__request.session_less_get(url=self.__url)
        return APIResponse(response)

    def send_post_request(self):
        self.__prepare_request_url()
        self.__prepare_request_args()
        self.__validate_request_spec()

        response: Response
        if len(self.__request_args) > 0:
            response = self.__request.session_less_post(url=self.__url, **self.__request_args)
        else:
            response = self.__request.session_less_post(url=self.__url)
        return APIResponse(response)

    def send_delete_request(self):
        self.__prepare_request_url()
        self.__prepare_request_args()
        self.__validate_request_spec()

        response: Response
        if len(self.__request_args) > 0:
            response = self.__request.session_less_delete(url=self.__url, **self.__request_args)
        else:
            response = self.__request.session_less_delete(url=self.__url)
        return APIResponse(response)

    def send_patch_request(self):
        self.__prepare_request_url()
        self.__prepare_request_args()
        self.__validate_request_spec()

        response: Response
        if len(self.__request_args) > 0:
            response = self.__request.session_less_patch(url=self.__url, **self.__request_args)
        else:
            response = self.__request.session_less_patch(url=self.__url)
        return APIResponse(response)

    def send_put_request(self):
        self.__prepare_request_url()
        self.__prepare_request_args()
        self.__validate_request_spec()

        response: Response
        if len(self.__request_args) > 0:
            response = self.__request.session_less_put(url=self.__url, **self.__request_args)
        else:
            response = self.__request.session_less_put(url=self.__url)
        return APIResponse(response)
