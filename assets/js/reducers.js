import { combineReducers } from 'redux'
import {appReducer} from './Containers/App/reducers'
import {routerReducer} from 'react-router-redux'

const rootReducer = combineReducers({
    appReducer,
    routing: routerReducer
});

export default rootReducer;