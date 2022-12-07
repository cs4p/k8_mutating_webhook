from flask import request, jsonify, Blueprint
import base64
import jsonpatch

admission_controller = Blueprint('mutate', __name__, url_prefix='/mutate')


# a simple page that says hello
@admission_controller.route('/hello')
def hello():
    return 'Hello from the %s app!' % admission_controller.name


@admission_controller.route('/deployments', methods=['POST'])
def deployment_webhook_mutate():
    # Variable is unused here but in theory you might wnat to check something before making changes...
    # request_info = request.get_json()
    return admission_response_patch(True, "Adding allow label", json_patch=jsonpatch.JsonPatch(
        [{"op": "add", "path": "/metadata/labels/allow", "value": "yes"}]))


def admission_response_patch(allowed, message, json_patch):
    base64_patch = base64.b64encode(json_patch.to_string().encode("utf-8")).decode("utf-8")
    return jsonify({"response": {"allowed": allowed,
                                 "status": {"message": message},
                                 "patchType": "JSONPatch",
                                 "patch": base64_patch}})
