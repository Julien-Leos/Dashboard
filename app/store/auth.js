export const state = () => ({
  accessToken: "",
  username: ""
});

export const mutations = {
  signIn(state, data) {
    state.accessToken = data.token;
    state.username = data.username;
  },
  signOut(state) {
    state.accessToken = "";
    state.username = "";
  }
};
