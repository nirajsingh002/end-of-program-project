export const initialState = {
  soilData: {
    Nitrogen: "0",
    Phosphorus: "0",
    Potassium: "0",
    temperature: "",
    humidity: "",
    ph: "",
    rainfall: "",
    isGetNPK: false,
  },
};

export function reducer(state, action) {
  switch (action.type) {
    case "SET_SOIL_DATA":
      return {
        ...state,
        soilData: {
          ...state.soilData,
          ...action.payload,
        },
      };

    default:
      return state;
  }
}
