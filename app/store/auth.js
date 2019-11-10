export const state = () => ({
  accessToken: "",
  userMail: "",
  userId: ""
});

export const mutations = {
  login(state, data) {
    this.$axios.defaults.headers.Authorization = data.token;
    state.accessToken = data.token;
    state.userMail = data.userMail;
  },
  logout(state) {
    this.$axios.defaults.headers.Authorization = "";
    state.accessToken = "";
    state.userMail = "";
    state.userId = "";
  },
  setUserId(state, userId) {
    state.userId = userId;
  }
};

export const actions = {
  async login({ dispatch, commit }, data) {
    commit("login", data);
    await dispatch("getUserIdByMail", data.userMail);
  },
  async getUserIdByMail({ commit }, userMail) {
    const { data } = await this.$axios.get("users");
    const users = data.data.users;
    for (const [userId, user] of Object.entries(users)) {
      if (user.email === userMail) {
        commit("setUserId", userId);
        return userId;
      }
    }
  }
};
