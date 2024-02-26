document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function fetch_emails(mailbox) {
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails)
    display_emails(emails, mailbox);
  })
  .catch(error => console.error('Error fetching emails: ', error));
}

function display_emails(emails, mailbox) {
  const emails_view = document.getElementById('emails-view');
  emails_view.innerHTML = '';

  emails_view.innerHTML += `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  emails.forEach(email => {
    const email_div = document.createElement('div');
    email_div.style.backgroundColor = email.read ? 'lightgray' : 'white';
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
  });
}


function load_mailbox(mailbox) {
  fetch_emails(mailbox);

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
}

function send_email() {
  const compose_recipients = document.querySelector('#compose-recipients').value;
  const compose_subject = document.querySelector('#compose-subject').value;
  const compose_body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: compose_recipients,
      subject: compose_subject,
      body: compose_body
    })
  })
  .then(response => response.json())
  .then(result => {
    load_mailbox('sent');
  })
  return false;
}
