
const form = document.querySelector('form');


form.addEventListener('submit', (e) => {

  e.preventDefault();


  const loginInput = document.getElementById('login');
  const passwordInput = document.getElementById('password');

  if (loginInput.value.trim() === '' || passwordInput.value.trim() === '') {
    alert('Please enter both the login and password.');
    return;
  }

  // If the form is valid, you can proceed with form submission
  // Here, you can perform any additional logic such as making an API call, etc.
  // For demonstration purposes, we'll simply log the form data to the console
  console.log('Form submitted!');
  console.log('Login:', loginInput.value);
  console.log('Password:', passwordInput.value);

  // Reset the form inputs
  form.reset();
});
