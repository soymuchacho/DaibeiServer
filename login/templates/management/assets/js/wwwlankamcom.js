

function setCookie(cname,cvalue)
{
	var Days = 1;
	var exp = new Date();
	exp.setTime(exp.getTime() + Days*24*60*60*1000);
	document.cookie = cname + "="+ escape(cvalue) + ";expires=" + exp.toGMTString();
}


function getCookie(cname)
{
	var arr,reg=new RegExp("(^| )"+cname+"=([^;]*)(;|$)");
	if(arr=document.cookie.match(reg))
		return unescape(arr[2]);
	else
		return null;
}

function clearCookie(cname)
{
	setCookie(cname, "", -1);
}

