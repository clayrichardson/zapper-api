require.config({
	baseUrl: '/static/js',
	paths: {
		vendor: '../vendors/js',
		templates: '../templates',
		jquery: '../vendors/js/jquery',
		underscore: '../vendors/js/underscore',
		backbone: '../vendors/js/backbone'
	},
	shim: {
		'vendor/bootstrap.min': ['jquery'],
		'vendor/backbone': ['vendor/underscore']
	}
});

require([
	'jquery',
	'underscore',
	'backbone'
], function (
	$,
	_
) {
	'use strict';
});
