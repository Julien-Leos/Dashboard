export const state = () => ({
  accessToken: "",
  username: ""
});

export const mutations = {
  login(state, data) {
    state.accessToken = data.token;
    state.username = data.username;
  },
  logout(state) {
    state.accessToken = "";
    state.username = "";
  }
};
