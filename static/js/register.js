$(function () {
    function bindCaptchaBtnClick() {
        $("#captcha-btn").click(function () {
            var $btn = $(this);
            var email = $("input[name='email']").val().trim();
            if (!email) {
                alert("Please enter email!");
                return;
            }
            // 解除点击事件，避免重复点击
            $btn.off('click');
            $.ajax('/auth/captcha?email='+email,{
                method:'GET',
                success:function(result){
                    if(result['code']==200){
                        alert("Send successful!");
                    }else{
                        alter(result['message']);
                    }
                },
                fail:function (error){
                    console.log(error);
                }
            })
            var countdown = 60;
            var timer = setInterval(function () {
                if (countdown <= 0) {
                    clearInterval(timer);
                    $btn.text("Get verification");
                    // 倒计时结束后重新绑定点击事件
                    bindCaptchaBtnClick();
                } else {
                    $btn.text(countdown + "s");
                    countdown--;
                }
            }, 1000);
        });
    }
    bindCaptchaBtnClick();
});
