document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);
  document.querySelector("#compose-form").onsubmit = send_email;

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function fetch_emails(mailbox) {
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      if (mailbox === "sent") {
        display_sent(emails, mailbox);
      } else {
        display_inbox_archieved(emails, mailbox);
      }
    })
    .catch((error) => console.error("Error fetching emails: ", error));
}

function display_sent(emails, mailbox) {
  const emails_view = document.querySelector("#emails-view");
  emails_view.innerHTML = "";

  emails_view.innerHTML += `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  emails.forEach((email) => {
    const email_div = document.createElement("div");
    email_div.style.backgroundColor = email.read ? "white" : "gray";
    email_div.innerHTML = `
        <table class="table">
          <tbody>
            <tr>
              <th scope="row"></th>
              <td><strong>${email.sender}</strong></td>
              <td>${email.subject}</td>
              <td>${email.timestamp}</td>
            </tr>
          </tbody>
        </table>
    `;
    emails_view.appendChild(email_div);
    email_div.addEventListener("click", () => load_mail(email.id, mailbox));
  });
}

function display_inbox_archieved(emails, mailbox) {
  const emails_view = document.querySelector("#emails-view");
  emails_view.innerHTML = "";

  emails_view.innerHTML += `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  emails.forEach((email) => {
    const email_div = document.createElement("div");
    email_div.style.backgroundColor = email.read ? "white" : "gray";
    email_div.innerHTML = `
        <table class="table">
          <tbody>
            <tr>
              <th scope="row"></th>
              <td><strong>${email.sender}</strong></td>
              <td>${email.subject}</td>
              <td>${email.timestamp}</td>
              <td><button class="btn-email archive-button">${
                email["archived"] ? "Unarchive" : "Archive"
              }</button></td>
            </tr>
          </tbody>
        </table>
    `;
    emails_view.appendChild(email_div);

    email_div.addEventListener("click", () => load_mail(email.id, mailbox));

    const archiveButton = email_div.querySelector(".archive-button");
    archiveButton.addEventListener("click", (event) => {
      event.stopPropagation(); // Prevent the click event from bubbling up to the email_div
      const newArchiveStatus = !email.archived; // Toggle the archived status
      fetch(`/emails/${email.id}`, {
        method: "PUT",
        body: JSON.stringify({
          archived: newArchiveStatus,
        }),
      })
        .then(() => {
          // Update the email object in the emails array with the new archived status
          email.archived = newArchiveStatus;
          // Update the text content of the button
          archiveButton.textContent = newArchiveStatus
            ? "Unarchive"
            : "Archive";
          load_mailbox("inbox");
        })
        .catch((error) => {
          console.error("Error archiving email:", error);
        });
    });
  });
}

function load_mailbox(mailbox) {
  fetch_emails(mailbox);

  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
}

function send_email() {
  const compose_recipients = document.querySelector(
    "#compose-recipients"
  ).value;
  const compose_subject = document.querySelector("#compose-subject").value;
  const compose_body = document.querySelector("#compose-body").value;

  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: compose_recipients,
      subject: compose_subject,
      body: compose_body,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      load_mailbox("sent");
    });
  return false;
}

function load_mail(email_id, mailbox) {
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "block";

  fetch(`emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });

  fetch(`emails/${email_id}`)
    .then((response) => response.json())
    .then((email) => {
      let email_view = document.querySelector("#email-view");
      email_view.innerHTML = `
          <div><strong>From:</strong> ${email.sender}</div>
          <div><strong>To:</strong> ${email.recipients}</div>
          <div><strong>Subject:</strong> ${email.subject}</div>
          <div><strong>Timestamp:</strong> ${email.timestamp}</div>
          <div><button class="btn-email" id="reply">Reply</button></div>
          <div>${email.body}</div>
        `;

      document.querySelector("#reply").addEventListener("click", (event) => {
        event.stopPropagation();
        console.log(email);
        compose_email();

        document.querySelector("#compose-recipients").value = email.sender;

        let subject = email.subject.startsWith("Re: ")
          ? email.subject
          : `Re: ${email.subject}`;
        document.querySelector("#compose-subject").value = subject;

        const current_datetime = new Date().toLocaleString();
        const body_prefix = `On ${current_datetime} ${email.sender} wrote:\n`;
        const pre_filled_body = `${body_prefix}${email.body}`;
        document.querySelector("#compose-body").value = pre_filled_body;
      });
    });
}
