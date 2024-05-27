const apiBaseUrl = 'http://127.0.0.1:5000';
const TOKEN_EXPIRATION_TIME = 2 * 60 * 1000; // 2 minutos

let tokenExpirationTimeout;

// Utility function to show and hide views
function showView(viewId) {
    document.querySelectorAll('#app > div').forEach(div => {
        div.classList.add('hidden');
    });
    document.getElementById(viewId).classList.remove('hidden');
}

// Método para obtener el token CSRF con 'credentials: include'
async function loadCsrfToken() {
    try {
        const response = await fetch(`${apiBaseUrl}/csrf-token`, {
            method: 'GET',
            credentials: 'include'  // Importante para que la cookie de sesión se mantenga
        });
        if (!response.ok) {
            throw new Error('Failed to load CSRF token');
        }
        const data = await response.json();
        window.csrfToken = data.csrfToken;
        console.log('CSRF Token loaded:', data.csrfToken);
        return data.csrfToken;
    } catch (error) {
        console.error('Error loading CSRF token:', error);
        return null;
    }
}

// Función para mostrar mensajes estéticos
function showMessage(message, isError = false) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
    messageDiv.style.color = isError ? 'red' : 'green';
}

// Función para limpiar mensajes
function clearMessage() {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = '';
}

// Función para manejar el proceso de login
async function login(event) {
    event.preventDefault(); // Evita el comportamiento predeterminado del formulario

    const nickname = document.getElementById('nickname').value;
    const clave = document.getElementById('clave').value;
    const token = document.getElementById('token').value;
    const tokenSent = document.getElementById('tokenSent').value === "true";

    const loginAttemptsKey = `loginAttempts_${nickname}`;
    const tokenAttemptsKey = `tokenAttempts_${nickname}`;
    const lockoutTimeKey = `lockoutTime_${nickname}`;

    const loginAttempts = parseInt(localStorage.getItem(loginAttemptsKey)) || 0;
    const tokenAttempts = parseInt(localStorage.getItem(tokenAttemptsKey)) || 0;
    const lockoutTime = parseInt(localStorage.getItem(lockoutTimeKey)) || 0;
    const currentTime = Date.now();

    if (loginAttempts >= 3 && currentTime < lockoutTime) {
        showMessage('Has alcanzado el máximo de intentos. Intenta nuevamente en 30 minutos.', true);
        return;
    }

    try {
        const csrfToken = window.csrfToken;
        const requestBody = { nickname, clave };
        if (tokenSent) {
            requestBody.token = token;
        }

        // Realiza una solicitud POST para el login
        const response = await fetch(`${apiBaseUrl}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            credentials: 'include',  // Importante para que la cookie de sesión se mantenga
            body: JSON.stringify(requestBody)
        });

        const data = await response.json();
        if (!response.ok) {
            console.error('Error data:', data);
            showMessage('Verifica tu nickname y contraseña y vuelve a intentar, tienes un máximo de 3 intentos.', true);

            // Incrementar los intentos de login fallidos del lado del cliente
            const updatedAttempts = loginAttempts + 1;
            localStorage.setItem(loginAttemptsKey, updatedAttempts);

            if (updatedAttempts >= 3) {
                localStorage.setItem(lockoutTimeKey, currentTime + 30 * 60 * 1000); // Bloqueo de 30 minutos
            }
            return;
        }

        if (data.message.includes("Token enviado")) {
            // Guarda el estado en sessionStorage
            sessionStorage.setItem('nickname', nickname);
            sessionStorage.setItem('clave', clave);
            document.getElementById('tokenSent').value = "true";
            document.getElementById('tokenInput').classList.remove('hidden');
            document.getElementById('nickname').disabled = true;
            document.getElementById('clave').disabled = true;
            showMessage('Un token ha sido enviado a su correo', false);
            // Iniciar el temporizador de expiración del token
            startTokenExpirationTimer();
        } else if (data.message.includes("Login exitoso")) {
            // Restablece el contador de intentos fallidos
            localStorage.removeItem(loginAttemptsKey);
            localStorage.removeItem(lockoutTimeKey);
            localStorage.removeItem(tokenAttemptsKey);

            // Guarda el token en sessionStorage y muestra la pantalla de gestión de tareas
            sessionStorage.setItem('token', token);
            sessionStorage.setItem('id_usuario', data.id_usuario);
            showView('taskManagerView');
            clearTokenExpirationTimer(); // Limpiar el temporizador de expiración del token
        } else {
            showMessage(data.message, true);

            // Incrementar los intentos de token fallidos si se está en el estado de token enviado
            if (tokenSent) {
                const updatedTokenAttempts = tokenAttempts + 1;
                localStorage.setItem(tokenAttemptsKey, updatedTokenAttempts);

                if (updatedTokenAttempts >= 3) {
                    showMessage('Has alcanzado el máximo de intentos de token. La sesión se cerrará.', true);
                    // Cerrar sesión y volver a la pantalla inicial
                    logout(true);
                }
            }
        }
    } catch (error) {
        console.error('Error during login:', error);
        showMessage(`Error: ${error.message}`, true);
    }
}

// Función para iniciar el temporizador de expiración del token
function startTokenExpirationTimer() {
    clearTokenExpirationTimer(); // Limpiar cualquier temporizador previo
    const expirationTime = Date.now() + TOKEN_EXPIRATION_TIME;
    sessionStorage.setItem('tokenExpiration', expirationTime);

    tokenExpirationTimeout = setTimeout(() => {
        const storedExpirationTime = parseInt(sessionStorage.getItem('tokenExpiration'), 10);
        if (Date.now() >= storedExpirationTime) {
            logout();
            showMessage('La sesión ha expirado. Por favor, inicia sesión nuevamente.', true);
        }
    }, TOKEN_EXPIRATION_TIME);
}

// Función para limpiar el temporizador de expiración del token
function clearTokenExpirationTimer() {
    if (tokenExpirationTimeout) {
        clearTimeout(tokenExpirationTimeout);
        tokenExpirationTimeout = null;
    }
}

// Función para cerrar sesión
function logout(showInitialMessage = false) {
    const nickname = sessionStorage.getItem('nickname');
    const loginAttemptsKey = `loginAttempts_${nickname}`;
    const tokenAttemptsKey = `tokenAttempts_${nickname}`;
    const lockoutTimeKey = `lockoutTime_${nickname}`;

    sessionStorage.clear();
    localStorage.removeItem(tokenAttemptsKey); // Restablecer los intentos de token fallidos
    localStorage.removeItem(loginAttemptsKey); // Restablecer los intentos de login fallidos
    localStorage.removeItem(lockoutTimeKey); // Restablecer el tiempo de bloqueo
    clearMessage(); // Limpiar cualquier mensaje previo
    clearTokenExpirationTimer(); // Limpiar el temporizador de expiración del token
    showView('loginView');
    // Restablecer el formulario de login
    document.getElementById('loginForm').reset();
    document.getElementById('nickname').disabled = false;
    document.getElementById('clave').disabled = false;
    document.getElementById('tokenInput').classList.add('hidden');
    document.getElementById('tokenSent').value = "false";
    if (showInitialMessage) {
        showMessage('Has alcanzado el máximo de intentos de token. La sesión se ha cerrado.', true);
    }
}

// Función para manejar la actividad del usuario
function resetTokenExpirationTimer() {
    if (document.getElementById('tokenSent').value === "true") {
        startTokenExpirationTimer();
    }
}

// Función para cargar el token CSRF al cargar la página y determinar la vista inicial
window.addEventListener('load', async () => {
    await loadCsrfToken();  // Usa el método con 'credentials: include' para obtener el token CSRF al cargar la página

    // Siempre mostrar la vista de login inicialmente
    showView('loginView');

    // Al cargar la página, verificamos si hay un token pendiente y mostramos el campo si es necesario
    if (sessionStorage.getItem('tokenPending') === 'true') {
        const tokenExpiration = parseInt(sessionStorage.getItem('tokenExpiration'), 10);
        if (Date.now() < tokenExpiration) {
            document.getElementById('tokenSent').value = "true";
            document.getElementById('tokenInput').classList.remove('hidden');
            document.getElementById('nickname').disabled = true;
            document.getElementById('clave').disabled = true;
            startTokenExpirationTimer(); // Reiniciar el temporizador de expiración
        } else {
            logout();
        }
    }
});

// Eventos para los botones de login y cierre de sesión
document.getElementById('loginForm').addEventListener('submit', login);
document.getElementById('logoutButton').addEventListener('click', () => logout());

// Eventos de actividad del usuario para resetear el temporizador de expiración del token
['mousemove', 'keydown', 'click'].forEach(event => {
    document.addEventListener(event, resetTokenExpirationTimer);
});

// Manejamos el evento antes de descargar la página para asegurarnos de que se guarda el estado del token
window.addEventListener('beforeunload', (event) => {
    if (document.getElementById('tokenSent').value === "true") {
        sessionStorage.setItem('tokenPending', 'true');
    } else {
        sessionStorage.removeItem('tokenPending');
    }
});
