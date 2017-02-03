


function barData() {
	// medData  = [
	// 	{
	// 		label: "diabetes",
	// 		value: 111
	// 	}, {
	// 		label:"prediabetes",
	// 		value: 8
	// 	}, {
	// 		label:"adhd",
	// 		value: 33
	// 	}, {
	// 		label:"apnea",
	// 		value: 55
	// 	}, {
	// 		label:"mood disorders",
	// 		value: 174
	// 	}, {
	// 		label:"high risk preg",
	// 		value: 38
	// 	}, {
	// 		label:"smokers",
	// 		value: 21
	// 	}, {
	// 		label:"no problems", 
	// 		value: 1121
	// 	}
	// ];
	return [ 
	    {
	      key: "Medical History",
	      values: medData
		}
	];
}

//var color = d3.scaleOrdinal(d3.schemeCategory20b);

nv.addGraph(function() {
	var chart = nv.models.discreteBarChart()
		.x(function(d) { return d.label })    //Specify the data accessors.
		.y(function(d) { return d.value })
		.staggerLabels(true)
		//.height(height)
		//.width(width)
		;
    //change the format of the numbers displayed. I read the nv.d3.js library to figure out the tick format 
    //is inherited as represented below. in the ',.0d', the comma means 'use commas every 3 digits', the .0d 
    //means how many decimal places to display, which in our case is 0. 
	chart.yAxis.tickFormat(d3.format(',.0d')); 

	var svg = d3.select('#chart1 svg')
		.datum(barData())
		.attr('width', width + width/5)
		.attr('height', height + height/5)
		.call(chart)
		;

	nv.utils.windowResize(chart.update);

	return chart;
});

nv.addGraph(function() {

	var chart2 = nv.models.pieChart()
		.x(function(d) { return d.label })    //Specify the data accessors.
		.y(function(d) { return d.value })
		.options({showTooltipPercent: true})
		//.width(width)
		//.height(height)
		;
//confused on what height/width is altering above and below 
	var svg = d3.select('#chart2 svg')
		.datum(medData)
		.attr('height', height)
		.append('g')
		//.attr('width', width)
		//.attr('height', height)
		//.attr('transform', 'translate(' + (width / 2) +  ',' + (height / 2) + ')');
		.call(chart2)
	;

	nv.utils.windowResize(chart2.update);

	return chart2;
});

			

// function visualize(q) {
// 	$.ajax({
// 	      type: "POST",
// 	      contentType: 'application/json',
// 	      url: "/testing",
// 	      dataType: "json",
// 	      data: JSON.stringify(q),
// 	      success:function(response){
// 	        cols = [];
// 	        var object = response[0]; 
// 	        cols.push({field: "user_id", title: "user_id", sortable: "true"});
// 	        for (row in object) {
// 	          if(row != "user_id") cols.push({field: row, title: row, sortable: "true"});
// 	        }
// 	        localStorage.setItem('specificQueryResponse', JSON.stringify(response));
// 	        window.data = response; 
// 	        localStorage.setItem('specificQueryCols', cols);
// 	        var bootstrapTab = $( '#dataTable' ).bootstrapTable({
// 	          columns: cols,
// 	          data: response            
// 	        });
// 	      }, 
// 	      error:function(){
// 	        console.log("well shit"); 
// 	      }
// 	    }); 
//   };

//
