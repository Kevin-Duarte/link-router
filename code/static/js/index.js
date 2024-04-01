
function getCookie(cookiename) 
{
    var cookiestring=RegExp(cookiename+"=[^;]+").exec(document.cookie);
    return decodeURIComponent(!!cookiestring ? cookiestring.toString().replace(/^[^=]+./,"") : "");
}

function stringToDate(string) {
    var myDate = new Date(string);
    var returnString = myDate.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true }) + ' ' +  (myDate.getMonth() + 1)  + "/" + myDate.getDate() + "/";
    returnString += myDate.getFullYear().toString().slice(-2);
    return returnString + " PST";
}

/* Do functions */
function do_signup(email, firstname, lastname) {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            genericFormLoadingCircle(false);
            if (xhr.status == 200)
                location.replace('/')
            else
                genericFormError(JSON.parse(xhr.responseText)['message']);            
        }
    }

    xhr.open('POST', '/anon/signup', true);
    let data = new FormData();
    data.append('email', email);
    data.append('firstname', firstname);
    data.append('lastname', lastname);
    xhr.send(data);
} 

function do_reset(email) {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if (xhr.readyState == XMLHttpRequest.DONE){
            genericFormLoadingCircle(false);
            if (xhr.status == 200)
                location.reload();
            else 
                genericFormError(JSON.parse(xhr.responseText)['message']); 
            
        }
    }

    var formData = new FormData()
    formData.append('email', email)
    xhr.open("POST", "/anon/password_reset_request", true);
    xhr.send(formData);
}

function do_login(email, password) {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            genericFormLoadingCircle(false);
            if (xhr.status == 200) 
                location.replace('/')
            else
                genericFormError(JSON.parse(xhr.responseText)['message']); 
        }
    }

    let data = new FormData();
    xhr.open('POST', '/anon/auth', true);
    data.append('email', email);
    data.append('password', password);
    xhr.send(data);
}

function do_logout() {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200)
                location.reload();
            else 
                alert("Error: " + JSON.parse(xhr.responseText)['message']);
            
        }
    }

    xhr.open('GET', '/user/logout', false)
    xhr.send()
}

function do_delete_link(id) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200)
                updatecontent_mylinks()
             else
                alert('Error: ' + JSON.parse(xhr.responseText)['message'])
        }
    }

    xhr.open('DELETE', '/user/delete_link?id=' + String(id), false);
    xhr.send()
}


function do_renew_link(id) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200){
                updatecontent_mylinks()
            } else{
                var response = JSON.parse(xhr.responseText)
                alert('Error: ' + response['message'])
            }
        }
    }
    xhr.open('POST', '/user/renew_link?id=' + String(id), false);
    xhr.send()
}

function do_add_ban(ipaddr, reason) {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200)
                updatecontent_banned()
            else 
                alert("Error: " + JSON.parse(xhr.responseText)['message']);
        }
    }

    let data = new FormData();
    data.append('ipaddr', ipaddr);
    data.append('reason', reason);
    xhr.open('POST', '/admin/add_ban');
    xhr.send(data)
}

function do_add_link(type, key, url) {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200)
                location.replace('/');
            else 
                alert("Error: " + JSON.parse(xhr.responseText)['message']);
        }
    }

    if (type == 'user')
        xhr.open('POST', '/user/add_link?key=' + key + "&url=" + url);
    else
        xhr.open('POST', '/anon/add_link?key=' + key + "&url=" + url);
    xhr.send()
}


/* Admin actions */
function admin_delete_link(id) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200){
                updatecontent_alllinks()
            } else{
                var response = JSON.parse(xhr.responseText)
                alert('Error: ' + response['message'])
            }
        }
    }
    xhr.open('DELETE', '/admin/delete_link?id=' + String(id), false);
    xhr.send()
}

function admin_delete_ban(id) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200){
                updatecontent_banned()
            } else{
                var response = JSON.parse(xhr.responseText)
                alert('Error: ' + response['message'])
            }
        }
    }
    xhr.open('DELETE', '/admin/delete_ban?id=' + String(id), false);
    xhr.send()
}

function admin_delete_user(id) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200){
                updatecontent_users()
            } else{
                var response = JSON.parse(xhr.responseText)
                alert('Error: ' + response['message'])
            }
        }
    }
    xhr.open('DELETE', '/admin/delete_user?id=' + String(id), false);
    xhr.send()
}

function admin_update_disable(id, option) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200){
                updatecontent_users()
            } else{
                var response = JSON.parse(xhr.responseText)
                alert('Error: ' + response['message'])
            }
        }
    }
    xhr.open('PATCH', '/admin/update_disable_user?id=' + String(id) + "&disable=" + option, false);
    xhr.send()
}

function admin_set_privledge(id, option) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200){
                updatecontent_users()
            } else{
                var response = JSON.parse(xhr.responseText)
                alert('Error: ' + response['message'])
            }
        }
    }
    xhr.open('PATCH', '/admin/update_admin_rights?id=' + String(id) + "&admin=" + option, false);
    xhr.send()
}






/* menu and menu functions */

function menu_select(menu_item) {
    event.preventDefault();
    var elements = document.querySelectorAll('.selected');
    for (var i=0; i < elements.length; i++){
        elements[i].classList.remove('selected')
    }
    document.getElementById(menu_item).classList.add('selected')
}

function updatecontent_newlink() {
    hostname = window.location.hostname
    document.getElementById('main').innerHTML = "\
    <div id='main-title'><h2>Create a New Link</h2></div> \
    <form action='/' method='POST' id='add-form'>\
                    <label for='key' id='hostname_label'><b>When users visit: " + 
                    hostname + 
                    "/</label><input type='text' id='key' name='key'><br><br>\
                    <label for='url'><b>They get sent to: </b></label>\
                    <select id='protocol' name='protocol'>\
                        <option value='https://'>https://</option>\
                        <option value='http://'>http://</option>\
                    </select>\
                    <input type='text' id='url' name='url'><br><br>\
                    <div id='link-submission-tip'>Note: Added links will expire in 30-days. Go to 'My Links' to renew important links.</div>\
                    <input type='submit' onclick='addLinkAction()' class='button-style' value='Submit'>\
                    <br>\
                </form>"
}


function updatecontent_users() {
    document.getElementById('main').innerHTML = "Loading...";
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200){
                


                var obj = JSON.parse(this.responseText);
                var table = document.createElement('TABLE');

                var tableHeader = new Array();

                //Create header
                tableHeader.push('Email / Name', 'Active / Admin / Disabled', "Creation / Last Login", 'Actions');
                var row = table.insertRow(-1);
                for (var i = 0; i < tableHeader.length; i++) {
                    var headerCell = document.createElement("TH");
                    headerCell.innerHTML = tableHeader[i];
                    row.appendChild(headerCell);
                }

                //Create cells
                for (var i = 0; i < obj.length; i++){
                    item = new Array()
                    item = [obj[i]['email'] + '<br>' + obj[i]['firstName'] + ' ' + obj[i]['lastName'],
                    "<b>Active:</b> " + obj[i]['accountActive'] + "<br><b>Admin:</b> " +  obj[i]['admin'] + "<br><b>Disabled:</b> " + obj[i]['disabled'],
                    stringToDate(obj[i]['creation']) + "<br>" + stringToDate(obj[i]['lastLogin']),
                    '<b>Admin: </b><button type="button" onclick="admin_set_privledge(' + obj[i]['id'] + ', 1)">+</button>' +
                    '<button type="button" onclick="admin_set_privledge(' + obj[i]['id'] + ', 0)">-</button><br>' +  
                    '<b>Delete: </b><button type="button" onclick="admin_delete_user(' + obj[i]['id'] + ')">Delete</button><br>' + 
                    '<b>Disable: </b><button type="button" onclick="admin_update_disable(' + obj[i]['id'] + ', 1)">+</button>' +
                    '<button type="button" onclick="admin_update_disable(' + obj[i]['id'] + ', 0)">-</button><br>'];
                    row = table.insertRow(-1);
                    for (var j = 0; j < tableHeader.length; j++) {
                        row.insertCell(-1).innerHTML = item[j];
                    }

                }

                // Table Style
                table.style.textAlign = 'left';
                table.style.borderCollapse = 'separate';
                table.style.borderSpacing = '20px';
                table.style.marginLeft='-20px';
                table.style.marginTop='-20px';
                table.style.width = '100%';
                document.getElementById('main').innerHTML = "<div id='main-title'><h2>Users</h2></div>";
                document.getElementById('main').appendChild(table);

            } else{
                var response = JSON.parse(xhr.responseText)
                alert('Error: ' + response['message'])
            }
        }
    }
    xhr.open('GET', '/admin/get_users', false);
    xhr.send();
}

function updatecontent_banned() {
    document.getElementById('main').innerHTML = "Loading...";
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200){
                
                var obj = JSON.parse(this.responseText);
                var table = document.createElement('TABLE');

                var tableHeader = new Array();

                //Create header
                tableHeader.push('IP / Reason', 'Creation', 'Actions');
                var row = table.insertRow(-1);
                for (var i = 0; i < tableHeader.length; i++) {
                    var headerCell = document.createElement("TH");
                    headerCell.innerHTML = tableHeader[i];
                    row.appendChild(headerCell);
                }

                //Create cells
                for (var i = 0; i < obj.length; i++){
                    item = new Array()
                    item = [obj[i]['ipaddr'] + '<br>' + obj[i]['reason'], 
                    stringToDate(obj[i]['creation']),  
                    '<button type="button" onclick="admin_delete_ban(' + obj[i]['id'] + ')">Un-Ban</button>'];
                    row = table.insertRow(-1);
                    for (var j = 0; j < tableHeader.length; j++) {
                        row.insertCell(-1).innerHTML = item[j];
                    }

                }
                // Table Style
                table.style.textAlign = 'left';
                table.style.borderCollapse = 'separate';
                table.style.borderSpacing = '20px';
                table.style.width = '100%';
                table.style.marginLeft='-20px';
                table.style.marginTop='-20px';
                document.getElementById('main').innerHTML = "<div id='main-title'><h2>Banned List</h2></div>";
                document.getElementById('main').innerHTML += `
                <b>New Ban:</b><br>
                <form id='ban-form'>
                <label for='ipaddr'>IP Address</label><br>
                <input type="text" name="ipaddr" required><br>
                <label for='reason'>Reason</label><br>
                <input type="text" name="reason" required><br><br>
                <button type="submit" onclick='banFormAction()'>Ban</button>
                </form><br>
                `
                document.getElementById('main').appendChild(table);

            } else{
                var response = JSON.parse(xhr.responseText)
                alert('Error: ' + response['message'])
            }
        }
    }
    
    xhr.open('GET', '/admin/get_banned', false);
    xhr.send();
}

function updatecontent_events() {
    document.getElementById('main').innerHTML =`
    <div id='main-title'><h2>Events</h2></div>
    <form id='query-form'>

    <div style='float:left'>
    <label for='ipaddr'>IP Address</label><br>
    <input type='text' name='ipaddr' placeholder='Any'><br>

    <label for='limit' >Search Limit</label><br>
    <input type='text' value='25' name='limit' placeholder='100'><br>
    </div>
    <div style='float:left; padding:0 0 0 10px'>

    <label for='type' >Type</label><br>
    <input type='text' name='type' placeholder='Any'><br>

    <label for='description'>Description</label><br>
    <input type='text' name='description' placeholder='Any'><br>
    </div>

    <div style='float:left; padding:0 0 0 10px'>

    <label for='startDate'>Start Date</label><br>
    <input type='date' name='startDate' ><br>

    <label for='email'>Email</label><br>
    <input type='text' name='email' placeholder='Any'><br>
    </div>

    <div style='float:left; padding:0 0 0 10px'>
    <label for='endDate'>End Date</label><br>
    <input type='date' name='endDate' ><br>

    <button type="submit" onclick='queryFormAction()'>Search</button>
    </div>
    </form> 
    <br>
    <div id=event-results></div>
    `;
}

function queryFormAction() {
    event.preventDefault();
    const form = document.querySelector('#query-form');
    ipaddr = form.elements['ipaddr'].value
    limit = form.elements['limit'].value
    email = form.elements['email'].value
    type = form.elements['type'].value
    description = form.elements['description'].value
    startDate = form.elements['startDate'].value
    endDate = form.elements['endDate'].value

    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200)
            {
                var obj = JSON.parse(this.responseText);
                var table = document.createElement('TABLE');

                var tableHeader = new Array();

                //Create header
                tableHeader.push('Type', 'Email', 'Description', 'IP Address', 'Timestamp');
                var row = table.insertRow(-1);
                for (var i = 0; i < tableHeader.length; i++) {
                    var headerCell = document.createElement("TH");
                    headerCell.innerHTML = tableHeader[i];
                    row.appendChild(headerCell);
                }

                //Create cells
                for (var i = 0; i < obj.length; i++){
                    item = new Array()
                    item = [obj[i]['type'],
                    obj[i]['email'],
                    obj[i]['description'],
                    obj[i]['ipaddr'],
                    stringToDate(obj[i]['creation'])];
                    row = table.insertRow(-1);
                    for (var j = 0; j < tableHeader.length; j++) {
                        row.insertCell(-1).innerHTML = item[j];
                    }

                }

                // Table Style
                table.style.textAlign = 'left';
                table.style.borderCollapse = 'separate';
                table.style.borderSpacing = '20px';
                table.style.width = '100%';
                table.style.marginLeft='-20px';
                table.style.marginTop='-20px';
                document.getElementById('event-results').innerHTML = ''
                document.getElementById('event-results').appendChild(table);

            }
            else 
                alert("Error: " + JSON.parse(xhr.responseText)['message']);
        }
    }

    
    xhr.open('GET', '/admin/get_events?ipaddr=' + ipaddr + '&limit=' + limit + '&email=' + email + '&description=' + description + '&type=' + type + '&startDate=' + startDate + '&endDate=' + endDate);
    xhr.send()    
}




function updatecontent_alllinks() {
    document.getElementById('main').innerHTML = "Loading...";
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200){
                
                var obj = JSON.parse(this.responseText);
                var table = document.createElement('TABLE');

                var tableHeader = new Array();

                //Create header
                tableHeader.push('Key / URL', 'Creation / Expiration', 'Actions');
                var row = table.insertRow(-1);
                for (var i = 0; i < tableHeader.length; i++) {
                    var headerCell = document.createElement("TH");
                    headerCell.innerHTML = tableHeader[i];
                    row.appendChild(headerCell);
                }

                //Create cells
                for (var i = 0; i < obj.length; i++){
                    item = new Array()
                    item = [obj[i]['key'] + '<br>' + obj[i]['realURL'], 
                    stringToDate(obj[i]['creation']) + '<br>' + stringToDate(obj[i]['expiration']),  
                    '<button type="button" onclick="admin_delete_link(' + obj[i]['id'] + ')">Delete</button>'];
                    row = table.insertRow(-1);
                    for (var j = 0; j < tableHeader.length; j++) {
                        row.insertCell(-1).innerHTML = item[j];
                    }

                }

                // Table Style
                table.style.textAlign = 'left';
                table.style.borderCollapse = 'separate';
                table.style.borderSpacing = '20px';
                table.style.width = '100%';
                table.style.marginLeft='-20px';
                table.style.marginTop='-20px';
                document.getElementById('main').innerHTML = "<div id='main-title'><h2>All Links</h2></div>";
                document.getElementById('main').appendChild(table);

            } else{
                var response = JSON.parse(xhr.responseText)
                alert('Error: ' + response['message'])
            }
        }
    }
    xhr.open('GET', '/admin/get_links', false);
    xhr.send();
}



function updatecontent_mylinks() {
    document.getElementById('main').innerHTML = "Loading...";
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200){
                
                var obj = JSON.parse(this.responseText);
                var table = document.createElement('TABLE');
                var tableHeader = new Array();

                //Create header
                tableHeader.push('Key / URL', 'Creation / Expiration', 'Actions');
                var row = table.insertRow(-1);
                for (var i = 0; i < tableHeader.length; i++) {
                    var headerCell = document.createElement("TH");
                    headerCell.innerHTML = tableHeader[i];
                    row.appendChild(headerCell);
                }

                //Create cells
                for (var i = 0; i < obj.length; i++){
                    item = new Array()
                    item = [obj[i]['key'] + '<br>' + obj[i]['realURL'], 
                    stringToDate(obj[i]['creation']) + '<br>' + stringToDate(obj[i]['expiration']),  
                    '<button type="button" onclick="do_renew_link(' + obj[i]['id'] + ')">Renew</button>' + '<br>' +
                    '<button type="button" onclick="do_delete_link(' + obj[i]['id'] + ')">Delete</button>' ];
                    row = table.insertRow(-1);                    
                    for (var j = 0; j < tableHeader.length; j++) {
                        row.insertCell(-1).innerHTML = item[j];
                    }

                }

                // Table Style
                table.style.textAlign = 'left';
                table.style.borderCollapse = 'separate';
                table.style.borderSpacing = '20px';
                table.style.width = '100%';
                table.style.marginLeft='-20px';
                table.style.marginTop='-20px';
                document.getElementById('main').innerHTML = "<div id='main-title'><h2>My Links</h2></div>";
                document.getElementById('main').appendChild(table);

            } else{
                var response = JSON.parse(xhr.responseText)
                alert('Error: ' + response['message'])
            }
        }
    }
    xhr.open('GET', '/user/links', false);
    xhr.send();
}

function updatecontent_account() {
    document.getElementById('main').innerHTML = "Loading...";
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE){
            if (xhr.status == 200){
                var accountInfo = JSON.parse(this.responseText);
                var outputHTML = ''
                outputHTML += "<div id='main-title'><h2>My Account</h2></div>";
                outputHTML += '<p><b>Email:</b> ' + accountInfo[1] ;
                outputHTML += '<br><b>First Name:</b> ' + accountInfo[3];
                outputHTML += '<br><b>Last Name:</b> ' + accountInfo[4];
                outputHTML += '<br><b>Created:</b> ' + stringToDate(accountInfo[5]) + "</p>";
                outputHTML += '<button type="button" onclick="do_reset(\''+ accountInfo[1] + '\')">Reset Password</button>';
                document.getElementById('main').innerHTML = outputHTML;

            } else{
                var response = JSON.parse(xhr.responseText)
                alert('Error: ' + response['message'])
            }
        }
    }
    xhr.open('GET', '/user/account_info', false);
    xhr.send();
}


function genericFormError(message) {
    document.getElementById('generic-form-error-div').style.display='block';
    document.getElementById('generic-form-error-div').innerHTML = '<p style="color: red; font-weight: bold;">' + message + '</p>';
}

function genericFormLoadingCircle(display) {
    if (display == true) {
        document.getElementById('generic-form-loading-wheel-div').style.display='block';
        document.getElementById('generic-form-action-button').style.display='none';
    }
    else {
        document.getElementById('generic-form-loading-wheel-div').style.display='none';
        document.getElementById('generic-form-action-button').style.display='block';
    }
}

/* onClick items */

function genericFormAction(type) {
    event.preventDefault();
    genericFormLoadingCircle(true);
    const form = document.querySelector('#generic-form');

    if (type == 'signup'){
        /* validate form */
        var emailRegex = /^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$/;
        var nameRegex = /^^[A-Za-z]{1,20}$$/
        if (emailRegex.test(form.elements['email'].value) == false)
        {
            genericFormError('Incorrect email address');
            genericFormLoadingCircle(false);
        }
        else if (nameRegex.test(form.elements['firstname'].value) == false || nameRegex.test(form.elements['lastname'].value) == false)
        {
            genericFormError('Incorrect name format');
            genericFormLoadingCircle(false);
        }
        else 
            do_signup(form.elements['email'].value, form.elements['firstname'].value, form.elements['lastname'].value);
    }
    else if (type == 'login') 
        do_login(form.elements['email'].value, form.elements['password'].value);
    else if (type == 'reset')
        do_reset(form.elements['email'].value);
}

function closeGenericForm() {
    document.getElementById('generic-form-div').style.display='none';
}

function addLinkAction(){
    event.preventDefault();
    const form = document.querySelector('#add-form')
    
    key = encodeURIComponent(form.elements['key'].value);
    url = encodeURIComponent(form.elements['url'].value);
    protocol = encodeURIComponent(form.elements['protocol'].value)

    if (getCookie('loggedIn') == '1')
        do_add_link('user', key, protocol + url);
    else
        do_add_link('', key, protocol + url)
} 


function banFormAction() {
    event.preventDefault();
    const form = document.querySelector('#ban-form');
    do_add_ban(form.elements['ipaddr'].value, form.elements['reason'].value)
}

/* Generic Pop-up Form */
function openGenericForm(type) {
    event.preventDefault();
    var genericFormContent = document.getElementById('generic-form');
    var divs = genericFormContent.getElementsByTagName('div');

    for (var i = 0; i < divs.length; i += 1) {
        divs[i].style.display='none';
    }

    document.getElementById('generic-form-div').style.display='block';
    if (type == 'signup') {
        document.getElementById('generic-form-label').innerHTML = '<b>Sign-Up</b>';
        document.getElementById('generic-form-email-div').style.display='block';
        document.getElementById('generic-form-firstname-div').style.display='block';
        document.getElementById('generic-form-lastname-div').style.display='block';
        document.getElementById('generic-form-action-button').innerHTML='Sign Up';
        document.getElementById('generic-form-action-button').onclick=function(){ genericFormAction(type)};
        document.getElementById('generic-form-hint-div').style.display='block';
        document.getElementById('generic-form-hint-div').innerHTML = '<p>Note: Check your inbox after submitting</p>'

    }
    else if (type == 'login') {
        document.getElementById('generic-form-label').innerHTML = '<b>Login</b>';
        document.getElementById('generic-form-email-div').style.display='block';
        document.getElementById('generic-form-password-div').style.display='block';
        document.getElementById('generic-form-remember-div').style.display='block';
        document.getElementById('generic-form-hint-div').style.display='block';
        document.getElementById('generic-form-hint-div').innerHTML = '<p><a href="/" onclick=openGenericForm("signup")>Sign Up</a> / <a href="/" onclick=openGenericForm("reset")>Reset Password</a></p>'//'<p>Pssst, you can sign up <a href="/" onclick=openGenericForm("signup")>here</a></p>'
        document.getElementById('generic-form-action-button').innerHTML='Login';
        document.getElementById('generic-form-action-button').onclick=function(){ genericFormAction(type)};
    }
    else if (type == 'reset') {
        document.getElementById('generic-form-label').innerHTML = '<b>Reset Password</b>';
        document.getElementById('generic-form-email-div').style.display='block';
        document.getElementById('generic-form-action-button').innerHTML='Submit';
        document.getElementById('generic-form-hint-div').style.display='block';
        document.getElementById('generic-form-action-button').onclick=function(){ genericFormAction(type)};
        document.getElementById('generic-form-hint-div').innerHTML = 'Check your inbox after submitting.'
        document.getElementById('generic-form-hint-div').innerHTML = '<p>Note: Check your inbox after submitting</p>'
    }

}



/* Put hostname into hostname label */
document.getElementById('hostname_label').innerHTML='<b>When users visit: </b>' + window.location.hostname + "/"

/* Update copyright info */
document.getElementById('footer').innerHTML= 'Copyright &copy; ' + new  Date().getFullYear()  + ' In Code We Speak'

/* Change webpage for anon in users */
if (getCookie('loggedIn') != '1') {

    /* show login button */
    document.getElementById('header-login-button').style.display='inline';

    /* show signup button */
    document.getElementById('header-signup-button').style.display='inline';


    /* Set tip */
    document.getElementById('link-submission-tip').innerHTML = "Note: Links created by guests expire in 7-days. Sign-up for a user account and get 30-day links with renewal options."

}

/* Change webpage for logged in users */
else {
    /* show logout button */
    document.getElementById('header-logout-button').style.display='inline';

    /* show left nav bar*/
    document.getElementById('nav').style.display='block';

    /* Move main content */
    document.getElementById('main').style.float='right';

    /* Change tip */
    document.getElementById('link-submission-tip').innerHTML = "Note: Added links will expire in 30-days. Go to 'My Links' to renew important links."


    /* Change webpage for admins */
    if (getCookie('admin') == '1')
    {
        x = document.getElementById('menu-users');
        x.style.display = 'block';

        x = document.getElementById('menu-alllinks');
        x.style.display = 'block';

        x = document.getElementById('menu-banned');
        x.style.display = 'block';

        x = document.getElementById('menu-events');
        x.style.display = 'block';
    }

}
