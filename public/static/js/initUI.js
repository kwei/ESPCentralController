
(function($){
    backend.esp.init();
	SSID.map(ssid => $('#'+ssid+'Timestamp').html(backend.timeStamp.render()));
	SSID.map(ssid => backend.sparkline.render($('#'+ssid+'Sparkline'), new Array(SSID.length).fill(0)));
})(this.jQuery);