var mute = true;

jQuery.preloadImages = function () {
	for (i = 0; i < arguments.length; i++) {
		jQuery("<img>").attr("src", arguments[i]);   
	} 
};

function rnCheck() {
	$('#nameform').fadeIn(700);
	$('#face').fadeIn(700);
}

function new_thumbs(){
	
	$(".thumbimg").each(function () {
        $(this).unbind('click');
    });

	$('#thumbnails').fadeOut(600, function () {
 		$('#thumbnails').html('<p><img id="loader" src="/facegame/static/images/loader.gif"></p>');
		$('#thumbnails').fadeIn(400);
		$.get('/facegame/json_thumbnails/?ajax=true&random=' + Math.random(), function (data) {
			$('#thumbnails').hide();
			$('#thumbnails').html(data.json_thumbnails);
			$('#thumbnails').fadeIn(400);
			initialize();
		});
    });
	
	
}

function initialize() {
	if ($.browser.opera) {
		$('#output').fadeIn(700);
		$('#nameform').attr("disabled", false);
	}
	$('#face').load(function () {
		$('#output').fadeIn(700);
		$('#nameform').attr("disabled", false);
	}).each(function () {
		if (this.complete) {
			$(this).trigger("load");
		}
	});

	$('li').mouseenter(function (event) {
		$(this).css("background-color", "#BFBAA4");
	}).mouseleave(function (event) {
		$(this).css("background-color", "#FFFFFF");
	});

	$('.thumbimg').mouseenter(function (event) {
		$(this).css("border", "1px solid black");
	}).mouseleave(function (event) {
		$(this).css("border", "1px solid gray");
	});

	$('.thumbimg').click(function (event) {
		$(this).unbind('click');
		var answer = $(this).attr("value");
		$.post('/facegame/name/updatestats/?ajax=true&random=' + Math.random(), {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(), 'answer': answer}, function (data) {
			$('#correctnum').html(data.correctAnswers);
			$('#wrongnum').html(data.wrongAnswers);
			$('#rownum').html(data.currentStreak + ", " + data.highestStreak);
			if (data.valid === true) {
				if (mute === false) {
					soundHandle1.load();
					soundHandle1.play();
				}
				$(".correctimg").animate({"width": "+=6px", "height": "+=6px"}, 300, function () {
					$(".correctimg").animate({"width": "-=6px", "height": "-=6px"}, 350);					
				});
				new_thumbs();
				return false;
			} else {
				if (mute === false) {
					soundHandle2.load();
					soundHandle2.play();
				}
				$(".thumbimg").each(function () {
                    if ($(this).attr("value") === answer) {
                        $(this).fadeTo(700, 0.35);
                    }
                });
				$(".wrongimg").animate({"width": "+=5px", "height": "+=5px"}, 300, function () {
					$(".wrongimg").animate({"width": "-=5px", "height": "-=5px"}, 350);
				});
				return false;
			}
		});
	});

	$('li').click(function (event) {
		$(this).unbind('click');
		var answer = $(this).find("input[type=radio]").val();
		$.post('/facegame/updatestats/?ajax=true&random=' + Math.random(), {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(), 'answer': answer}, function (data) {
			$('#correctnum').html(data.correctAnswers);
			$('#wrongnum').html(data.wrongAnswers);
			$('#rownum').html(data.currentStreak + ", " + data.highestStreak);
			if (data.valid === true) {
				if (mute === false) {
					soundHandle1.load();
					soundHandle1.play();
				}
				$("li").unbind('click');
				$(this).find("input[type=radio]").attr("checked", "checked");
				$('#nameform').fadeOut(600);
				$('#face').fadeOut(600, function () {
					$(this).attr('src', '/facegame/static/images/loader.gif');
					$(this).fadeIn(400);
				});
				$(".correctimg").animate({"width": "+=6px", "height": "+=6px"}, 300, function () {
					$(".correctimg").animate({"width": "-=6px", "height": "-=6px"}, 350);					
				});
				$.get('/facegame/jsonform/?ajax=true&random=' + Math.random(), function (form) {
					$('#face').fadeOut(400);
					$('#output').css("display", "none");
					$('#output').html(form.jsonform);
					rnCheck();
					initialize();
				});
				return false;
			} else {
				if (mute === false) {
					soundHandle2.load();
					soundHandle2.play();
				}
				$("li").find("input[value=" + answer + "]").parent().fadeTo(700, 0.35);
				$(".wrongimg").animate({"width": "+=5px", "height": "+=5px"}, 300, function () {
					$(".wrongimg").animate({"width": "-=5px", "height": "-=5px"}, 350);
				});
				return false;
			}
		});
		return false;
		
	});
}

$(document).ready(function () {
	$.preloadImages("/facegame/static/images/loader.gif", "/facegame/static/images/muteon.png");

	soundHandle1 = document.getElementById('soundHandle1');
	soundHandle2 = document.getElementById('soundHandle2');
	$("#soundHandle1").attr('preload', 'auto');
	$("#soundHandle2").attr('preload', 'auto');
	soundHandle1.src = '/facegame/static/sounds/correct.ogg';

	soundHandle2.src = '/facegame/static/sounds/wrong.ogg';

	$('.muteimg').bind("click", function (event) {
		if (mute === true) {
			mute = false;
			$('.muteimg').attr('src', '/facegame/static/images/muteoff.png');
		} else {
			mute = true;
			$('.muteimg').attr('src', '/facegame/static/images/muteon.png');
		}
	});

	$('.correctimg').tipsy();
	$('.wrongimg').tipsy();
	$('.rowimg').tipsy();
	$('.muteimg').tipsy();
	$('.logoimg').tipsy();
	$('.resetimg').tipsy();
	$('.switchimg').tipsy();

	new_thumbs();
});

function deteleconfirm() {
	var confirmanswer = confirm("You are about to reset your stats. Are you sure?");
	if (confirmanswer) {
		var answer = "RESET";
		$.post('/updatestats/?ajax=true&random=' + Math.random(), {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(), 'answer': answer}, function (data) {
			$('#correctnum').html(data.correctAnswers);
			$('#wrongnum').html(data.wrongAnswers);
			$('#rownum').html(data.currentStreak + ", " + data.highestStreak);
			return false;
		});
		return false;
	}
	return false;
}
