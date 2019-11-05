export const state = () => ({
  access_token: ""
});

export const mutations = {
  update(state, token) {
    state.access_token = token;
  }
};
