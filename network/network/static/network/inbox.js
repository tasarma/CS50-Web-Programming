document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#new-post-form").onsubmit = save_new_post;
});

function save_new_post(event) {
  event.preventDefault();
  const body = document.querySelector('#new-post-body').value;

  fetch("/", {
    method: "POST",
    body: JSON.stringify({
      body: body,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
    });
}
