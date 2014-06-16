/**
*	Global variables for the site.
*/

var url = "http://localhost:8000/"; //	For development.
var siteName = "Facegame";


casper.test.begin('Site functionality', 10, function suite(test) {
	casper.start(url, function() {
		
		/**
		*	Testing basic settings for the site.	
		*/
		test.assertHttpStatus(200, 'Connected to the main page');
		test.assertUrlMatch('/', 'URL is root');
		test.assertTitle(siteName, "sites title is the one expected");
		test.assertExists('form[id="nameform"]', "form for guessing is found");

		/**
		*	Guess every name in the form so the page is going to update the player at least once.
		*/

		this.click('#id_name_0');
	});

	casper.wait(500, function(){
		test.assertExists('form[id="nameform"]', "form for guessing is still found after first guess");
	});

	casper.then(function() {
		this.click('#id_name_1');
	});

	casper.wait(500, function(){
		test.assertExists('form[id="nameform"]', "form for guessing is still found after second guess");
	});

	casper.then(function() {
		this.click('#id_name_2');
	});

	casper.wait(500, function(){
		test.assertExists('form[id="nameform"]', "form for guessing is still found after third guess");
	});

	casper.then(function() {
		this.click('#id_name_3');
	});

	casper.wait(500, function(){
		test.assertExists('form[id="nameform"]', "form for guessing is still found after fourth guess");
	});

	casper.then(function() {
		this.click('#id_name_4');
	});

	casper.wait(500, function(){
		test.assertExists('form[id="nameform"]', "form for guessing is still found after fifth guess");
	});

	/**
	*	Switch the game mode.
	*/

	casper.then(function() {
		this.click('a');
	});

	casper.wait(500, function() {
		//	Check if the new url matches.
		test.assertUrlMatch('/name', 'URL is /name');
	});

	casper.run(function() {
		test.done();
	});

});
