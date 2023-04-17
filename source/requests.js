//Post to student home
fetch('/user/4/list', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5kb2UiLCJleHAiOjE2ODE2NjMxNDV9.Gnq3P5mNbo-NUTfmV29iKt-EAd73_ZNB_M9sHgErSHM",
        
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

// Mark solved
fetch('/ticket/mark_solved', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5kb2UiLCJleHAiOjE2ODE2NjMxNDV9.Gnq3P5mNbo-NUTfmV29iKt-EAd73_ZNB_M9sHgErSHM",     
    },
    body: JSON.stringify({
        "ticket_id": '4'
    }),
})
.then(r => r.json())
.then(l=> console.log(l))
.catch((error) => {
    console.error('Error:', error);
});

// Mark duplicate
fetch('/ticket/mark_duplicate', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5kb2UiLCJleHAiOjE2ODE2NjMxNDV9.Gnq3P5mNbo-NUTfmV29iKt-EAd73_ZNB_M9sHgErSHM",     
    },
    body: JSON.stringify({
        "ticket_id": '4',
        "duplicate_id": '3'
    }),
})
.then(r => r.json())
.then(l=> console.log(l))
.catch((error) => {
    console.error('Error:', error);
});
// likes
fetch('/ticket/like', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5kb2UiLCJleHAiOjE2ODE2NjMxNDV9.Gnq3P5mNbo-NUTfmV29iKt-EAd73_ZNB_M9sHgErSHM",     
    },
    body: JSON.stringify({
        "ticket_id": '4',
        "user_id": '1',
    }),
})
.then(r => r.json())
.then(l=> console.log(l))
.catch((error) => {
    console.error('Error:', error);
});
// replies
fetch('/ticket/reply', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5kb2UiLCJleHAiOjE2ODE2NjMxNDV9.Gnq3P5mNbo-NUTfmV29iKt-EAd73_ZNB_M9sHgErSHM",     
    },
    body: JSON.stringify({
        "ticket_id": '4',
        "user_id": '1',
        "content": 'reply 1'
    }),
})
.then(r => r.json())
.then(l=> console.log(l))
.catch((error) => {
    console.error('Error:', error);
});
// Register
fetch('/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'John Doe',
        username: 'johndoe',
        email: 'johndoe@example.com',
        password: 'mypassword',
        admin: false
      })
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
  
  // Login
fetch('/login', {
method: 'POST',
headers: {
    'Content-Type': 'application/json'
},
body: JSON.stringify({
    username: 'johndoe',
    password: 'mypassword',
    })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));