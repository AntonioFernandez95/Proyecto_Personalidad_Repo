import { createContext, useContext, useMemo, useReducer, useState } from "react"
import { applyDelta, Event, hydrateClientStorage, useEventLoop, refs } from "/utils/state.js"

export const initialState = {"state": {"is_hydrated": false, "router": {"session": {"client_token": "", "client_ip": "", "session_id": ""}, "headers": {"host": "", "origin": "", "upgrade": "", "connection": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": ""}, "page": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}}}, "state.update_vars_internal_state": {}, "state.results_state": {"isUserApto": false, "is_1_ok": false, "is_2_ok": false, "is_3_ok": false, "is_4_ok": false, "is_5_ok": false, "is_6_ok": false, "is_7_ok": false, "score_item_1": 0, "score_item_2": 0, "score_item_3": 0, "score_item_4": 0, "score_item_5": 0, "score_item_6": 0, "score_item_7": 0}, "state.test_state": {"current_data": [], "current_progress": 0.7518796992481203, "num_pregunta_actual": 0, "num_preguntas": 1, "pag_actual": 0, "selections": {}, "test_data": [], "total_pages": 133, "total_preguntas": 133}, "state.on_load_internal_state": {}, "state.state": {"logged_in": false, "user": null}, "state.state.login_state": {"checkStatusButton": true, "description": "Introduce tu correo para recibir la contraseña de acceso de un solo uso", "display": "none", "email": "", "isChecked": false, "isClick1Done": false, "isEmailRegistered": false, "isEmailValid": false, "isOptionalChecked": false, "isWaiting": false, "password": "", "showEmailNotFoundAlert": false, "showPasswordAlert": "none", "show_email_alert": "block", "show_terms_alert": "block"}, "state.state.login_state.authentication": {}, "state.state.login_state.button_click": {}}

export const defaultColorMode = "light"
export const ColorModeContext = createContext(null);
export const UploadFilesContext = createContext(null);
export const DispatchContext = createContext(null);
export const StateContexts = {
  state: createContext(null),
  state__update_vars_internal_state: createContext(null),
  state__results_state: createContext(null),
  state__test_state: createContext(null),
  state__on_load_internal_state: createContext(null),
  state__state: createContext(null),
  state__state__login_state: createContext(null),
  state__state__login_state__authentication: createContext(null),
  state__state__login_state__button_click: createContext(null),
}
export const EventLoopContext = createContext(null);
export const clientStorage = {"cookies": {}, "local_storage": {}}

export const state_name = "state"

// Theses events are triggered on initial load and each page navigation.
export const onLoadInternalEvent = () => {
    const internal_events = [];

    // Get tracked cookie and local storage vars to send to the backend.
    const client_storage_vars = hydrateClientStorage(clientStorage);
    // But only send the vars if any are actually set in the browser.
    if (client_storage_vars && Object.keys(client_storage_vars).length !== 0) {
        internal_events.push(
            Event(
                'state.update_vars_internal_state.update_vars_internal',
                {vars: client_storage_vars},
            ),
        );
    }

    // `on_load_internal` triggers the correct on_load event(s) for the current page.
    // If the page does not define any on_load event, this will just set `is_hydrated = true`.
    internal_events.push(Event('state.on_load_internal_state.on_load_internal'));

    return internal_events;
}

// The following events are sent when the websocket connects or reconnects.
export const initialEvents = () => [
    Event('state.hydrate'),
    ...onLoadInternalEvent()
]

export const isDevMode = true

export function UploadFilesProvider({ children }) {
  const [filesById, setFilesById] = useState({})
  refs["__clear_selected_files"] = (id) => setFilesById(filesById => {
    const newFilesById = {...filesById}
    delete newFilesById[id]
    return newFilesById
  })
  return (
    <UploadFilesContext.Provider value={[filesById, setFilesById]}>
      {children}
    </UploadFilesContext.Provider>
  )
}

export function EventLoopProvider({ children }) {
  const dispatch = useContext(DispatchContext)
  const [addEvents, connectErrors] = useEventLoop(
    dispatch,
    initialEvents,
    clientStorage,
  )
  return (
    <EventLoopContext.Provider value={[addEvents, connectErrors]}>
      {children}
    </EventLoopContext.Provider>
  )
}

export function StateProvider({ children }) {
  const [state, dispatch_state] = useReducer(applyDelta, initialState["state"])
  const [state__update_vars_internal_state, dispatch_state__update_vars_internal_state] = useReducer(applyDelta, initialState["state.update_vars_internal_state"])
  const [state__results_state, dispatch_state__results_state] = useReducer(applyDelta, initialState["state.results_state"])
  const [state__test_state, dispatch_state__test_state] = useReducer(applyDelta, initialState["state.test_state"])
  const [state__on_load_internal_state, dispatch_state__on_load_internal_state] = useReducer(applyDelta, initialState["state.on_load_internal_state"])
  const [state__state, dispatch_state__state] = useReducer(applyDelta, initialState["state.state"])
  const [state__state__login_state, dispatch_state__state__login_state] = useReducer(applyDelta, initialState["state.state.login_state"])
  const [state__state__login_state__authentication, dispatch_state__state__login_state__authentication] = useReducer(applyDelta, initialState["state.state.login_state.authentication"])
  const [state__state__login_state__button_click, dispatch_state__state__login_state__button_click] = useReducer(applyDelta, initialState["state.state.login_state.button_click"])
  const dispatchers = useMemo(() => {
    return {
      "state": dispatch_state,
      "state.update_vars_internal_state": dispatch_state__update_vars_internal_state,
      "state.results_state": dispatch_state__results_state,
      "state.test_state": dispatch_state__test_state,
      "state.on_load_internal_state": dispatch_state__on_load_internal_state,
      "state.state": dispatch_state__state,
      "state.state.login_state": dispatch_state__state__login_state,
      "state.state.login_state.authentication": dispatch_state__state__login_state__authentication,
      "state.state.login_state.button_click": dispatch_state__state__login_state__button_click,
    }
  }, [])

  return (
    <StateContexts.state.Provider value={ state }>
    <StateContexts.state__update_vars_internal_state.Provider value={ state__update_vars_internal_state }>
    <StateContexts.state__results_state.Provider value={ state__results_state }>
    <StateContexts.state__test_state.Provider value={ state__test_state }>
    <StateContexts.state__on_load_internal_state.Provider value={ state__on_load_internal_state }>
    <StateContexts.state__state.Provider value={ state__state }>
    <StateContexts.state__state__login_state.Provider value={ state__state__login_state }>
    <StateContexts.state__state__login_state__authentication.Provider value={ state__state__login_state__authentication }>
    <StateContexts.state__state__login_state__button_click.Provider value={ state__state__login_state__button_click }>
      <DispatchContext.Provider value={dispatchers}>
        {children}
      </DispatchContext.Provider>
    </StateContexts.state__state__login_state__button_click.Provider>
    </StateContexts.state__state__login_state__authentication.Provider>
    </StateContexts.state__state__login_state.Provider>
    </StateContexts.state__state.Provider>
    </StateContexts.state__on_load_internal_state.Provider>
    </StateContexts.state__test_state.Provider>
    </StateContexts.state__results_state.Provider>
    </StateContexts.state__update_vars_internal_state.Provider>
    </StateContexts.state.Provider>
  )
}