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

	// buy booking modal close/cancel handling (separate modal)
	const buyBookingOverlay = document.getElementById('buyBookingOverlay');
	const buyBookingClose = document.getElementById('buyBookingClose');
	const buyBookingCancel = document.getElementById('buyBookingCancel');

	if(buyBookingClose) buyBookingClose.addEventListener('click', ()=> closeOverlay(buyBookingOverlay));
	if(buyBookingCancel) buyBookingCancel.addEventListener('click', (e)=>{ e.preventDefault(); closeOverlay(buyBookingOverlay); });

	[loginOverlay, signupOverlay, bookingOverlay, buyBookingOverlay].forEach(ov=>{
		if(!ov) return;
		ov.addEventListener('click', (e)=>{
			if(e.target === ov) closeOverlay(ov);
		});
	});

	document.addEventListener('keydown', (e)=>{
		if(e.key === 'Escape'){
			[loginOverlay, signupOverlay, bookingOverlay, buyBookingOverlay].forEach(ov=>{ 
				if(ov && !ov.classList.contains('hidden')) closeOverlay(ov); 
			});
		}
	});
})();

/* Card navigation for DETAILS only */
(function(){
	document.querySelectorAll('.details-btn').forEach(btn => {
		btn.addEventListener('click', ()=>{
			const id = btn.dataset.id;
			window.location.href = `/car/${encodeURIComponent(id)}/`;
		});
	});
})();

/* RENT and BUY now require LOGIN — open modal if clicked */
(function(){

	/* ---------------- RENT BUTTON ---------------- */
	document.querySelectorAll('.rent-btn').forEach(btn=>{
		btn.addEventListener('click', ()=>{
			const bookingOverlay = document.getElementById('bookingOverlay');
			const loginOverlay = document.getElementById('loginOverlay');
			const carId = btn.dataset.id;

			if(bookingOverlay){
				// Open rent booking modal
				const carInput = bookingOverlay.querySelector('input[name="car_id"]');
				if(carInput) carInput.value = carId;

				const typeInput = bookingOverlay.querySelector('input[name="request_type"]');
				if(typeInput) typeInput.value = 'rent';

				bookingOverlay.classList.remove('hidden');
			}
			else if(loginOverlay){
				loginOverlay.classList.remove('hidden');
			}
		});
	});


	/* ---------------- BUY BUTTON — FIXED VERSION ---------------- */
	document.querySelectorAll('.buy-btn').forEach(btn=>{
		btn.addEventListener('click', ()=>{
			const buyBookingOverlay = document.getElementById('buyBookingOverlay');
			const loginOverlay = document.getElementById('loginOverlay');
			const carId = btn.dataset.id;

			if(buyBookingOverlay){

				// Set car ID
				const carInput = buyBookingOverlay.querySelector('input[name="car_id"]');
				if(carInput) carInput.value = carId;

				// ⭐ FIXED: Make sure BUY request_type is always set
				const typeInput = buyBookingOverlay.querySelector('input[name="request_type"]');
				if(typeInput) typeInput.value = 'buy';

				// Open modal
				buyBookingOverlay.classList.remove('hidden');
			}
			else if(loginOverlay){
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

/* Details page fetch */
(function(){
	const detailImage = document.getElementById('detailImage');
	if(!detailImage) return;

	let id = new URLSearchParams(window.location.search).get('id');
	if(!id){
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


document.addEventListener("DOMContentLoaded", function () {

    // -------------------------
    // RENT MODAL
    // -------------------------
    document.querySelectorAll('.rent-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const overlay = document.getElementById('bookingOverlay');
            const form = document.getElementById('bookingForm');
            
            form.querySelector('input[name="car_id"]').value = btn.dataset.id;
            form.querySelector('input[name="request_type"]').value = "rent";

            overlay.classList.remove('hidden');
        });
    });

    document.getElementById('bookingClose').onclick = () => {
        document.getElementById('bookingOverlay').classList.add('hidden');
    };
    document.getElementById('bookingCancel').onclick = () => {
        document.getElementById('bookingOverlay').classList.add('hidden');
    };


    // -------------------------
    // BUY MODAL (FIXED)
    // -------------------------
    document.querySelectorAll('.buy-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const overlay = document.getElementById('buyBookingOverlay');
            const form = document.getElementById('buyBookingForm');

            // FIX 1 → set correct car_id only for BUY form
            form.querySelector('input[name="car_id"]').value = btn.dataset.id;

            // FIX 2 → force request_type = buy
            form.querySelector('input[name="request_type"]').value = "buy";

            overlay.classList.remove('hidden');
        });
    });

    document.getElementById('buyBookingClose').onclick = () => {
        document.getElementById('buyBookingOverlay').classList.add('hidden');
    };

    document.getElementById('buyBookingCancel').onclick = () => {
        document.getElementById('buyBookingOverlay').classList.add('hidden');
    };

});

/* Star Rating Selector Enhancement */
(function(){
	const starInput = document.getElementById('starInput');
	if(!starInput) return;
	
	const labels = starInput.querySelectorAll('label');
	const radios = starInput.querySelectorAll('input[type="radio"]');
	
	// Set initial state
	const checkedRadio = starInput.querySelector('input[type="radio"]:checked');
	if(checkedRadio){
		const checkedValue = parseInt(checkedRadio.value);
		updateStarDisplay(checkedValue);
	}
	
	// Handle hover effects
	labels.forEach((label, index) => {
		label.addEventListener('mouseenter', () => {
			const value = parseInt(radios[index].value);
			updateStarDisplay(value);
		});
		
		label.addEventListener('click', () => {
			radios[index].checked = true;
			const value = parseInt(radios[index].value);
			updateStarDisplay(value);
		});
	});
	
	starInput.addEventListener('mouseleave', () => {
		const checkedRadio = starInput.querySelector('input[type="radio"]:checked');
		if(checkedRadio){
			const value = parseInt(checkedRadio.value);
			updateStarDisplay(value);
		}
	});
	
	function updateStarDisplay(rating){
		labels.forEach((label, index) => {
			if(index < rating){
				label.style.color = '#fbbf24';
				label.style.textShadow = '0 0 8px rgba(251, 191, 36, 0.5)';
			} else {
				label.style.color = 'rgba(230, 238, 248, 0.3)';
				label.style.textShadow = 'none';
			}
		});
	}
})();

