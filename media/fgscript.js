/*var correctAnswers = 0;
var wrongAnswers = 0;
var currentStreak = 0;
var highestStreak = 0;
var skips = 0;*/
var skippable = true;
var mute = true;

jQuery.preloadImages = function()
{
	for(var i = 0; i<arguments.length; i++)
	{
		jQuery("<img>").attr("src", arguments[i]);   
	} 
}

$(document).ready(function()
{
	$.preloadImages("/facegame/static/images/loader.gif", "/facegame/static/images/muteon.png");

	soundHandle1 = document.getElementById('soundHandle1');
	soundHandle2 = document.getElementById('soundHandle2');
	$("#soundHandle1").attr('preload', 'auto');
	$("#soundHandle2").attr('preload', 'auto');
	soundHandle1.src = '/facegame/static/sounds/correct.ogg';
	/*$(soundHandle1).bind("ended", function()
	{
		$('#nameform').submit();
	});*/
	soundHandle2.src = '/facegame/static/sounds/wrong.ogg';

	$('.muteimg').bind("click", function(event)
	{
		if (mute == true)
		{
			mute = false;
			$('.muteimg').attr('src', '/facegame/static/images/muteoff.png');
		} else
		{
			mute = true;
			$('.muteimg').attr('src', '/facegame/static/images/muteon.png');
		}
	});

	/*$('.helpimg').bind("click", function(event)
	{
		toggleTooltips();
	});*/

	/*$('.correctimg').tipsy({trigger: 'manual', html: true, gravity: 'se'});
	$('.wrongimg').tipsy({trigger: 'manual', html: true, gravity: 'sw'});
	$('.rowimg').tipsy({trigger: 'manual', html: true, gravity: 'ne'});
	$('.skipimg').tipsy({trigger: 'manual', html: true, gravity: 'nw'});
	$('.muteimg').tipsy({trigger: 'manual', html: true, gravity: 's'});
	$('.helpimg').tipsy({trigger: 'manual', html: true, gravity: 'w'});
	$('.logoimg').tipsy({trigger: 'manual', html: true, gravity: 'e'});*/

	$('.correctimg').tipsy();
	$('.wrongimg').tipsy();
	$('.rowimg').tipsy();
	$('.skipimg').tipsy();
	$('.muteimg').tipsy();
	$('.logoimg').tipsy();

	initialize();
});

function response(responseText)
{
	$('#face').fadeOut(400, function()
	{
		$('#output').css("display", "none");
		$('#output').html(responseText);
		rnCheck();
		initialize();
	});
}

/*function toggleTooltips()
{
	if (tooltips == false)
	{
		$('.correctimg').tipsy("show");
		$('.wrongimg').tipsy("show");
		$('.rowimg').tipsy("show");
		$('.skipimg').tipsy("show");
		$('.muteimg').tipsy("show");
		$('.helpimg').tipsy("show");
		$('.logoimg').tipsy("show");
		tooltips = true;
		return false;
	} else
	{
		$('.correctimg').tipsy("hide");
		$('.wrongimg').tipsy("hide");
		$('.rowimg').tipsy("hide");
		$('.skipimg').tipsy("hide");
		$('.muteimg').tipsy("hide");
		$('.helpimg').tipsy("hide");
		$('.logoimg').tipsy("hide");
		tooltips = false;
		return false;
	}
}*/

function initialize()
{
	$('.skipimg').fadeTo(500, 1.0);
	if( $.browser.opera ){
		$('#output').fadeIn(700);
		$('#nameform').attr("disabled", false);
	}
	$('#face').load(function()
	{
		$('#output').fadeIn(700);
		$('#nameform').attr("disabled", false);
	}).each(function()
	{
		if (this.complete)
		{
			$(this).trigger("load");
		}
	});

	$('li').mouseenter(function(event)
	{
		$(this).css("background-color", "#BFBAA4");
	}).mouseleave(function(event)
	{
		$(this).css("background-color", "#FFFFFF");
	});

	$('.skipimg').click(function(event)
	{
		var answer = "SKIPSKIP";
		$.post('/updatestats/', {'answer': answer}, function(data)
		{
			$('#skipnum').html(data.skips);
			$('.skipimg').fadeTo(500, 0.3).unbind('click');
			$('li').unbind('click');
			$('li').find("input[value=" + rnCorrect + "]").attr("checked", "checked");
			$('#nameform').fadeOut(600);
			$('#face').fadeOut(600, function()
			{
				$(this).attr('src', '/facegame/static/images/loader.gif');
				$(this).fadeIn(400);
			});
			$.get('/jsonform/', function(form)
			{
				$('#face').fadeOut(400);
				$('#output').css("display", "none");
				$('#output').html(form.jsonform);
				rnCheck();
				initialize();
			});
			return false;
		});
	});

	$('li').click(function(event)
	{
		$(this).unbind('click');
		var answer = $(this).find("input[type=radio]").val();
		$.post('/updatestats/', {'answer': answer}, function(data)
		{
			$('#correctnum').html(data.correctAnswers);
			$('#wrongnum').html(data.wrongAnswers);
			$('#rownum').html(data.currentStreak + ", " + data.highestStreak);
			if (data.valid == true)
			{
				if (mute == false)
				{
					soundHandle1.load();
					soundHandle1.play();
				}
				$("li").unbind('click');
				$(".skipimg").fadeTo(500, 0.3).unbind('click');
				if (skippable == true)
				{
					skippable = false;
				}
				$(this).find("input[type=radio]").attr("checked", "checked");
				$('#nameform').fadeOut(600);
				$('#face').fadeOut(600, function()
				{
					$(this).attr('src', '/facegame/static/images/loader.gif');
					$(this).fadeIn(400);
				});
				$(".correctimg").animate({"width": "+=6px", "height": "+=6px"}, 300, function()
				{
					$(".correctimg").animate({"width": "-=6px", "height": "-=6px"}, 350);					
				});
				/*if (mute == true)
				{
					$('#nameform').submit();
				}*/
				$.get('/jsonform/', function(form)
				{
					$('#face').fadeOut(400);
					$('#output').css("display", "none");
					$('#output').html(form.jsonform);
					rnCheck();
					initialize();
				});
				return false;
			} else
			{
				if (mute == false)
				{
					soundHandle2.load();
					soundHandle2.play();
				}
				$(".skipimg").fadeTo(500, 0.3).unbind('click');
				if (skippable == true)
				{
					skippable = false;
				}
				$("li").find("input[value="+answer+"]").parent().fadeTo(700, 0.35);
				$(".wrongimg").animate({"width": "+=5px", "height": "+=5px"}, 300, function()
				{
					$(".wrongimg").animate({"width": "-=5px", "height": "-=5px"}, 350);
				});
				return false;
			}
		});
		return false;
		

		/*if ($(this).find("input[type=radio]").val() == rnCorrect)
		{
			if (mute == false)
			{
				soundHandle1.load();
				soundHandle1.play();
			}
			$("li").unbind('click');
			$(".skipimg").fadeTo(500, 0.3).unbind('click');
			correctAnswers += 1;
			currentStreak += 1;
			if (currentStreak > highestStreak)
			{
				highestStreak = currentStreak;
			}
			if (skippable == true)
			{
				skippable = false;
			}
			$('#correctnum').html(correctAnswers);
			$('#rownum').html(currentStreak + ", " + highestStreak);
			$(this).find("input[type=radio]").attr("checked", "checked");
			$('#nameform').fadeOut(600);
			$('#face').fadeOut(600, function()
			{
				$(this).attr('src', '/facegame/static/images/loader.gif');
				$(this).fadeIn(400);
			});
			$(".correctimg").animate({"width": "+=6px", "height": "+=6px"}, 300, function()
			{
				$(".correctimg").animate({"width": "-=6px", "height": "-=6px"}, 350);					
			});
			if (mute == true)
			{
				$('#nameform').submit();
			}
			return false;
		}
		else
		{
			$.post('/update/', {'test': 'test'}, function(data){
				alert(data.valid);
			});
			if (mute == false)
			{
				soundHandle2.load();
				soundHandle2.play();
			}
			$(this).unbind('click');
			$(".skipimg").fadeTo(500, 0.3).unbind('click');
			wrongAnswers += 1;
			if (skippable == true)
			{
				skippable = false;
			}
			$('#wrongnum').html(wrongAnswers);
			currentStreak = 0;
			$('#rownum').html(currentStreak + ", " + highestStreak);
			$(this).fadeTo(700, 0.35);
			$(".wrongimg").animate({"width": "+=5px", "height": "+=5px"}, 300, function()
			{
				$(".wrongimg").animate({"width": "-=5px", "height": "-=5px"}, 350);
			});
			return false;
		}*/
	});

	/*var options = {target: '#output', success: response};
	$('#nameform').ajaxForm(options);*/
}
