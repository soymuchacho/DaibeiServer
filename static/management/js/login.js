$(function () {
	$('#login').click(function(){
		$.post("https://119.23.45.38/admin/authentication",
			{
				username:$('#username').val(),
				password:$('#password').val(),
			},
			function(data,status){
				var obj = eval("(" + data + ")");
				if (obj.hasOwnProperty("token"))
				{
					var addr = "https://119.23.45.38/admin/manager?next=";
					addr = addr + obj.token;
					setCookie("token",obj.token);
					location.href = addr;
				}
				else
					$('#result').html(obj.error);
			});
	});
});

function checklogin()
{
	var username = $('#username').val();
	var password = $('#password').val();
	if(username==""||password==""){
		alert("请确认是否有空缺项！");  
		matchResult=false;  
	}else if(username.length<3||username.length>20){  
		alert("用户名长度应在3到20个字符之间！");  
		matchResult=false;  
	}
}
