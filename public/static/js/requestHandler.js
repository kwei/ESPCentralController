$package("backend.requestHandler");
backend.requestHandler = function(){

	let formatRes = function(element){
		let child = "<li>";
		child += element + "</li>";
		return child;
	}

	let isLoading = false

	function fdoLoadingDom() {
		$.blockUI({
			message: '<div id="loading-bar-spinner" class="spinner"><div class="spinner-icon"></div></div>'
		});
		isLoading = true;
	}

	function fdoReleaseDom() {
		if(isLoading){
			$.unblockUI();
		}
	}

	function fcreateRSSIList(data) {
		data = data._message;
		// console.log(typeof(data), data);
		let d = "<ul class=\"ist-unstyled mt-3 mb-4\">";
		data.map(x => d+=formatRes(x));
		d += "</ul>"
		// console.log(d);
		return d
		
	}

	function formatSparklineData(data) {
		dataset = new Array(SSID.length).fill(0);
		// console.log('create dataset: ', dataset);
		data = data._message;
		for(let i=0 ; i < data.length ; i++){
			x = data[i];
			x = x.split(":");
			// console.log('x', x);
			index = parseInt(x[0].replace('ESP', ''), 10)-1;
			value = -parseInt(x[1].replace('dBm', ''), 10);
			// console.log('index: ', index);
			// console.log('value: ', value);
			dataset[index] = value;
		}
		return dataset;
	}

	let isLoop = {};


	let httpReq = function(ssid, cb){
		// console.log("request to" + ssid);

		$.ajax({
			type: 'GET',
			url: '/requestRSS/'+ssid,
			timeout: 5000,
			beforeSend: () => { 
				if(cb == undefined) fdoLoadingDom();
				// $('#'+ssid+'rssi').html("waiting..."); 
			},
			complete: () => { 
				fdoReleaseDom();
				backend.kabimon.sleep(100);
				if(cb != undefined && isLoop[ssid]){
					cb(ssid, httpReq);
				}else{
					isLoop[ssid] = false;
				}
			},
			success: function(data){
				// $('#'+ssid+'rssi').html(fcreateRSSIList(data));
				console.log(ssid, " res: ", data);
				data = formatSparklineData(data);
				// console.log("formatSparklineData: ", data);
				backend.sparkline.render($('#'+ssid+'Sparkline'), data);
				$('#'+ssid+'Timestamp').html(backend.timeStamp.render());
				
			},
			statusCode: {
				404: function(){
					console.log(ssid, " 404");
					backend.sparkline.render($('#'+ssid+'Sparkline'), new Array(SSID.length).fill(0));
					// $('#'+ssid+'rssi').html("Not Found!");
				},
				500: function(){
					console.log(ssid, " 500");
					backend.sparkline.render($('#'+ssid+'Sparkline'), new Array(SSID.length).fill(0));
					// $('#'+ssid+'rssi').html("Internal Server Error!");
				}
			},
			error: function (XMLHttpRequest, textStatus, errorThrown){
				console.log(ssid, " Something Wrong :( => ", errorThrown);
				backend.sparkline.render($('#'+ssid+'Sparkline'), new Array(SSID.length).fill(0));
				// $('#'+ssid+'rssi').html("Something Wrong :(");
			}
		});
	}

	return {
		init: function(){
			SSID.map(x => isLoop[x] = false);
		},

		handleRequest: function(ssid){
			isLoop[ssid] = true;
			httpReq(ssid);
		},

		handleRequestLoop: function(ssid){
			isLoop[ssid] = true;
			httpReq(ssid, httpReq);
		},

		handleRequestStop: function(ssid){
			isLoop[ssid] = false;
		},

		handleRequestAll: function(){
			for(let i=0 ; i < SSID.length ; i++){
				isLoop[SSID[i]] = true;
				httpReq(SSID[i], httpReq);
			}
		}, 

		handleRequestAllStop: function(){
			SSID.map(x => isLoop[x] = false);
		}
	};
}();

$(function() {
	backend.requestHandler.init();
});