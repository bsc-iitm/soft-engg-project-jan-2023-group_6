//Post to student home
fetch('http://127.0.0.1:8080/student_home', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        "user_id": '4'
    }),
})
.then(r => r.json())
.then(l=> console.log(l))
.catch((error) => {
    console.error('Error:', error);;
});