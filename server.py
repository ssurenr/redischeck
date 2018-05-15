from rediscluster import StrictRedisCluster
from flask import Flask, render_template, request, jsonify, json
import os
import timeit

app = Flask(__name__)
port = int(os.getenv("PORT", 9099))
redis_cluster_host = os.getenv("")

# Test if app running in local or hosted environment
# Should be replaced with more realistic test

if port == 9099:
    startup_nodes = [{"host": "localhost", "port": "6379"}]
else:
    paas_properties = json.loads(os.getenv("PAAS_PROPERTIES"))
    redis_cluster_endpoint = paas_properties["product"]["v1"]["services"]["redis"]["cluster"]["endpoint"]
    startup_nodes = [{"host": redis_cluster_endpoint, "port": "6379"}]

rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
rc_nondecoded = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=False)


@app.route("/", methods=["GET"])
def frontpage():
    return render_template('index.html', redis_server_address=startup_nodes[0]["host"])


@app.route("/api/fk", methods=["POST"])
def fetch_key():
    keyFound = False
    elapsed = 0
    value = ""

    if request.method == "POST":
        key = request.form["fetchkey"]
        # value = "VAL"
        # return jsonify({"value": value, "time": elapsed})
        app.logger.debug("Got Key:" + key)

        if rc.exists(key):
            start_time = timeit.default_timer()
            value = rc.get(key)
            elapsed = timeit.default_timer() - start_time
            keyFound = True

        return jsonify({"found": keyFound, "value": value, "time": str(elapsed * 1000) + " ms"})


@app.route("/api/pt", methods=["POST"])
def performance_test():
    # Note: decode_responses must be set to True when used with python3
    payload = ("Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium," 
               "totamrem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta"
               "sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia"
               "consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est,"
               "qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi"
               "tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis"
               "nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur?"
               "Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur,"
               "vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?")
    ops_count = 10000
    start_time = timeit.default_timer()
    for count in range(ops_count):
        str_count = str(count)
        rc.set("foo" + str_count, payload)
    elapsed = timeit.default_timer() - start_time

    for count in range(ops_count):
        rc.delete("foo" + str(count))

    print("Elapsed Time: {0} s".format(elapsed))
    print("Average Time: {0} us".format(elapsed / ops_count * 1000000))

    return jsonify(
        {
            "Payload": payload,
            "Operation Count": ops_count,
            "Elapsed Time": "{0} s".format(elapsed),
            "Average Time": "{0} us".format(elapsed / ops_count * 1000000)
        }
    )


@app.route("/api/sl", methods=["GET"])
def slowlog():
    slow_log = str(rc_nondecoded.slowlog_get())
    return jsonify(slow_log)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)

# # Note: decode_responses must be set to True when used with python3
# rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
