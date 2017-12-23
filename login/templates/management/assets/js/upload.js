// 上传资源
$('#upload').click(function(){
	var formData = new FormData($('#uploadForm')[0]);
	$.ajax({
		xhr: function(){
			var xhr = new window.XMLHttpRequest();
			xhr.upload.addEventListener("progress", function(evt){
				if (evt.lengthComputable) {
					var percentComplete = (evt.loaded / evt.total) * 100;
					//Do something with upload progress
				
					console.log(percentComplete);
					$("#percent").html(parseInt(percentComplete) + '%')  
				    $("#progressNumber").css("width",""+percentComplete+"px");
				}
			}, false);
			//Download progress
			xhr.addEventListener("progress", function(evt){
				if (evt.lengthComputable) {
					var percentComplete = evt.loaded / evt.total;
					//Do something with download progress
					console.log(percentComplete);
				
				}
			}, false);
			return xhr;
		},
		url:'https://119.23.45.38/upload',
		type:'POST',
		data:formData,
		cache:false,
		contentType:false,
		processData:false,
		beforeSend:function(request){
			var token = getCookie('token');
			request.setRequestHeader('Authentication',token)
			request.setRequestHeader('charset','utf-8')
		},
		success:function(returndata){
			alert("上传完成");
		},
		error:function(){
			alert("表单提交异常!");
		}
	});
	return false;
});

// 获取文件大小
function getFilesize(){
	var f = document.getElementById("fileInput").files;
	var fileSize = f[0].size;
	$('#size').val(fileSize);
}



