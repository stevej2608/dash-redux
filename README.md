## dash-redux

Provides Plotly/[Dash] with support for a Redux style [store of truth].

    pip install dash-redux

In the *ReduxStore* component, **state** is derived from any number automatically generated
surrogate stores. The surrogate stores are presented to the application for update via callbacks.
When a callback completes, the updated surrogate is copied to a master
store. This mechanism acts as a data multiplexor feeding application state changes from Dash UI events
into an immutable **single source of truth** that can then be used to trigger
additional activity in the UI.

The application interfaces with the store using the callbacks *@Redux.update(...)*. This
callback defines Dash IO to be used by the callback handler in the normal way. When
triggered by a Dash event the associated function is called with the IO state `together
with a reference to a surrogate store` that contains a copy of the master store. The callback
modifies the state as required and returns the store state.  *ReduxStore* then copies the
new state into the master store. This, in turn, triggers an event on the master store
that can be used by the application in standard Dash callbacks.

*ReduxStore* also supports an `action_function` execution model that enforces a formal
separation of the Dash/UI from the model.

*Update function:*
```
Redux = ReduxStore(id='store', data = { "todo": []})

@Redux.update(button.input.n_clicks, input.state.value)
def new_activity(button_clicks, input, state):
    if button_clicks and input:
          state['todo'].append(input)
    return state
```
*Action function:*
```
from .todo_model import TODO_MODEL, ModelActions as action

Redux = ReduxStore(id='store', data=TODO_MODEL)

@Redux.action(button.input.n_clicks, input.state.value)
def _add(button_clicks, input):
    if button_clicks and input:
        return action.add, input
    else:
        NOUPDATE

...
```
*todo_model.py*:
```
class ModelActions:

    def add(state, input):
        current = state.todo.copy()
        state.past.append(current)
        state.todo.append(input)
        state.future = []
        return state

    def delete(state, index):
        state.past.append(state.todo.copy())
        state.todo.pop(index)
        return state

    def undo(state):
        if len(state.past) > 0:
            state.future.append(state.todo)
            state.todo = state.past.pop()
        return state

    def redo(state):
        if len(state.future) > 0:
            state.past.append(state.todo)
            state.todo = state.future.pop()
        return state

```

The snippets are taken from the todo example. See [todo/todo.py](todo/todo.py).

#### TODO Example

An eighty line todo application demonstrates the *ReduxStore*. User input
is added to the todo list. Elements from the list can be deleted. The
example also provides UNDO and REDO buttons that demonstrate how to
easily manage an applications state history.

To run the application clone this repository, then:

    pip install -r requirements.txt

    python app.py

#### Build the project

The dash-redux package is available on [pypi]. If needed, to create a local
tarball, first change the release version in *dash_spa/_version.py*, then:

    rm -rf dist dash_spa.egg-info build

    python setup.py sdist bdist_wheel

The tarball is in *dist/dash_spa-<version>.tar.gz*

To install the tarball in a dash project:

    pip install dash_spa-<version>.tar.gz

#### Testing

Pytest and [Dash Duo](https://dash.plotly.com/testing) are used for testing. To run
these tests both the Chrome browser and Chrome driver must be installed.

To run the tests:

    pytest

#### Publish

    twine upload dist/*

[pypi]: https://pypi.org/project/dash-redux/
[Dash]: https://dash.plot.ly/introduction
[store of truth]: https://redux.js.org/understanding/thinking-in-redux/three-principles
