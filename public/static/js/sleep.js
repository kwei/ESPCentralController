$package("backend.kabimon");
backend.kabimon = function(){
	return {
		sleep: function(milliseconds){
			var start = new Date().getTime();
			while(1){
				if ((new Date().getTime() - start) > milliseconds) break;
			}
		}
	};
}();