function injectUserData(data) {
    let login = data.login;
    let password = data.password;

    let passwordFields = document.querySelectorAll("input[type='password']");

    if (!passwordFields)
        return {success: false, login, password};

    function getLogin() {
        let inputs = [...document.querySelectorAll("input[type='text']"),
            ...document.querySelectorAll("input[type='email']"),
            ...document.querySelectorAll("input[type='login']")];

        let names = ['username', 'login', 'email', 'user[username]', 'user[login]', 'user[email]'];
        for (let name of names) {
            let input = inputs.filter(i => i.name == name)[0];
            if (input) return input;
        }

        // try to find input before password
        let field = passwordFields[0];
        let all_inputs = [...document.querySelectorAll('input')];
        for (let i = 1; i < all_inputs.length; i++) {
            if (all_inputs[i] === field) return all_inputs[i - 1];
        }

        return null;
    }

    let loginField = getLogin();
    console.log(loginField, passwordFields, login, password);
    if (loginField) {
        console.log("ins");
        loginField.value = login;
        for (let passwordField of passwordFields)
            passwordField.value = password;
        return {success: true, login, password};
    }
    return {success: false, login, password};
}


function getLoginFromInput(_) {
    let inputs = [...document.querySelectorAll("input[type='text']"),
        ...document.querySelectorAll("input[type='email']"),
        ...document.querySelectorAll("input[type='login']")];

    let names = ['username', 'login', 'email', 'user[username]', 'user[login]', 'user[email]'];
    for (let name of names) {
        let input = inputs.filter(i => i.name == name)[0];
        if (input) return input.value;
    }

    // try to find input before password
    let field = document.querySelectorAll("input[type='password']")[0];
    if (!field) return null;
    let all_inputs = [...document.querySelectorAll('input')];
    for (let i = 1; i < all_inputs.length; i++) {
        if (all_inputs[i] === field) return all_inputs[i - 1].value;
    }

    return null;
}

function injectPassword(data) {
    let password = data.password;

    let passwordFields = document.querySelectorAll("input[type='password']");
    if (!passwordFields)
        return {success: false, password};

    for (let passwordField of passwordFields)
        passwordField.value = password;
    return {success: true, password};
}

// used to inject scripts into page DOM
function call(fun, args, callback) {
    code = fun.toString();
    code += "data=" + JSON.stringify(args) + ";";
    code += fun.name + '(data);';
    chrome.tabs.executeScript(
        null,
        {code: code},
        callback,
    );
}