window.onload = function(){
	$.ajax({
		url:"https://119.23.45.38/admin/manager/new/getuserlist?page=1",
		type:"GET",
		beforeSend:function(request){
			var oauth = getCookie("token");
			request.setRequestHeader("Authentication",oauth);
		},
		success:function(data){
			var obj = eval("(" + data + ")");
			if(obj.hasOwnProperty("users"))
			{
				var html = '';
				for(key in obj.users)
				{
					html += '<tr><td><img src="img/contact-img.png" class="img-circle avatar hidden-phone"/>' 
						+ '<a href="user-profile.html" class="name">' + obj.users[key].username + '</a><span class="subtext">使用中</span>'
						+ '</td><td>' + obj.users[key].date + '</td><td>' + obj.users[key].location + '</td><td>' 
						+ obj.users[key].version + '</td></tr>';
				}
				$('#userlist').append(html);
			}

			if(obj.hasOwnProperty("pages"))
			{
				// 设置页码
				var html = '';
				for(var i=1; i <= obj.pages; i++)
				{
					html += '<li><button onclick="getuserlistpage(' + i.toString() + ')">' + i.toString() + '</button></li>';
				}
				$('#userpage').append(html);
			}
		}
	});
};


function getuserlistpage(page)
{
	var geturl = "https://119.23.45.38/admin/manager/new/getuserlist?page=" + page.toString();
	$.ajax({
		url:geturl,
		type:"GET",
		beforeSend:function(request){
			var token = getCookie("token"); 
			request.setRequestHeader("Authentication",token);
		},
		success:function(data){
			var obj = eval("(" + data + ")");
			if(obj.hasOwnProperty("users"))
			{
				var html = '';
				for(key in obj.users)
				{
					html += '<tr><td><img src="img/contact-img.png" class="img-circle avatar hidden-phone"/>' 
						+ '<a href="user-profile.html" class="name">' + obj.users[key].username + '</a><span class="subtext">使用中</span>'
						+ '</td><td>' + obj.users[key].date + '</td><td>' + obj.users[key].location + '</td><td>' 
						+ obj.users[key].version + '</td></tr>';
				}
				$('#userlist').empty();
				$('#userlist').append(html);
			}
		}
	});
}

