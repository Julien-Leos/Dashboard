const axios = require("axios");

export default function({ store, redirect }) {
  if (!store.state.auth.accessToken) {
    axios.defaults.headers.Authorization = "";
    return redirect("/signIn");
  }
  axios.defaults.headers.Authorization = store.state.auth.accessToken;
}
