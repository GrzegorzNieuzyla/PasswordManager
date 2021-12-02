
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

function sendNotification(title, msg) {
    chrome.notifications.create({
        title: title,
        message: msg,
        type: "basic",
        iconUrl: "icon128.png"
    });
}

chrome.browserAction.onClicked.addListener(tab => {
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
        var activeTab = tabs[0];
        createPassword(activeTab.url, 'user', console.log);
    });
});

function onPasswordsLoaded(data) {
    if (data.length == 0) return;
    let login = data[0].login;
    let password = data[0].password;
    console.log(login, password);
}

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    if (changeInfo.status == 'complete') {
        console.log(tabId, changeInfo, tab);
        getPasswords(tab.url, onPasswordsLoaded);
    }
})
