(() => {
	const container = document.getElementById('app-snackbar-container');
	const template = document.getElementById('app-snackbar-template');
	const variants = {
		success: {title: 'Success', icon: 'bx-check-circle', duration: 5500},
		error: {title: 'Something went wrong', icon: 'bx-error-circle', duration: 8500},
		info: {title: 'Information', icon: 'bx-info-circle', duration: 6500},
	};
	const maxVisible = 3;

	const normalizeType = (type) => {
		const tags = String(type || '').toLowerCase().split(/\s+/);
		if (tags.includes('success')) return 'success';
		if (tags.includes('error')) return 'error';
		return 'info';
	};

	const dismissSnackbar = (snackbar) => {
		if (!snackbar || snackbar.dataset.dismissed === 'true') return;
		snackbar.dataset.dismissed = 'true';
		window.clearTimeout(Number(snackbar.dataset.timerId));
		snackbar.classList.add('is-leaving');
		window.setTimeout(() => snackbar.remove(), 180);
	};

	const showSnackbar = (options = {}) => {
		if (!container || !template) return null;
		if (typeof options === 'string') options = {message: options};
		const {type = 'info', title, message = '', duration} = options || {};

		const variant = normalizeType(type);
		const settings = variants[variant];
		const snackbar = template.content.firstElementChild.cloneNode(true);
		const icon = snackbar.querySelector('[data-snackbar-icon]');
		const titleElement = snackbar.querySelector('[data-snackbar-title]');
		const messageElement = snackbar.querySelector('[data-snackbar-message]');
		const dismissButton = snackbar.querySelector('[data-snackbar-dismiss]');
		const timeout = Number.isFinite(duration) ? Math.max(0, duration) : settings.duration;

		snackbar.classList.add(`app-snackbar--${variant}`);
		snackbar.dataset.dismissed = 'false';
		snackbar.setAttribute('role', variant === 'error' ? 'alert' : 'status');
		snackbar.setAttribute('aria-live', variant === 'error' ? 'assertive' : 'polite');
		snackbar.setAttribute('aria-atomic', 'true');
		icon.className = `bx ${settings.icon}`;
		titleElement.textContent = title || settings.title;
		messageElement.textContent = message == null ? '' : String(message);
		messageElement.hidden = messageElement.textContent.length === 0;
		dismissButton.addEventListener('click', () => dismissSnackbar(snackbar));

		while (container.querySelectorAll('.app-snackbar').length >= maxVisible) {
			const oldestSnackbar = container.querySelector('.app-snackbar');
			window.clearTimeout(Number(oldestSnackbar.dataset.timerId));
			oldestSnackbar.remove();
		}

		container.append(snackbar);
		snackbar.classList.add('is-visible');

		let remaining = timeout;
		let startedAt = 0;
		let timerId = 0;
		const startTimer = () => {
			if (remaining <= 0 || timerId || snackbar.dataset.dismissed === 'true') return;
			startedAt = Date.now();
			timerId = window.setTimeout(() => dismissSnackbar(snackbar), remaining);
			snackbar.dataset.timerId = String(timerId);
		};
		const pauseTimer = () => {
			if (!timerId) return;
			window.clearTimeout(timerId);
			remaining = Math.max(0, remaining - (Date.now() - startedAt));
			timerId = 0;
			snackbar.dataset.timerId = '';
		};

		snackbar.addEventListener('mouseenter', pauseTimer);
		snackbar.addEventListener('mouseleave', startTimer);
		snackbar.addEventListener('focusin', pauseTimer);
		snackbar.addEventListener('focusout', (event) => {
			if (!snackbar.contains(event.relatedTarget)) startTimer();
		});
		startTimer();
		return snackbar;
	};

	window.showSnackbar = showSnackbar;
	window.EasyRides = window.EasyRides || {};
	window.EasyRides.showSnackbar = showSnackbar;

	const showDjangoMessages = () => {
		document.querySelectorAll('template[data-server-snackbar]').forEach((messageTemplate) => {
			showSnackbar({
				type: messageTemplate.dataset.type,
				message: messageTemplate.content.textContent.trim(),
			});
			messageTemplate.remove();
		});
	};

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', showDjangoMessages, {once: true});
	} else {
		showDjangoMessages();
	}
})();
