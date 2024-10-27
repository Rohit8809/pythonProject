function addTask() {
    const taskInput = document.getElementById('task-input');
    const taskList = document.getElementById('task-list');

    if (taskInput.value.trim() !== '') {
        const li = document.createElement('li');
        li.textContent = taskInput.value;
        taskList.appendChild(li);
        taskInput.value = ''; // Clear the input
    } else {
        alert('Please enter a task.');
    }
}

function manageEmail() {
    alert('Email management feature is currently not implemented.');
}

function sendWhatsApp() {
    alert('WhatsApp notification feature is currently not implemented.');
}

// Dummy news recommendations
const newsList = document.getElementById('news-list');

recommendedNews.forEach(news =>
{
    const li = document.createElement('li');
    li.textContent = news;
    newsList.appendChild(li);
});
