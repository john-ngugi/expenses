const usernameField = document.querySelector('#username-field');
const feedbackField = document.querySelector('.invalid-feedback');
const emailField = document.querySelector('#email-field')
const emailfeedbackField = document.querySelector('.invalid-feedback-email')
const usernameSuccessOutput = document.querySelector('.usernamesuccessoutput')
const emailSuccessOutput = document.querySelector('.emailsuccessoutput')
const showPasswordToggle = document.querySelector('.showPasswordToggle')
const passwordField = document.querySelector('#password-field')
const submitButton = document.querySelector('.submit-btn')


usernameField.addEventListener('keyup', (e) => {
    if (e.target.value == '') {
        usernameSuccessOutput.style.display = 'none';
    } else {
        usernameSuccessOutput.style.display = 'block';
    }
    usernameField.classList.remove('is-invalid');
    feedbackField.style.display = 'none';
    const usernameVal = e.target.value;
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`
    console.log('username value', usernameVal)
    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username", {
                body: JSON.stringify({ username: usernameVal }),
                method: 'POST',
            })
            .then((res) => res.json())
            .then(data => {
                console.log('data:', data);
                usernameSuccessOutput.style.display = 'none';
                if (data.username_error) {
                    // submitButton.setAttribute('disabled', 'disabled');
                    submitButton.disabled = true;
                    usernameField.classList.add('is-invalid');
                    feedbackField.style.display = 'block';
                    feedbackField.innerHTML = `<p>${data.username_error}</p>`;
                } else {
                    submitButton.removeAttribute('disabled')
                }
            });
    }


});

emailField.addEventListener('keyup', (e) => {

    emailField.classList.remove('is-invalid');
    emailfeedbackField.style.display = 'none';
    const emailVal = e.target.value;

    console.log('email value', emailVal)
    if (emailVal.length > 0) {
        fetch("/authentication/validate-email", {
                body: JSON.stringify({ email: emailVal }),
                method: 'POST',
            })
            .then((res) => res.json())
            .then(data => {
                console.log('data:', data);
                if (data.email_error) {
                    submitButton.disabled = true;
                    emailField.classList.add('is-invalid');
                    emailfeedbackField.style.display = 'block';
                    emailfeedbackField.innerHTML = `<p class="text-danger">${data.email_error}</p>`;
                } else {
                    submitButton.removeAttribute("disabled")
                }
            });
    }


});


showPasswordToggle.addEventListener('click', (e) => {
    if (showPasswordToggle.textContent === 'SHOW') {
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password")
    }
})