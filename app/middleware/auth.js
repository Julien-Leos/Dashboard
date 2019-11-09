const axios = require("axios");

export default function({ store, redirect }) {
  if (!store.state.auth.accessToken) {
    store.commit("auth/logout");
    return redirect("/login");
  }
  axios.defaults.headers.Authorization = store.state.auth.accessToken;
}
