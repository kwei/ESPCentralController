$package("backend.timeStamp");
backend.timeStamp = function(){
	return {
		getTime: function(){
			let today = new Date();
			let date = today.getFullYear()+'/'+(today.getMonth()+1)+'/'+today.getDate();
			let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
			let dateTime = date+', '+time;
			let timestamp = 'time: '+dateTime;
			return timestamp
		},
		render: function(){
			return "<small class='text-muted'>"+backend.timeStamp.getTime()+"</small>";
		}
	};
}();