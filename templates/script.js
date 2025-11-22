// Shared dataset for car details
const CAR_DATA = {
	r1: { id:'r1', title:'CityCruise LX', price:'$49 / day', img:'https://picsum.photos/seed/r1/1200/720', desc:'Compact and efficient — perfect for city trips. Automatic, AC, good mileage.', type:'rent' },
	r2: { id:'r2', title:'UrbanSport GT', price:'$79 / day', img:'https://picsum.photos/seed/r2/1200/720', desc:'Sporty handling with premium features. Ideal for weekend getaways.', type:'rent' },
	r3: { id:'r3', title:'EcoRide S', price:'$39 / day', img:'https://picsum.photos/seed/r3/1200/720', desc:'Fuel efficient and eco-friendly. Great for budget trips.', type:'rent' },
	r4: { id:'r4', title:'Comfort XL', price:'$89 / day', img:'https://picsum.photos/seed/r4/1200/720', desc:'Spacious and luxurious interior for family travel.', type:'rent' },

	s1: { id:'s1', title:'RoadMaster 2022', price:'$28,900', img:'https://picsum.photos/seed/s1/1200/720', desc:'Reliable midsize sedan with modern conveniences and warranty.', type:'sale' },
	s2: { id:'s2', title:'Volt EV', price:'$34,500', img:'https://picsum.photos/seed/s2/1200/720', desc:'Electric vehicle with fast charging and advanced safety tech.', type:'sale' },
	s3: { id:'s3', title:'Classic Coupe', price:'$24,700', img:'https://picsum.photos/seed/s3/1200/720', desc:'Stylish coupe with punchy engine and refined interior.', type:'sale' },
	s4: { id:'s4', title:'FamilyVan Pro', price:'$21,200', img:'https://picsum.photos/seed/s4/1200/720', desc:'Roomy van for family needs, great cargo and comfort.', type:'sale' }
};

/* Modal handling: support separate login/signup overlays on index.html
   and also fallback to a generic modalOverlay (used by car-details.html) */
(function(){
	const loginOverlay = document.getElementById('loginOverlay');
	const signupOverlay = document.getElementById('signupOverlay');
	const genericOverlay = document.getElementById('modalOverlay'); // for other pages

	const loginBtn = document.getElementById('loginBtn') || document.getElementById('loginBtn2');
	const signupBtn = document.getElementById('signupBtn') || document.getElementById('signupBtn2');

	// close buttons
	const loginClose = document.getElementById('loginClose');
	const signupClose = document.getElementById('signupClose');
	const genericClose = document.querySelector('#modalOverlay .modal-close');

	// helper open/close
	function openOverlay(ov){
		if(!ov) return;
		ov.classList.remove('hidden');
	}
	function closeOverlay(ov){
		if(!ov) return;
		ov.classList.add('hidden');
	}

	// index header buttons: prefer separate overlays if present
	if(loginBtn){
		loginBtn.addEventListener('click', (e)=>{
			e.preventDefault();
			if(loginOverlay) openOverlay(loginOverlay);
			else if(genericOverlay){
				// fallback: show generic and ensure login form visible
				openOverlay(genericOverlay);
				const lf = genericOverlay.querySelector('#loginForm');
				const sf = genericOverlay.querySelector('#signupForm');
				if(lf) lf.classList.remove('hidden');
				if(sf) sf.classList.add('hidden');
			}
		});
	}
	if(signupBtn){
		signupBtn.addEventListener('click', (e)=>{
			e.preventDefault();
			if(signupOverlay) openOverlay(signupOverlay);
			else if(genericOverlay){
				openOverlay(genericOverlay);
				const lf = genericOverlay.querySelector('#loginForm');
				const sf = genericOverlay.querySelector('#signupForm');
				if(sf) sf.classList.remove('hidden');
				if(lf) lf.classList.add('hidden');
			}
		});
	}

	// close handlers
	if(loginClose) loginClose.addEventListener('click', ()=> closeOverlay(loginOverlay));
	if(signupClose) signupClose.addEventListener('click', ()=> closeOverlay(signupOverlay));
	if(genericClose) genericClose.addEventListener('click', ()=> closeOverlay(genericOverlay));

	// overlay click to close (for each overlay)
	[loginOverlay, signupOverlay, genericOverlay].forEach(ov=>{
		if(!ov) return;
		ov.addEventListener('click', (e)=>{
			if(e.target === ov) closeOverlay(ov);
		});
	});

	// ESC to close any open overlay
	document.addEventListener('keydown', (e)=>{
		if(e.key === 'Escape'){
			[loginOverlay, signupOverlay, genericOverlay].forEach(ov=>{ if(ov && !ov.classList.contains('hidden')) closeOverlay(ov); });
		}
	});

	// simple demo submit handlers (index forms)
	const loginFormIndex = document.getElementById('loginFormIndex');
	if(loginFormIndex) loginFormIndex.addEventListener('submit', (e)=>{ e.preventDefault(); alert('Logged in (demo)'); closeOverlay(loginOverlay); });

	const signupFormIndex = document.getElementById('signupFormIndex');
	if(signupFormIndex) signupFormIndex.addEventListener('submit', (e)=>{ e.preventDefault(); alert('Account created (demo)'); closeOverlay(signupOverlay); });
})();

/* Card action navigation */
(function(){
	const actionBtns = document.querySelectorAll('.action-btn');
	actionBtns.forEach(btn=>{
		btn.addEventListener('click', (e)=>{
			const id = btn.dataset.id;
			if(!id) return;
			// go to details with id param
			window.location.href = `car-details.html?id=${encodeURIComponent(id)}`;
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

/* Populate details page if present */
(function(){
	// only run on details page
	const detailImage = document.getElementById('detailImage');
	if(!detailImage) return;

	const params = new URLSearchParams(window.location.search);
	const id = params.get('id') || 's1';
	const car = CAR_DATA[id] || CAR_DATA['s1'];

	// populate DOM
	document.getElementById('detailTitle').textContent = car.title;
	document.getElementById('detailDesc').textContent = car.desc;
	document.getElementById('detailPrice').textContent = car.price;
	detailImage.src = car.img;
	const actionBtn = document.getElementById('primaryAction');
	actionBtn.textContent = (car.type === 'rent') ? 'Rent this car' : 'Buy this car';
	actionBtn.addEventListener('click', ()=>{
		alert(`${actionBtn.textContent} — proceed to checkout (demo).`);
	});

	/* reuse modal triggers from details page header */
	const loginBtn2 = document.getElementById('loginBtn2');
	const signupBtn2 = document.getElementById('signupBtn2');
	if(loginBtn2) loginBtn2.addEventListener('click', ()=> document.getElementById('modalOverlay').classList.remove('hidden'));
	if(signupBtn2) signupBtn2.addEventListener('click', ()=> document.getElementById('modalOverlay').classList.remove('hidden'));
})();

/* reveal-on-scroll: observe elements with .reveal and toggle .in-view on enter/leave
   (so animations run every time you scroll up/down) */
(function(){
	// guard
	if (typeof IntersectionObserver === 'undefined') {
		document.querySelectorAll('.reveal').forEach(el => el.classList.add('in-view'));
		return;
	}

	const revealEls = document.querySelectorAll('.reveal');
	if (revealEls.length === 0) return;

	const io = new IntersectionObserver((entries) => {
		entries.forEach(entry => {
			const el = entry.target;
			if (entry.isIntersecting && entry.intersectionRatio > 0.08) {
				el.classList.add('in-view');
			} else {
				el.classList.remove('in-view');
			}
		});
	}, {
		threshold: [0.08, 0.2],
		rootMargin: '0px 0px -8% 0px'
	});

	revealEls.forEach(el => io.observe(el));
})();

/* Billing toggle + Get Pro button handling (updated: smooth sliding switch) */
(function(){
	const billingToggle = document.getElementById('billingToggle');
	const planPrices = document.querySelectorAll('.plan-price');
	let yearly = false; // default monthly

	function updatePrices(){
		planPrices.forEach(p=>{
			const m = p.dataset.month;
			const y = p.dataset.year;
			if(yearly){
				p.textContent = `$${y} / yr`;
			} else {
				p.textContent = `$${m} / mo`;
			}
		});
	}

	if(billingToggle){
		// click/tap
		billingToggle.addEventListener('click', ()=>{
			yearly = !yearly;
			billingToggle.setAttribute('aria-checked', yearly ? 'true' : 'false');
			updatePrices();
		});
		// keyboard: space or enter
		billingToggle.addEventListener('keydown', (e)=>{
			if(e.key === 'Enter' || e.key === ' '){
				e.preventDefault();
				yearly = !yearly;
				billingToggle.setAttribute('aria-checked', yearly ? 'true' : 'false');
				updatePrices();
			}
		});
		// initialize visual state
		billingToggle.setAttribute('aria-checked', yearly ? 'true' : 'false');
		updatePrices();
	}

	// wire Get buttons to open signup overlay (or fallback)
	document.querySelectorAll('.get-btn').forEach(btn=>{
		btn.addEventListener('click', (e)=>{
			const target = btn.dataset.target || 'signupOverlay';
			const ov = document.getElementById(target) || document.getElementById('modalOverlay');
			if(ov) ov.classList.remove('hidden');
			setTimeout(()=>{
				const input = ov && ov.querySelector('input');
				if(input) input.focus();
			}, 120);
		});
	});
})();
