export const state = () => ({
  accessToken: ""
});

export const mutations = {
  update(state, token) {
    state.accessToken = token;
  }
};
