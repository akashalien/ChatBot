from flask import Flask, render_template, request, jsonify
import conversation


app = Flask(__name__)
app.config["DEBUG"] = True
conversation.initBrain()


@app.route('/')
def index():
    return render_template('main_page.html')


@app.route('/api/', methods=["GET","POST"])
def api():
    try:
        if request.method == "POST":
            data = request.get_json()
            query = data['query']
            reply = conversation.botAnswer(query)
            # dict can also be used as param for jsonify
            return jsonify(
                response=reply,
                mode="reply"
            )
    except Exception as e:
        return jsonify(
            response="Error: " + str(e)
        )


@app.route('/quote', methods=["GET"])
def quote():
    from apis import quotes
    try:
        return quotes.getQuote()
    except Exception as e:
        return "Error: " + str(e)


@app.route('/test', methods=["GET"])
def test():
    from apis import quotes
    try:
        return "Test Successful!"
    except Exception as e:
        return "Error: " + str(e)


if __name__ == "__main__":
    app.run()