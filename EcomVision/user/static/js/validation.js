document.addEventListener('DOMContentLoaded', function() {

  let form = null
//  form = document.getElementById('Form_Validation');
  form = document.Form_Validation;

  form.addEventListener('submit', function (e) {

    e.preventDefault();

    const Fullname = document.getElementById('fullname')?.value.trim() || '';
    const Email = document.getElementById('email')?.value.trim() || '';
    const Password = document.getElementById('password')?.value || '';
    const C_Password = document.getElementById('confirm-password')?.value || '';
    const Otp = document.getElementById('otp')?.value || ''; // Optional OTP field

    alert("Go Ahead..")

    const FullnameError = document.getElementById('FullnameError')
    const EmailError = document.getElementById('EmailError')
    const PasswordError = document.getElementById('PasswordError')
    const C_PasswordError = document.getElementById('C_PasswordError')
    const OtpError = document.getElementById('OtpError')

    alert("Fullname : "+Fullname +"\nEmail : "+Email +"\nPassword : "+Password +"\nC_Password : "+C_Password +"\nOtp : "+Otp)

    if (FullnameError) FullnameError.textContent = '';
    if (EmailError) EmailError.textContent = '';
    if (PasswordError) PasswordError.textContent = '';
    if (C_PasswordError) C_PasswordError.textContent = '';
    if (OtpError) OtpError.textContent = '';


    if (FullnameError) {
        if (Fullname === '') {
            FullnameError.textContent = "Full name is required";

        }
        else {
            FullnameError.textContent = '';
        }
    }

    if (EmailError) {
        const EmailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (Email === '') {
            EmailError.textContent = "Email is required";

        }
        else if (!EmailPattern.test(Email)) {
            EmailError.textContent = 'Invalid email formate';

        }
        else {
            EmailError.textContent = '';
        }
    }

    if (PasswordError) {
        PasswordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$!%*?&])[A-Za-z\d@#+$!%*?&]{8,}$/;
        if (Password === '') {
            PasswordError.textContent = "Password is required";

        }
        else if (!PasswordPattern.test(Password)) {
            PasswordError.textContent = 'Invalid formate';

        }
        else {
            PasswordError.textContent = '';
        }
    }

    if (C_PasswordError) {
        if (C_Password === '') {
            C_PasswordError.textContent = "Confirm password is required";

        }
        else if (C_Password !== Password) {
            C_PasswordError.textContent = 'Both password must be same';

        }
        else {
            C_PasswordError.textContent = '';
        }
    }

    OtpPattern = /^[?=.*\d]{4}$/;
    if (OtpError) {
        if (Otp === '') {
            OtpError.textContent = "OTP is required";

        }
        else if (!OtpPattern.test(Otp)) {
            OtpError.textContent = 'OTP must be in 4 digits';
        }
        else {
            OtpError.textContent = '';
        }
    }

    alert("Form submitted successfully...")
    form.submit();

  });
});