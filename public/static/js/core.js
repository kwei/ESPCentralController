var $package = function(pkg){
	if(typeof(pkg) != 'string') return;
	pkg = pkg.split(".");
	var temp, container;
	for(var i=0, len=pkg.length ; i<len, container=pkg[i] ; i++){
		try{
			temp = (temp? (temp[container] = temp[container] || {}) : (eval(container+"="+container+"||{}")));
		}catch{
			temp = eval(container+"={}");
		}
	}
};

var SSID = ['ESP01','ESP02','ESP03','ESP04',
			'ESP05','ESP06','ESP07','ESP08','ESP09',
			'ESP10','ESP11','ESP12','ESP13', 'ESP14',
			'ESP15','ESP16','ESP17','ESP18'];
			