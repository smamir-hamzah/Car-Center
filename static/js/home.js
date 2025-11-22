/* home.js — adapted for Django template usage */

/* Modal handling: support separate login/signup overlays */
(function(){
	const loginOverlay = document.getElementById('loginOverlay');
	const signupOverlay = document.getElementById('signupOverlay');

	const loginBtn = document.getElementById('loginBtn') || document.getElementById('loginBtn2');
	const signupBtn = document.getElementById('signupBtn') || document.getElementById('signupBtn2');

	const loginClose = document.getElementById('loginClose');
	const signupClose = document.getElementById('signupClose');

	function openOverlay(ov){
		if(!ov) return;
		ov.classList.remove('hidden');
	}
	function closeOverlay(ov){
		if(!ov) return;
		ov.classList.add('hidden');
	}

	if(loginBtn){
		loginBtn.addEventListener('click', (e)=>{
			e.preventDefault();
			if(loginOverlay) openOverlay(loginOverlay);
		});
	}
	if(signupBtn){
		signupBtn.addEventListener('click', (e)=>{
			e.preventDefault();
			if(signupOverlay) openOverlay(signupOverlay);
		});
	}

	if(loginClose) loginClose.addEventListener('click', ()=> closeOverlay(loginOverlay));
	if(signupClose) signupClose.addEventListener('click', ()=> closeOverlay(signupOverlay));

	// booking modal close/cancel handling (if present)
	const bookingOverlay = document.getElementById('bookingOverlay');
	const bookingClose = document.getElementById('bookingClose');
	const bookingCancel = document.getElementById('bookingCancel');

	if(bookingClose) bookingClose.addEventListener('click', ()=> closeOverlay(bookingOverlay));
	if(bookingCancel) bookingCancel.addEventListener('click', (e)=>{ e.preventDefault(); closeOverlay(bookingOverlay); });

	[loginOverlay, signupOverlay].forEach(ov=>{
		if(!ov) return;
		ov.addEventListener('click', (e)=>{
			if(e.target === ov) closeOverlay(ov);
		});
	});

	document.addEventListener('keydown', (e)=>{
		if(e.key === 'Escape'){
			[loginOverlay, signupOverlay].forEach(ov=>{ 
				if(ov && !ov.classList.contains('hidden')) closeOverlay(ov); 
			});
		}
	});

	// simple demo submit handlers (index forms) — if you have real auth, let Django handle them
	const loginFormIndex = document.getElementById('loginFormIndex');
	if(loginFormIndex) loginFormIndex.addEventListener('submit', (e)=>{
		// Let form submit normally to server (comment out if you want demo dialog)
		// e.preventDefault();
		// alert('Logged in (demo)');
		// closeOverlay(loginOverlay);
	});

	const signupFormIndex = document.getElementById('signupFormIndex');
	if(signupFormIndex) signupFormIndex.addEventListener('submit', (e)=>{
		// Let form submit normally to server
	});
})();

/* Card navigation for DETAILS only */
(function(){
	document.querySelectorAll('.details-btn').forEach(btn => {
		btn.addEventListener('click', ()=>{
			const id = btn.dataset.id;
			// go to a dedicated details page or use query param — here we open a simple detail route
			window.location.href = `/car/${encodeURIComponent(id)}/`; // optional detail page you can create
		});
	});
})();

/* RENT and BUY now require LOGIN — open modal if clicked */
(function(){
	document.querySelectorAll('.rent-btn').forEach(btn=>{
		btn.addEventListener('click', ()=>{
			const bookingOverlay = document.getElementById('bookingOverlay');
			const loginOverlay = document.getElementById('loginOverlay');
			const carId = btn.dataset.id;
			if(bookingOverlay){
				// On user page: open booking modal and set car id
				bookingOverlay.classList.remove('mode-buy');
				const carInput = bookingOverlay.querySelector('input[name="car_id"]');
				if(carInput) carInput.value = carId;
				bookingOverlay.classList.remove('hidden');
			} else if(loginOverlay){
				// On home page (no booking modal available): show login
				loginOverlay.classList.remove('hidden');
			}
		});
	});

	document.querySelectorAll('.buy-btn').forEach(btn=>{
		btn.addEventListener('click', ()=>{
			const bookingOverlay = document.getElementById('bookingOverlay');
			const loginOverlay = document.getElementById('loginOverlay');
			const carId = btn.dataset.id;
			if(bookingOverlay){
				// Open booking modal in buy mode: hide rent-only fields
				bookingOverlay.classList.add('mode-buy');
				const carInput = bookingOverlay.querySelector('input[name="car_id"]');
				if(carInput) carInput.value = carId;
				bookingOverlay.classList.remove('hidden');
			} else if(loginOverlay){
				loginOverlay.classList.remove('hidden');
			}
		});
	});
})();

/* Search behavior (demo) */
(function(){
	const searchForm = document.getElementById('searchForm');
	if(!searchForm) return;

	searchForm.addEventListener('submit', (e)=>{
		e.preventDefault();
		const start = document.getElementById('startDate').value;
		const end = document.getElementById('endDate').value;
		const pickup = document.getElementById('pickup').value || 'anywhere';
		alert(`Searching cars from ${start || 'any'} to ${end || 'any'} at ${pickup} (demo)`);
	});
})();

/* Details page fetch — run only on a details page that includes detailImage element */
(function(){
	const detailImage = document.getElementById('detailImage');
	if(!detailImage) return;

	const params = new URLSearchParams(window.location.search);
	const id = params.get('id');
	if(!id){
		// fallback: try to parse id from path /car/<id>/
		const parts = window.location.pathname.split('/').filter(Boolean);
		if(parts.length && parts[0] === 'car' && parts[1]) id = parts[1];
	}

	if(!id) return;

	fetch(`/api/car/${encodeURIComponent(id)}/`)
		.then(res => {
			if(!res.ok) throw new Error('Car not found');
			return res.json();
		})
		.then(car => {
			const titleEl = document.getElementById('detailTitle');
			const descEl = document.getElementById('detailDesc');
			const priceEl = document.getElementById('detailPrice');
			if(titleEl) titleEl.textContent = car.title;
			if(descEl) descEl.textContent = car.description;
			if(priceEl) priceEl.textContent = car.price;
			if(detailImage) detailImage.src = car.image || '';

			const actionBtn = document.getElementById('primaryAction');
			if(actionBtn){
				actionBtn.textContent = (car.type === 'rent') ? 'Rent this car' : 'Buy this car';
				actionBtn.addEventListener('click', ()=>{
					alert(`${actionBtn.textContent} — proceed to checkout (demo).`);
				});
			}
		})
		.catch(err=>{
			console.error("Error loading car:", err);
		});
})();

/* reveal-on-scroll */
(function(){
	if (typeof IntersectionObserver === 'undefined') {
		document.querySelectorAll('.reveal').forEach(el => el.classList.add('in-view'));
		return;
	}

	const revealEls = document.querySelectorAll('.reveal');
	const io = new IntersectionObserver((entries) => {
		entries.forEach(entry => {
			if (entry.isIntersecting) {
				entry.target.classList.add('in-view');
			} else {
				entry.target.classList.remove('in-view');
			}
		});
	}, {
		threshold: [0.08, 0.2],
		rootMargin: '0px 0px -8% 0px'
	});

	revealEls.forEach(el => io.observe(el));
})();