(function($) {    
    var apiRequest;
    
    var apiRequest = {
        init : function() {
            $.get( "/espHandle", function( data ) {
                console.log("load completed: " + data);
            });
        }
    };
    window.apiRequest = apiRequest;
})(this.jQuery);