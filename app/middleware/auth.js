export default function({ store, redirect }) {
  console.log("MIDDLEWARE", store.state);
  if (!store.state.auth.access_token) {
    console.log("REDIRECT");
    // return redirect("/signIn");
  }
}
