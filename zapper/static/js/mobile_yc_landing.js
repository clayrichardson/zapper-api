var landing_jobs = {
	// the middle column needs to stay centered yet keep
	// an absolute position to have the opaque backdrop
	elem_positions: function () {
		var $footer_col = $('.footer-middle-col'),
			$footer_mound_shadow = $('.footer-mound-shadow'),
			footer_col_width = $footer_col.width(),
			footer_mound_width = $footer_mound_shadow.width(),
			center_elem = function (elem_width, $elem, window_width) {
				var left_gutter = (window_width - elem_width) / 2;

				$elem.css('margin-left', left_gutter + 'px');
			},
			resize_function = function () {
				var window_width = $(window).width();

				if (window_width < 320) {
					window_width = 320;
				}

				center_elem(footer_col_width, $footer_col, window_width);
				center_elem(footer_mound_width, $footer_mound_shadow, window_width);
			};

		$(window).resize(resize_function);
		$(window).bind('orientationchange', resize_function);
		resize_function();
	},


	// events on the footer including waitlist submission
	footer_events: function () {
		var $join_input = $('.join-form input'),
			$join_btn = $('.join-form a'),
			validate_email = function (email) {
				var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
				return re.test(email);
			};
		$join_input.focus(function () {
			$(this).attr('placeholder', 'john@example.com');
			$(this).addClass('active-placeholder');
		});
		$join_input.blur(function () {
			$(this).attr('placeholder', 'Join the Waiting List');
			$(this).removeClass('active-placeholder');
		});
		$join_input.keypress(function (e) {
			$join_input.removeClass('error');
			if (e.which === 13) {
				$join_btn.click();
			}
		});

		$join_btn.click(function () {
			var email = $join_input.val();

			if (validate_email(email)) {
				$.ajax({
					type: 'POST',
					url: '/api/v1/waitlist/',
					contentType: 'application/json',
					data: '{ "email": "' + email + '"}',
					beforeSend: function (xhr, settings) {
						function getCookie(name) {
							var cookieValue = null;
							if (document.cookie && document.cookie !== '') {
								var cookies = document.cookie.split(';');
								for (var i = 0; i < cookies.length; i++) {
									var cookie = $.trim(cookies[i]);
									if (cookie.substring(0, name.length + 1) == (name + '=')) {
										cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
										break;
									}
								}
							}
							return cookieValue;
						}

						if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
							xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
						}
					},
					success: function (response) {
						$('.join-form').hide();
						$('.zapper-share').show();
					}
				});
			} else {
				$join_input.addClass('error');
			}
			return false;
		});
	}
};

$(document).ready(function () {
	landing_jobs.elem_positions();
	landing_jobs.footer_events();
});

// storyboard animations of the ui pieces
$(document).ready(function () {
	var event_queue = [],
		currentAnimation,
		currentCondition,

		// allows for events to run in order
		// and for throttle-prevention
		event_ready = true,
		window_height = $(window).height(),
		footer_height = $('.footer').height();

	function queue(condition, animation) {
		event_queue.unshift({
			condition: condition,
			animation: animation
		});
	}

	function dequeue() {
		var currentEvent = event_queue.pop();

		if (currentEvent) {
			currentAnimation = currentEvent.animation;
			currentCondition = currentEvent.condition;
		} else {
			// nothing more to animate
			currentAnimation = currentCondition = undefined;
			$(window).off('scroll');
			$(window).off('resize');
			$(window).off('orientationchange');
			landing_jobs.elem_positions();
		}
	}

	function animate() {
		if (!currentAnimation) {
			dequeue();
			if (!currentAnimation) {
				return;
			}
		}

		if (event_ready && currentCondition()) {
			event_ready = false;
			currentAnimation();
			dequeue();
			animate();
		}
	}

	function initialize () {
		// logo and text fade
		queue(function () {
			return true;
		}, function () {
			$('.zapper-logo').animate({
				opacity: 100
			}, 10000);
			$('.tag-line').animate({
				opacity: 100
			}, 10000);

			window.setTimeout(function () {
				event_ready = true;
				animate();
			}, 500);
		});

		// app sample image fade in
		queue(function () {
			var scrollY = $(window).scrollTop(),
				dummyY = $('.dummy-app').offset().top;

			return (window_height + scrollY) >= dummyY;
		}, function () {
			$('.dummy-app').animate({
				opacity: 100
			}, {duration: 5000, queue: false});
			window.setTimeout(function () {
				event_ready = true;
				animate();
			}, 500);
		});

		// slide up footer
		queue(function () {
			return true;
		}, function () {
			$('.footer').animate({
				bottom: 0
			}, 500, function () {
				$('.footer-mound-shadow').show();
				event_ready = true;
				animate();
			});
		});

		// fade in bullet points
		function fadeBullet ($elem) {
			$elem.animate({
				opacity: 100
			}, {duration: 10000, queue: false});
			window.setTimeout(function () {
				event_ready = true;
				animate();
			}, 1000);
		}

		queue(function () {
			var scrollY = $(window).scrollTop(),
				bulletY = $('.bullet').first().offset().top;

			return (window_height + scrollY - footer_height) >= bulletY;
		}, function () {
			fadeBullet($('.bullet').first());
		});
		queue(function () {
			var scrollY = $(window).scrollTop(),
				bulletY = $($('.bullet').get(1)).offset().top;

			return (window_height + scrollY - footer_height) >= bulletY;
		}, function () {
			fadeBullet($($('.bullet').get(1)));
		});
		queue(function () {
			return true
		}, function () {
			fadeBullet($($('.bullet').get(2)));
		});
	}

	initialize();

	$(window).scroll(animate);
	$(window).resize(function () {
		var new_height = $(window).height();

		if (new_height > window_height) {
			animate();
		}

		window_height = new_height;
	});
	$(window).bind('orientationchange', animate);

	window.setTimeout(animate, 1000);
});
