var cad = cad || {};
cad.backupHtmlKey= "backupHtml";

$(document).ready(function(){
	// cad.hideEdit();
	var url = new Url();

	if ((url.query.edit) && (url.query.edit=="1")){
		/* $("#editButton").show(); */
		$("#editButton").css("display", "inline-block");
	} else {
		$('#editMenuLayer').hide();
	}

	cad.pageName = cad.getPageName();

	$("#downloadAnchor").click(function(){ $(this).hide(); });
});

cad.getPageName = function(){
	var u = new Url;
	var pathParts = u.path.split('/');
	var lastPathPart = pathParts[pathParts.length - 1];
	var pageNameParts = lastPathPart.split('.');
	var nameIndex = 0;

	if (pageNameParts.length > 1){
		nameIndex = pageNameParts.length - 2;
	}

	var pageName = pageNameParts[nameIndex];

	return pageName;
};

cad.prepEdit = function(){
	if (cad.editing){
		return;
	}

	cad.showEdit();
	var editAreas = $(".editArea");

	if ($(editAreas).length == 0){
		$(".editable").each(function(ix, ele){
			$(ele).after(
				'<br class="editDeco" />'+
				'<textarea class="editArea" for="' + $(ele).attr("id") + '" cols="48" rows="10">'+
				// cad.contentToInputFormat($(ele).html())+
				$(ele).html()+
				'</textarea>'
			);

			$(ele).data(cad.backupHtmlKey, $(ele).html());
		});
	} else {
		$(".editable").each(function(ix, ele){
			$(ele).html($(ele).data(cad.backupHtmlKey));
		});

		$(editAreas).show();
		$(".editDeco").show();
	}
};

cad.cancelEdit = function(){
	$(".editable").each(function(ix, ele){
		$(ele).html($(ele).data(cad.backupHtmlKey));
	});

	$(".editArea, .editDeco").remove();
	cad.hideEdit();
};

cad.testEdit = function(){
	$(".editArea").each(function(ix, ele){
		$("#" + $(ele).attr("for")).html(cad.inputToContentFormat($(ele).val(), true));
	});

	cad.hideEdit();
};

cad.saveEdit = function(){
	var downloadFileName = "setTextOf" + cad.properCase(cad.pageName) + '.js';

	var lines = [];
	lines.push(
		'$(document).ready(function(){'
	);

	$(".editArea").each(function(ix, ele){
		lines.push('\t$("#' + $(ele).attr("for") + '").html(');
		lines.push("\t\t'" + cad.inputToContentFormat($(ele).val()) + "'");
		lines.push('\t);');
	});

	lines.push(
		'});'
	);

	cad.hideEdit();

	var downBlob = new Blob([lines.join('\r')], {type: "text/plain; charset=utf-8"});
	var URL = window.URL || window.webkitURL || window.mozURL || window.msURL;
	var blobUrl = URL.createObjectURL(downBlob);
	$("#downloadAnchor").attr("href", blobUrl);
	$("#downloadAnchor").attr("download", downloadFileName);
	$("#downloadAnchor").css("display","inline-block");
};

cad.showEdit = function(){
	$("#editButton").hide();
	$("#downloadAnchor").hide();
	$("#testEditButton").css("display","inline-block");
	$("#cancelButton").css("display","inline-block");
	$("#saveButton").css("display","inline-block");
	cad.editing = true;
};

cad.hideEdit = function(){
	$(".editTool").remove();
	$(".editArea").hide();
	$(".editDeco").hide();
	$("#cancelButton").hide();
	$("#testEditButton").hide();
	$("#saveButton").hide();
	$("#downloadAnchor").hide();
	$("#editButton").css("display","inline-block");
	cad.editing = false;
};

cad.properCase = function(inputStr){
	if (!inputStr){
		return inputStr;
	}

	if (inputStr.length == 1){
		return inputStr[0].toUpperCase();
	}

	return inputStr[0].toUpperCase() + inputStr.substr(1).toLowerCase();
};

/*
cad.contentToInputFormat = function(innerHtml){
	var noCr = innerHtml.replace(/\r/g, "").replace(/\n/g, "").trim();
	var parts = [];

	var currentPart = "";
	for (var i=0; i < noCr.length; i++){
		var chr = noCr[i];

		if (chr == "<"){
			parts.push(currentPart);
			currentPart = "";
		}

		currentPart += chr;

		if (chr == ">"){
			parts.push(currentPart);
			currentPart = "";
		}
	}

	if (currentPart){
		parts.push(currentPart);
	}

	var paragraphNesting = 0;
	for (i=0; i<parts.length; i++){
		var lowerPart = parts[i].toLowerCase();
		if ((lowerPart.substr(0, 2) == "<p") && (lowerPart != "<p>")){
			paragraphNesting = 1;
		} else if (lowerPart == "</p>"){
			if (paragraphNesting == 0){
				parts[i] = "\r";
			} else {
				--paragraphNesting;
			}
		} else if (lowerPart == "<p>"){
			if (paragraphNesting == 0){
				parts[i] = "";
			} else {
				++paragraphNesting;
			}
		}

		parts[i] = parts[i].trim();
	}

	return parts.join("\r");
};
*/

cad.inputToContentFormat = function(input, forTest){
	var normalized = input.replace(/\r\n/g, "\r").replace(/\n/g, "\r");

	if (!forTest){
		normalized = normalized.replace(/'/g, "\\'");
	}

	var parts = normalized.split("\r");

	for (var i=parts.length-1; i>=0; i--){
		if (!parts[i]){
			parts.splice(i, 1);
		}
	}

	if (parts.length == 0){
		return "";
	}

	/*
	if (parts.length == 1){
		return parts[0];
	}

	var bareTextPartCount = 0;
 	for  (i=0; i<parts.length; i++){
		if (parts[i][0] == "<"){
			bareTextPartCount = 0;
		} else {
			bareTextPartCount++;

			if (bareTextPartCount > 1){
				if (bareTextPartCount == 2){
					parts[i-1] = '<p>' + parts[i-1] + '</p>';
				}

				parts[i] = '<p>' + parts[i] + '</p>';
			}
		}
	}
	*/

	return parts.join("");
};

