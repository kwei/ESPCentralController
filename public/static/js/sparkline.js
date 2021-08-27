$package("backend.sparkline");
backend.sparkline = function(){

	return {
		render: function(handler, data){
			handler.sparkline(data, {
				type: 'bar',
				barColor: '#3b97f9',
				zeroColor: '#000000',
				barSpacing: 2,
				barWidth: 5,
				height: '40',
				tooltipFormat: '{{offset:offset}}:  -{{value}}dBm',
				tooltipValueLookups: {
			        'offset': {
			            0: 'ESP01',
			            1: 'ESO02',
			            2: 'ESO03',
			            3: 'ESO04',
			            4: 'ESO05',
			            5: 'ESO06',
			            6: 'ESO07',
			            7: 'ESO08',
			            8: 'ESO09',
			            9: 'ESO010',
			            10: 'ESO11',
			            11: 'ESO12',
			            12: 'ESO13',
			            13: 'ESO14',
			            14: 'ESO15',
			            15: 'ESO16',
			            16: 'ESO17',
			            17: 'ESO18'
			        }
			    }
			});
		}
	}
}();