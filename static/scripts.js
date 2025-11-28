async function postData(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const errorDate = await response.json().catch(() => ({}));
        const message = errorDate.detail || errorDate.message || 'Server error';
        throw new Error(message);
    }
    return await response.json();
}

const logBtn = document.querySelector('.log-btn');
if (logBtn) {
    logBtn.addEventListener('click', toggleRegistration); 
    }

const signUpBtn = document.querySelector('.sign-btn');
if (signUpBtn) {
    signUpBtn.addEventListener('click', showSignup);
}

function toggleRegistration() {
    const hero = document.getElementById('hero');
    const log = document.getElementById('log');
    const sign = document.getElementById('signup');

    if (hero.classList.contains('hidden')) {
        hero.classList.remove('hidden');
        sign.classList.add('hidden');

    }
    
    if (hero.classList.contains('hidden') && (sign.classList.contains('hidden'))){
        log.classList.add('hidden')
        hero.classList.remove('hidden')
    }
    else {
        hero.classList.add('hidden');
        log.classList.remove('hidden');

    }
    
}
function showSignup() {
    const log = document.getElementById('log');
    const sign = document.getElementById('signup');
    log.classList.toggle('hidden');
    sign.classList.toggle('hidden');
}
function showMain() {
    const hero = document.getElementById('hero');
    const log = document.getElementById('log');
    const sign = document.getElementById('signup');

    hero.classList.remove('hidden');
    log.classList.add('hidden');
    sign.classList.add('hidden');
    
}




document.querySelector('.log-btn').addEventListener('click', async function() {
    const email = document.getElementById('in-log').value;
    const password = document.getElementById('in-pass').value;

    if (!email || !password) {
        alert('Please fill in all fields');
        return;
    }

    try {
        const result = await postData('/login', {
            email: email,
            password: password
        });
        console.log('Login successful: ', result);
        alert('Login successful!');

        localStorage.setItem('access_token', result.access_token);
        localStorage.setItem('user_id', result.user_id);
        localStorage.setItem('user_email', result.email);

        window.location.href = '/';
    } catch (error) {
        console.error('Login error:', error);
        if (error.detail) {
            alert('Login faild: ' + error.detail);
        } else {
            alert('Login failed. Please check your credentials.');
        }
    }
})

document.querySelector('.makeAcc-btn').addEventListener('click', async function() {
    const name = document.getElementById('nikname').value;
    const age = document.getElementById('age').value;
    const password = document.getElementById('pass').value;
    const confirmPassword = document.getElementById('againpass').value;
    const email = document.getElementById('email').value;

    if (!name) {
        alert('Please fill name');
        return;
    }


    if (!password) {
        alert('Please fill password');
        return;
    }


    if (!age) {
        alert('Please fill age');
        return;
    }


    if (!email) {
        alert('Please fill email');
        return;
    }


    if (password !== confirmPassword) {
        alert('Password do not match');
        return;
    }
 
    if (isNaN(age) || age < 0) {   //если возраст не число и меньше ноля
        alert('Please enter a valid age');
        return;
    }

    try {
        const result = await postData('/register', {
            name: name,
            email: email, //`${name.toLower.Case().replace(/\s+/g, '')}@example.com` - генератор заглушки в виде почты, но он мне не нужен т.к. у меня почта обязательна
            password: password,
            age: parseInt(age)
        });

        console.log('Registration successful: ', result);
        alert('Registration successful! You can log in.');

        showSignup();
    } catch (error) {
        console.error('Registration error: ', error);
        if (error.detail) {
            alert('Registration failed: ' + error.detail);
        } else {
            alert('Registration failed. Please try again.');
        }
    }
})

function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (token) {
        // Скрыть кнопку Sign In, если пользователь авторизован
        const signInBtn = document.querySelector('.btn-get-started');
        if (signInBtn) {
            signInBtn.textContent = 'Personal account';
            signInBtn.onclick = function() {
                window.location.href = '/dashboard';
            };
        }
    }
}




// Запускаем проверку авторизацции при загрузке страницы
document.addEventListener('DOMContentLoaded', checkAuth);