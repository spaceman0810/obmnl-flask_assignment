# Import libraries
from flask import Flask,request,url_for,redirect,render_template

#Flask: Creating a basic Flask application.. Flask is a micro web framework for Python used to build web applications. It provides tools, libraries, and technologies for developers to build web applications more efficiently. It handles routing, HTTP requests, and responses, among other things.
#request: Accessing form data submitted via POST request. request is a Flask module used to handle incoming HTTP requests in Flask applications. It provides access to request data such as form data, query parameters, files, and headers. Developers use it to extract data sent by the client in a request.
#url_for: Generating URLs for different routes. url_for is a Flask function used for generating URLs for Flask routes. It takes the name of the route function as an argument and returns the corresponding URL. It's useful because it allows you to change URLs in your application without having to manually update them in your code.
#redirect: Redirecting the user to a different route. redirect is a Flask function used to redirect the client's browser to a different URL. It takes a URL as an argument and sends an HTTP redirect response to the client. It's commonly used after form submissions or to direct users to a different page.
#render_template is a function used for rendering an HTML template with dynamic content, which can be used to generate custom error pages with HTML content.

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data: You can assume that the transactions already exist on the interface when it is executed for the first time
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]
#The reason to implement Read before the other functions is to be able to redirect to the page with all transactions every time a new transaction is created, updated, or deleted.
#Therefore, the function to read the existing transactions must exist before the others are implemented.

# Read operation: List all transactions
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

#The parameter transactions=transactions means that the Python variable transactions is being passed to the transactions variable in the template context. Let's break it down:
#"transactions.html" is the name of the HTML template file that Flask will render.
#transactions is the Python variable being passed to the template.
#transactions=transactions is a keyword argument in Python that assigns the value of the Python variable transactions to the template variable also named transactions.
#So, when rendering the template, the transactions variable in the template will have the same value as the Python variable transactions.
#This allows you to pass data from your Python code to the HTML template, making it available for use in the rendered HTML.

# Create operation: Display add transaction form
@app.route("/add", methods=['GET','POST'])
def add_transaction():

#If the request method is POST, use request.form to extract the form data, create a new transaction, append it to the transactions list, and then use redirect and url_for to send the user back to the list of transactions.
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        # Append the new transaction to the list
        transactions.append(transaction)
        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))

 #If the request method is GET, use the render_template function to display an HTML form using a template named form.html. This form will allow users to input data for a new transaction.   
    # Render the form template to display the add transaction form
    return render_template("form.html")
    
# Update operation: Display edit transaction form
@app.route("/edit/<int:transaction_id>", methods=['GET','POST'])
def edit_transaction(transaction_id):
#If the request method is POST, use request.form to get the updated data, find the transaction with the ID that matches transaction_id and modify its data, then redirect the user back to the list of transactions.
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']
        amount = float(request.form['amount'])
        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))

#If the request method is GET, find the transaction with the ID that matches transaction_id and use render_template to display a form pre-populated with the current data of the transaction using a template named edit.html.
    # Find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)


# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
   for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break

    # Redirect to the transactions list page
   return redirect(url_for("get_transactions"))

# Run the Flask app
#python -m flask --app app.py run
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)