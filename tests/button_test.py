import dash
from dash import html, ALL, callback
from dash_prefix import prefix, trigger_index, match
from dash_prefix.dash_prefix import NOUPDATE

from dash_redux import ReduxStore

def test_buttons(dash_duo):

    BUTTON_TEST ='Button Test'

    app = dash.Dash(__name__)

    pfx = prefix("redux_test")

    store = ReduxStore(id=pfx('store'), data={})
    btn1 = html.Button("Button1", id=pfx('btn1'))
    btn2 = html.Button("Button2", id=pfx("btn2"))
    container = html.Div(BUTTON_TEST, id=pfx('container'))

    @store.update(btn1.input.n_clicks)
    def btn1_update(clicks, store):
        if clicks:
            if 'btn1' in store:
                store['btn1'] += 1
            else:
                store['btn1'] = 1
        return store


    @store.update(btn2.input.n_clicks)
    def btn2_update(clicks, store):
        if clicks:
            if 'btn2' in store:
                store['btn2'] += 1
            else:
                store['btn2'] = 1
        return store


    @callback(container.output.children, store.store.input.data)
    def btn2_update(store):
        if store:
            msg = ""
            if store and 'btn1' in store:
                msg += f"Button 1 pressed {store['btn1']} times! "

            if store and 'btn2' in store:
                msg += f"Button 2 pressed {store['btn2']} times! "

            return msg.strip()
        else:
            return NOUPDATE

    app.layout = html.Div([store, btn1, btn2, container])

    dash_duo.start_server(app)

    def wait_text(text):
        return dash_duo.wait_for_text_to_equal(container.css_id, text, timeout=4)

    dash_duo.wait_for_text_to_equal(container.css_id, BUTTON_TEST, timeout=4)

    _container = dash_duo.find_element(container.css_id)
    _btn1 = dash_duo.find_element(btn1.css_id)
    _btn2 = dash_duo.find_element(btn2.css_id)

    assert _container.text == BUTTON_TEST

    _btn1.click()
    assert wait_text("Button 1 pressed 1 times!")

    _btn2.click()
    assert wait_text("Button 1 pressed 1 times! Button 2 pressed 1 times!")

    _btn1.click()
    assert wait_text("Button 1 pressed 2 times! Button 2 pressed 1 times!")

    _btn2.click()
    assert wait_text("Button 1 pressed 2 times! Button 2 pressed 2 times!")
