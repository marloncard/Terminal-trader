function getKey() {
    return window.sessionStorage.getItem('api_key')
};

function updateDisplay () {
    const loginForm = document.querySelector("div.login_form");
    const getInfo = document.querySelector("div.get_info");
    const api_key = window.sessionStorage.getItem("api_key");
    if (api_key) {
      loginForm.classList.add('hidden');
      getInfo.classList.remove('hidden');
  
    } else {
      loginForm.classList.remove('hidden');
      getInfo.classList.add('hidden');
    }
    /* check for logged in status, show and hide display elements */
};

function login (user_name, password) {
    console.log(user_name, password)
    const url = "http://127.0.0.1:5000/api/get_api_key"
    const promise = fetch(url, {
        method: "post",
        mode: "cors",
        headers: {
            "content-type": "application/json"
        },
        body: JSON.stringify({
            user_name,
            password
        })
    })
    promise.then(blob=>blob.json()).then(json=>{
        console.log(json)
        if (json.api_key !== undefined) {
            window.sessionStorage.setItem('api_key', json.api_key)
            flash("Successfully logged in!")
            updateDisplay();
        } else {
            flash("Bad credentials")
        }
    }).catch(e=>{
        flash("Promise exception", e)
    })
};

function logout () {
    window.sessionStorage.setItem("api_key", "");
    /* clear api_key in sessionStorage */
    
};

function getUserInfo () {
    /* get the username, full name, and balance of the logged in user */
    const api_key = getKey();
    const url = `http://127.0.0.1:5000/api/account_info/${api_key}`
    const promise = fetch(url)
    promise.then(blob=>blob.json()).then(json=>{
        output(json);
    })
};

function output (content) {
    const output = document.getElementById('output');
    /* display a message */
    console.log(content);
    output.innerHTML += "<p>"+ JSON.stringify(content)
};

function flash (message) {
    const flash = document.getElementById('flash');
    /* display a message to the flash div */
    flash.innerHTML = `<p>${message}</p>`
};

window.addEventListener('load', () => {
    const usernameField = document.querySelector('form input[name="user_name"]')
    const passwordField = document.querySelector('form input[name="password"]')
    const submitButton = document.querySelector('form input[type="submit"]')
    const getInfoButton = document.getElementById('getinfo')
    const logoutButton = document.getElementById('logout')

    submitButton.addEventListener("click", (event) => {
        event.preventDefault()
        login(usernameField.value, passwordField.value)
    })
    logoutButton.addEventListener("click", event=> {
        logout();
        updateDisplay();
        flash("Successfully logged out!")
    })
    getInfoButton.addEventListener("click", event=> {
        getUserInfo()
    })
    
    updateDisplay()
});