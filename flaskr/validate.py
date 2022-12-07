from flask import request, jsonify, Blueprint

admission_controller = Blueprint('validate', __name__, url_prefix='/validate')


# a simple page that says hello
@admission_controller.route('/hello')
def hello():
    return 'Hello from the %s app!' % admission_controller.name


@admission_controller.route('/deployments', methods=['POST'])
def deployment_webhook():
    request_info = request.get_json()
    if request_info["request"]["object"]["metadata"]["labels"].get("allow"):
        return admission_response(True, "Allow label exists")
    return admission_response(False, "Not allowed without allow label")


def admission_response(allowed, message):
    return jsonify({"response": {"allowed": allowed, "status": {"message": message}}})
