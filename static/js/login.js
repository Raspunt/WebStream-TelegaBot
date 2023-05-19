




function CheckPassword(){

    let username = document.getElementById("username_input").value;
    let password = document.getElementById("password_input").value;

    let form_data = new FormData();
    form_data.append('username',username)
    form_data.append('password',password)

    url = "/CheckPassword"

    axios.post(url,form_data)
    .then(function (response) {
        console.log(response.data);

        if (response.data === 1){
            location.href = "/"
        }

    })
    .catch(function (error) {
        console.log(error);
    });
    



}



function SetArgsUpdate(){
    const queryString = window.location.search;
    console.log(queryString);
}

SetArgsUpdate()