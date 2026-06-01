import dash
import dash_html_components as html

external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.Button(
            [
                  # Icon from Font Awesome
                # "Submit",
                # html.I(className="question-circle-fill"),
            ],
            id="submit-button",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

