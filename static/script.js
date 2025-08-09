function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files.length) return alert("Select a file first!");

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/review', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => document.getElementById('output').textContent = data.review)
    .catch(err => console.error(err));
}
