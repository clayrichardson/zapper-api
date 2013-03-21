var landing_jobs = {
	// the middle column needs to stay centered yet keep
	// an absolute position to have the opaque backdrop
	elem_positions: function () {
		var $footer_col = $('.footer-middle-col'),
			$footer_mound_shadow = $('.footer-mound-shadow'),
			$team_col = $('.team-middle-col'),
			$team_bg = $('.team-bg'),
			footer_col_width = $footer_col.width(),
			footer_mound_width = $footer_mound_shadow.width(),
			center_elem = function (elem_width, $elem, window_width) {
				var left_gutter = (window_width - elem_width) / 2;

				$elem.css('margin-left', left_gutter + 'px');
			},
			resize_function = function () {
				var window_width = $(window).width();

				if (window_width < 1020) {
					return;
				}

				center_elem(footer_col_width, $footer_col, window_width);
				center_elem(footer_mound_width, $footer_mound_shadow, window_width);

				if (window_width < 1200) {
					if (window_width <= 1020) {
						window_width = 1020;
					}
					$team_bg.width(window_width);
				} else {
					$team_bg.width(1200);
				}

				$team_col.css('left', ((window_width - 1020) / 2) + 'px');
			};

		$(window).resize(resize_function);
		resize_function();
	},


	// events on the footer including waitlist submission
	footer_events: function () {
		var $join_input = $('.join-form input'),
			$join_btn = $('.join-form a');
		$join_input.focus(function () {
			$(this).attr('placeholder', 'john@example.com');
			$(this).addClass('active-placeholder');
		});
		$join_input.blur(function () {
			$(this).attr('placeholder', 'Join the Waiting List');
			$(this).removeClass('active-placeholder');
		});
		$join_input.keypress(function (e) {
			if (e.which === 13) {
				$join_btn.click();
			}
		});

		$join_btn.click(function () {
			var email = $join_input.val();
			// validate email
			// error or:
			// submit
			// error or:
			// success
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

		// app sample image expansion
		queue(function () {
			var scrollY = $(window).scrollTop(),
				dummyY = $('.dummy-app').offset().top;

			return (window_height + scrollY) >= dummyY;
		}, function () {
			$('.dummy-app').animate({
				width: '436px',
				height: '716px',
				'margin-left': '0px',
				'margin-right': '0px'
			}, {
				duration: 1000,
				complete: function () {
					event_ready = true;
					animate();
				},
				queue: false
			});
			$('.dummy-app').animate({
				opacity: 100
			}, {duration: 5000, queue: false});
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

		// slide and fade in first bullet
		queue(function () {
			var scrollY = $(window).scrollTop(),
				bulletY = $('.gutter.right .bullet').first().offset().top;
			return ((window_height / 2) + scrollY - footer_height) >= bulletY;
		}, function () {
			$('.gutter.right .bullet').first().animate({
				opacity: 100
			}, {duration: 10000, queue: false});
			$('.gutter.right .bullet').first().animate({
				'margin-left': '0px'
			}, {duration: 500, queue: false, easing: 'linear'});

			window.setTimeout(function () {
				event_ready = true;
				animate();
			}, 500);
		});

		// slide and fade in second bullet
		queue(function () {
			var scrollY = $(window).scrollTop(),
				bulletY = $('.gutter.left .bullet').offset().top;
			return ((window_height / 2) + scrollY - footer_height) >= bulletY;
		}, function () {
			$('.gutter.left .bullet').animate({
				opacity: 100
			}, {duration: 10000, queue: false});
			$('.gutter.left .bullet').animate({
				'margin-right': '0px'
			}, {duration: 500, queue: false, easing: 'linear'});

			window.setTimeout(function () {
				event_ready = true;
				animate();
			}, 500);
		});

		// slide and fade in third bullet
		queue(function () {
			var scrollY = $(window).scrollTop(),
				bulletY = $($('.gutter.right .bullet').get(1)).offset().top;
			return ((window_height / 2) + scrollY - footer_height) >= bulletY;
		}, function () {
			$($('.gutter.right .bullet').get(1)).animate({
				opacity: 100
			}, {duration: 10000, queue: false});
			$($('.gutter.right .bullet').get(1)).animate({
				'margin-left': '0px'
			}, {duration: 500, queue: false, easing: 'linear'});

			window.setTimeout(function () {
				event_ready = true;
				animate();
			}, 500);
		});

		// fade in background of team section
		queue(function () {
			var scrollY = $(window).scrollTop(),
				team_bgY = $('.team-bg').offset().top;
			return ((window_height / 2) + scrollY - footer_height) >= team_bgY;
		}, function () {
			$('.team-bg').animate({
				opacity: 100
			}, 10000);

			window.setTimeout(function () {
				event_ready = true;
				animate();
			}, 500);
		});

		// bubble the avatars
		function bubbleAnimation ($avatar) {
			window.setTimeout(function () {
				$avatar.animate({
					width: '198px',
					height: '198px',
					'border-radius': '99px',
					'margin': '0 21px'
				}, {
					duration: 125,
					queue: false,
					complete: function () {
						$avatar.animate({
							width: '180px',
							height: '180px',
							'border-radius': '90px',
							'margin': '0 30px'
						}, {
							duration: 250,
							queue: false,
							complete: function () {
								$avatar.addClass('bubbled');
							}
						});
					}
				});
			}, 500);

			window.setTimeout(function () {
				event_ready = true;
				animate();
			}, 375);
		}
		queue(function () {
			return true;
		}, function () {
			bubbleAnimation($('.avatar').first());
		});
		queue(function () {
			return true;
		}, function () {
			bubbleAnimation($($('.avatar').get(1)));
		});
		queue(function () {
			return true;
		}, function () {
			bubbleAnimation($($('.avatar').get(2)));
		});
		queue(function () {
			return true;
		}, function () {
			bubbleAnimation($($('.avatar').get(3)));
		});

		// slide names and titles up and meet tagline down
		queue(function () {
			return true;
		}, function () {
			$('.bio-entry').animate({
				'margin-top': '0px'
			}, {
				duration: 500,
				queue: false,
				complete: function () {
					event_ready = true;
					animate();
				}
			});

			$('.meet-line').animate({
				'margin-top': '0px'
			}, {
				duration: 500,
				queue: false
			});

			$('.meet-line').animate({
				opacity: 100
			}, {duration: 10000, queue: false});
			$('.bio-entry').animate({
				opacity: 100
			}, {duration: 10000, queue: false});

			$('.avatar-row').animate({
				'margin-top': '50px'
			}, {
				duration: 500,
				queue: false
			});
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

	window.setTimeout(animate, 1000);
});
