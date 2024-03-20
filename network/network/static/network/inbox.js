document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelector("#follow-button")
    .addEventListener("click", () => follow_user());
});

function follow_user() {
  const follow_button = document.querySelector('#follow-button');
  const viewed_user = follow_button.dataset.username;

  const unfollow = document.querySelector('#follow-button-container');

  fetch(`/follow_user/${viewed_user}`, {
    method: "POST",
    body: JSON.stringify({}),
  })
  .then((response) => response.json())
  .then((result) => {
    location.reload();
    });
}
