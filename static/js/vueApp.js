
const { createApp } = Vue




let app = createApp({
   data() {
     return {
       showVideo:true,
       username:"",
       password:"",
       ImgDegrees:90
     }
   },
 methods:{
    

    CheckUser(){
        var fd = new FormData();
        fd.append('username', this.username);
        fd.append('password', this.password);
    
        axios({
            method: "post",
            url: "/LoginUser",
            data:fd,
            headers: { "Content-Type": "multipart/form-data" },
            })
        .then(function (response) {
            //handle success
            console.log(response.data);

            if (response.data === "correct"){
                app.showVideo = true;
                console.log(app.showVideo);
                
            }


        })
        .catch(function (response) {
            //handle error
        });	
    },
    RotateCamera(){
        
        const camera = document.getElementById('camera');
        camera.style.transform = `rotate(${this.ImgDegrees}deg)`;
        this.ImgDegrees += 90

    },


    StartCamera(){

        location.reload(); 
        console.log("Start Camera");

    },
    SendMotorSignal(comm,btnId){
        
        let btn = document.getElementById(btnId)
        btn.style = "background-color:black;color: white;"
        
        var fd = new FormData();
        fd.append('mc', comm);
    
        axios({
            method: "post",
            url: "/motor_command",
            data:fd,
            headers: { "Content-Type": "multipart/form-data" },
        })
       .then(function (response) {
            btn.style = "background-color:white;color: black;"
       })
      .catch(function (response) {
      
       });	


    },
    RecordVideo(){
        axios({
            method: "post",
            url: "/EnableMontionDetection",
            headers: { "Content-Type": "multipart/form-data" },
        })
       .then(function (response) {

        })
      .catch(function (response) {
      
       });
    },
    EnableAnalizator(){
        
        axios({
            method: "post",
            url: "/EnableAnalizator",
            headers: { "Content-Type": "multipart/form-data" },
        })
       .then(function (response) {

        })
      .catch(function (response) {
      
       });

    },
    EnableFaceRecognation(){
        
        axios({
            method: "post",
            url: "/EnableFaceRecognation",
            headers: { "Content-Type": "multipart/form-data" },
        })
       .then(function (response) {

        })
      .catch(function (response) {
      
       });

    },


    getCookie(cname) {
        let name = cname + "=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let ca = decodedCookie.split(';');
        for(let i = 0; i <ca.length; i++) {
          let c = ca[i];
          while (c.charAt(0) == ' ') {
            c = c.substring(1);
          }
          if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
          }
        }
        return "";
    }

    ,checkEncryptPassword(password){
      
    
        let form_data = new FormData();
        form_data.append('password',password)
    
        url = "/CheckEncryptPassword"
    
        axios.post(url,form_data)
        .then(function (response) {
            console.log(response.data);
    
            if (response.data === 0){
                location.href = "/login"
            }
    
        })
        .catch(function (error) {
            console.log(error);
        });
    }
    
},
created() {
    
    let password = this.getCookie("password");
    
    if (password == ""){
        location.href = "login"  
    }else {

        this.checkEncryptPassword(password)
 
    }
    



},



}).mount('#app')
