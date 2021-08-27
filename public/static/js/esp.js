$package("backend.esp");
backend.esp = function(){

	let card = function(ssid){
		let cardTemplate = '<div class="col">\
			<div class="card mb-2 shadow-sm">\
				<div class="card-header">\
					<h4 class="my-0 fw-normal">'+ssid+'</h4>\
				</div>\
				<div class="card-body">\
					<span id="'+ssid+'Sparkline"></span>\
					<ul class="list-unstyled mt-3 mb-4">\
						<li id="'+ssid+'Timestamp"><small class="text-muted"></small></li>\
					</ul>\
					<div class="btn-group" role="group">\
						<button type="button" onclick="backend.requestHandler.handleRequest(\''+ssid+'\')" class="btn btn-outline-primary">Request</button>\
						<button type="button" onclick="backend.requestHandler.handleRequestLoop(\''+ssid+'\')" class="btn btn-outline-success">Loop</button>\
						<button type="button" onclick="backend.requestHandler.handleRequestStop(\''+ssid+'\')" class="btn btn-outline-danger">Stop</button>\
					</div>\
				</div>\
			</div>\
		</div>';
		return cardTemplate;
	}

	return {
		init: function(){
			SSID.map(ssid => $('#espCards').append(card(ssid)));
		}
	};
}();