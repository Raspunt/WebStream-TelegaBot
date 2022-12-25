
const { createApp } = Vue


try{
Vue.config.devtools = true;
}
catch (e){
 console.log('dev-tools not work ):')
}

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

    StopCamera(){

        axios({
            method: "post",
            url: "/stopCamera",
            headers: { "Content-Type": "multipart/form-data" },
        })
        .then((response)=>{

        })

        console.log("Stop Camera");

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
    EnableMontionDetection(){
        
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
    DisableMontionDetection(){
        
        axios({
            method: "post",
            url: "/DisableMontionDetection",
            headers: { "Content-Type": "multipart/form-data" },
        })
       .then(function (response) {

        })
      .catch(function (response) {
      
       });

    },


    playSound () {
        document.getElementById('AudioStream').play();
    },


    
    
},


}).mount('#app')
