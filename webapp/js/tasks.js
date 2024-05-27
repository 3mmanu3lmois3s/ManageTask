// Función para mostrar las tareas
function renderTasks(tasks) {
    const taskContainer = document.querySelector('.task-container .task-content');
    taskContainer.innerHTML = ''; // Limpiar el contenido anterior

    tasks.forEach(task => {
        const taskElement = document.createElement('div');
        taskElement.className = 'task';

        const taskDescription = document.createElement('span');
        taskDescription.textContent = task.descripcion;

        const taskButtons = document.createElement('div');
        taskButtons.className = 'task-buttons';

        const completeButton = document.createElement('button');
        completeButton.className = 'complete';
        completeButton.textContent = 'Completar';
        completeButton.addEventListener('click', () => completeTask(task.id));

        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete';
        deleteButton.textContent = 'Eliminar';
        deleteButton.addEventListener('click', () => deleteTask(task.id));

        taskButtons.appendChild(completeButton);
        taskButtons.appendChild(deleteButton);
        taskElement.appendChild(taskDescription);
        taskElement.appendChild(taskButtons);

        taskContainer.appendChild(taskElement);
    });
}

// Función para completar una tarea (debes implementar la lógica de completar tarea)
function completeTask(taskId) {
    console.log(`Completing task with ID: ${taskId}`);
    // Aquí iría la lógica para completar la tarea, por ejemplo, una llamada a la API
}

// Función para eliminar una tarea (debes implementar la lógica de eliminar tarea)
function deleteTask(taskId) {
    console.log(`Deleting task with ID: ${taskId}`);
    // Aquí iría la lógica para eliminar la tarea, por ejemplo, una llamada a la API
}

// Función para obtener las tareas desde la API
async function fetchTasks() {
    try {
        const response = await fetch(`${apiBaseUrl}/tareas`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrfToken
            },
            credentials: 'include'
        });
        const data = await response.json();
        if (response.ok) {
            renderTasks(data);
        } else {
            console.error('Error fetching tasks:', data.message);
        }
    } catch (error) {
        console.error('Error fetching tasks:', error);
    }
}

// Llamada de ejemplo para cargar las tareas reales cuando se muestra la vista de gestión de tareas
function loadTasks() {
    if (document.getElementById('taskManagerView')) {
        fetchTasks();
    }
}

document.addEventListener('DOMContentLoaded', loadTasks);
