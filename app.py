from flask import Flask, request, jsonify
import base64
import jsonpatch

admission_controller = Flask(__name__)


@admission_controller.route('/validate/deployments', methods=['POST'])
def deployment_webhook():
    request_info = request.get_json()
    if request_info["request"]["object"]["metadata"]["labels"].get("allow"):
        return admission_response(True, "Allow label exists")
    return admission_response(False, "Not allowed without allow label")


@admission_controller.route('/mutate/deployments', methods=['POST'])
def deployment_webhook_mutate():
    request_info = request.get_json()
    return admission_response_patch(True, "Adding allow label", json_patch = jsonpatch.JsonPatch([{"op": "add", "path": "/metadata/labels/allow", "value": "yes"}]))
def admission_response_patch(allowed, message, json_patch):
    base64_patch = base64.b64encode(json_patch.to_string().encode("utf-8")).decode("utf-8")
    return jsonify({"response": {"allowed": allowed,
                                 "status": {"message": message},
                                 "patchType": "JSONPatch",
                                 "patch": base64_patch}})


def admission_response(allowed, message):
    return jsonify({"response": {"allowed": allowed, "status": {"message": message}}})


if __name__ == '__main__':
    admission_controller.run(host='0.0.0.0', port=443, ssl_context=("/server.crt", "/server.key"))
