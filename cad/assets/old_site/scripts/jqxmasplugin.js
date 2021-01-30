(function($){

	var testing = false;
	var pause = 1000;
	var thisText;
	var spansArray;
	var spanClasses=[];
	var classBasicName = 'xm';
	var magicClass = 'xmas';
	var currentClass;
	var iteration = 0;

	$.fn.kbxmasPlugin = function(pMagicClass, pPause){

		magicClass = pMagicClass || magicClass;
		pause = pPause || pause;

		$(this).find('*').each(function(){
			thisText = $(this).text();

			if (thisText !== $(this).html())
				return;

			spansArray = [];

			for (var i=0; i<thisText.length; i++){
				if ((thisText[i] >= 'A' && thisText[i] <= 'Z') || (thisText[i] >= 'a' && thisText[i] <= 'z')){
					spansArray.push('<span class="'+classBasicName+thisText[i].toUpperCase()+'">'+thisText[i]+'</span>');
				} else {
					spansArray.push(thisText[i]);
				}
			}

			$(this).html(spansArray.join(''));
		});

		// free memory
		spansArray = [];

		for (i='A'.charCodeAt(0); i<='Z'.charCodeAt(0); i++){
			spanClasses.push(classBasicName+String.fromCharCode(i));
		}

		currentClass = spanClasses.length - 1;

		setInterval(
			function(){
				setMagicOnChar();
			},
			pause
		);

		return this;
	}

	function setMagicOnChar(){
		// removeData to prevent memory leaks
		$('.'+magicClass).removeClass(magicClass).removeData();

		currentClass++;

		if (currentClass >= spanClasses.length){
			currentClass = 0;

			if (testing){
				iteration++;
				console.log('Iteration '+iteration);
			}
		}

		$('.'+spanClasses[currentClass]).addClass(magicClass);
	}

})(jQuery);
