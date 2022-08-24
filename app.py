import logging
import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from server import serve_app

from todo import layout

def create_dash():
    app = dash.Dash( __name__,
        prevent_initial_callbacks=True,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP])
    return app


def create_app(dash_factory) -> Dash:
    app = dash_factory()
    def _layout():
        return html.Div([
            html.Div([
                html.Div([
                    html.Div([], className="col-md-1"),
                    html.Div(layout, id='page-content', className="col-md-10"),
                    html.Div([], className="col-md-1")
                ], className='row')
            ], className="container-fluid"),
        ])

    app.layout = _layout()
    return app


if __name__ == "__main__":

    logging.basicConfig(format = '%(levelname)s %(module)13s/%(lineno)-5d %(message)s')

    app = create_app(create_dash)

    # Turn off werkzeug logging as it's very noisy

    _log = logging.getLogger('werkzeug')
    _log.setLevel(logging.ERROR)

    log = logging.getLogger('redux_store')
    log.setLevel(logging.WARN)
    serve_app(app, debug=False)
