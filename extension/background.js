function copy(text) {
    const ta = document.createElement('textarea');
    ta.style.cssText = 'opacity:0; position:fixed; width:1px; height:1px; top:0; left:0;';
    ta.value = text;
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    document.execCommand('copy');
    ta.remove();
}


function getSites() {
    fetch('https://localhost:22222/v1/api/sites', {method: 'GET'})
        .then(response => {
            return response.json();
        }).then(callback);
}

function getPasswords(url, callback) {
    fetch(`https://localhost:22222/v1/api/password?url=` + encodeURIComponent(url), {method: 'GET'})
        .then(response => {
            return response.json();
        }).then(callback);
}

function createPassword(url, login, callback) {
    fetch('https://localhost:22222/v1/api/createpassword?url=' + encodeURIComponent(url) + '&login=' + encodeURIComponent(login), {method: 'GET'})
        .then(response => {
            return response.json();
        }).then(callback);
}

let inputDataItem = {
    id: "input_data",
    title: "Input password data",
    contexts: ["all"]
};

let createDataItem = {
    id: "create_data",
    title: "Create password for current site",
    contexts: ["all"]
};

chrome.contextMenus.create(inputDataItem);
chrome.contextMenus.create(createDataItem);

chrome.contextMenus.onClicked.addListener(data => {
    if (data.menuItemId === "input_data") {
        chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
            var activeTab = tabs[0];
            getPasswords(activeTab.url, onPasswordsLoaded);
        });
    } else if (data.menuItemId === 'create_data') {
        call(getLoginFromInput, [], createPasswordWithLogin);
    }
});

function createPasswordWithLogin(result) {
    let login = result[0];
    if (!login) {
        login = window.prompt("Could not find login, enter it manually to continue:", "");
        if (!login) return;
    }

    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
        var activeTab = tabs[0];
        createPassword(activeTab.url, login, onRecordCreated);
    });
}

function onRecordCreated(data) {
    let login = data.login;
    let password = data.password;
    if (!login || !password) {
        alert("Could not insert new record");
        return;
    }
    call(injectPassword, {password}, postRecordCreated)
}

function postRecordCreated(data) {
    if (!data[0].success) {
        copy(result[0].password);
        alert("Could not insert password. \nPassword copied to clipboard.");
    }
}

function onPasswordsLoaded(data) {
    console.log("Received passwords: ", data);
    if (data.length == 0) return;
    let record = null;
    if (data.length > 1) {
        let prompt = data.map((r, i) => i + ". " + r.login).join('\n');
        let choice = parseInt(window.prompt("Multiple records found, pick login:\n" + prompt));
        if (!choice || !data[choice]) return;
        record = data[choice];
    } else {
        record = data[0];
    }
    let login = record.login;
    let password = record.password;
    console.log("Calling inject");
    call(injectUserData, {login, password}, postInsertData);
}

function postInsertData(result) {
    if (!result[0].success) {
        copy(result[0].password);
        alert("Could not insert user data. \nPassword for '" + result[0].login + "' copied to clipboard.");
    }
}

chrome.browserAction.onClicked.addListener(tab => {
    var newURL = "https://localhost:22222/";
    chrome.tabs.create({url: newURL});
    alert("Extension welcome page opened.\n" +
        "If there is an error about not private connection, trust the certificate to proceed.\n" +
        "If there is an error that the site cannot be reached, open desktop application and login to a database.\n");
});


chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    if (changeInfo.status == 'complete') {
        console.log(tabId, changeInfo, tab);
        getPasswords(tab.url, onPasswordsLoaded);
    }
})
