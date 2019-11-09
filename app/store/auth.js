const axios = require("axios");

export const state = () => ({
  accessToken: "",
  userMail: "",
  userId: ""
});

export const mutations = {
  login(state, data) {
    axios.defaults.headers.Authorization = data.token;
    state.accessToken = data.token;
    state.userMail = data.userMail;
  },
  logout(state) {
    axios.defaults.headers.Authorization = "";
    state.accessToken = "";
    state.userMail = "";
    state.userId = "";
  },
  setUserId(state, userId) {
    state.userId = userId;
  }
};

export const actions = {
  login({ dispatch, commit }, data) {
    commit("login", data);
    dispatch("getUserIdByMail", data.userMail);
  },
  async getUserIdByMail({ commit }, userMail) {
    const { data } = await axios.get("http://localhost:8080/users");
    const users = data.data.users;
    for (const [userId, user] of Object.entries(users)) {
      if (user.email === userMail) {
        commit("setUserId", userId);
        return userId;
      }
    }
  }
};
