function takeImages() {
    const id = document.getElementById('id').value;
    const name = document.getElementById('name').value;
    
    fetch('/take_images', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `id=${id}&name=${name}`
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function saveProfile() {
    fetch('/save_profile', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function trackImages() {
    fetch('/track_images', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.attendance) {
            const attendanceList = document.getElementById('attendanceList');
            attendanceList.innerHTML += `<p>ID: ${data.attendance.id}, Name: ${data.attendance.name}</p>`;
        } else {
            alert('No face recognized');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}