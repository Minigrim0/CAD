$(document).ready(function(){
	$("a.menuItem, a.underButton").each(function(ix, ele){
		var href = $(ele).attr("href");
		if (href){
			var hUrl = new Url(href);
			hUrl.query.edit = "1";
			$(ele).attr("href", hUrl);
		}	
	});
});
