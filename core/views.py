from django.core.exceptions import PermissionDenied
from revproxy.views import ProxyView
from revproxy.response import get_django_response

from waf.settings import UPSTREAM
from .models import Policy
import re


class TestProxyView(ProxyView):
    upstream = UPSTREAM

    def get_policy_variable(self, policy: Policy) -> str:
        if policy.variable == "host":
            return self.get_request_headers().get("host")
        elif policy.variable == "headers":
            if policy.selector:
                return self.get_request_headers().get(policy.selector)
            return self.get_request_headers()
        elif policy.variable == "body":
            return self.request.body

    def check_policy(self, policy: Policy) -> bool:
        variable = self.get_policy_variable(policy)

        operator_actions = {
            "contains": lambda x, y: y in x,
            "equals": lambda x, y: x == y,
            "starts-with": lambda x, y: x.startswith(y),
            "ends-with": lambda x, y: x.endswith(y),
            "matches": lambda x, y: re.match(y, x),
        }

        operation = operator_actions.get(policy.operator)

        return operation(variable, policy.value) if operation else False

    def handle_policy(self, policy: Policy):
        action_handlers = {
            "block": lambda: self.block_request(),
            "alert": lambda: self.alert_request(policy),
            "log": lambda: self.log_request(policy),
        }
        return action_handlers.get(policy.action)()

    def block_request(self):
        raise PermissionDenied()

    def alert_request(self, policy: Policy):
        print("ALERT: %s" % policy)

    def log_request(self, policy: Policy):
        print("LOG: %s" % policy)

    def handle_request(self):
        active_policies = Policy.objects.filter(is_active=True)
        for policy in active_policies:
            if self.check_policy(policy):
                return self.handle_policy(policy)

    def dispatch(self, request, path):
        self.request_headers = self.get_request_headers()

        redirect_to = self._format_path_to_redirect(request)
        if redirect_to:
            return redirect(redirect_to)

        proxy_response = self._created_proxy_response(request, path)

        self._replace_host_on_redirect_location(request, proxy_response)
        self._set_content_type(request, proxy_response)

        self.handle_request()

        response = get_django_response(
            proxy_response,
            strict_cookies=self.strict_cookies,
            streaming_amount=self.streaming_amount,
        )

        print("RESPONSE RETURNED: %s", response)
        return response
