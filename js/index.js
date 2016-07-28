$(document).ready(function(){
    $('#error_msg').hide();
    login.init();
});

var login = {
    init : function(){
        $('#submit_btn').unbind('click');
        $('#submit_btn').click(
            function(){
                login.signIn();
            }
        );

        $(document).keypress(
            function(e) {
                if(e.which == 13) {
                    console.log("ENTER");
                    login.signIn();
                }
            }
        );
    },
    messageBox : function(header,message){
        $("#dialog_header").html(header);
        $("#dialog_message").html(message);
        $(".dialog").modal("show");
    },
    signIn : function() {

        var passwd = document.getElementById('user_password').value;
        var passwdHashed = CryptoJS.MD5(passwd);
        var admin = document.getElementById('user').value;

        authent = JSON.stringify([{'username':admin,'password':passwd}]);
        //authent = JSON.stringify([{'username':admin,'password':passwdHashed.toString()}]);
        console.log(authent);

        login.main_page();

    },
    main_page : function() {
        window.location="main.html";
    }
}