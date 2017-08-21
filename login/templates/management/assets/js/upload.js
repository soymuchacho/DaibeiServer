// 上传资源
$('#upload').click(function(){
	var formData = new FormData($('#uploadForm')[0]);
	var bar = $('.bar');
	var percent = $('.percent');
	$.ajax({
		url:'https://119.23.45.38/upload',
		type:'POST',
		dataType:'text',
		data:formData,
		beforeSend:function(request){
			var token = getCookie('token');
			request.setRequestHeader('Authentication',token)
			var percentVal = '0%';
			bar.width(percentVal);
			percent.html(percentVal);
		},
		xhr:function(){
			// 绑定progress事件的回调函数
			myXhr = $.ajaxSetting.xhr();
			// 检查upload属性是否存在
			if(myXhr.upload)
			{
				myXhr.upload.addEventListener('progress',progressHandingFunction,false);	
			}
			return myXhr;
		},
		success:function(returndata){
			alert(returndata)
			var percentVal = '100%';
			bar.width=(percentVal);
			percent.html(percentVal);
		},
		error:function(){
			alert("表单提交异常!");
		}
	});
	return false;
});

// 上传进度回调函数
function progressHandingFunction(e) {
	if(e.lengthComputable){
		var percentVal = e.loaded/e.total*100;
		bar.width(percentVal);
		percent.html(percentVal + '%');
	}
}

// 获取文件大小
function getFilesize(){
	var f = document.getElementById("fileInput").files;
	var fileSize = f[0].size;
	$('#size').val(fileSize);
}



