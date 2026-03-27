import React, { createContext, useReducer } from "react";
import { initialState, reducer } from "./reducers";

export const AppContext = createContext();

export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}
