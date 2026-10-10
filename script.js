    document.addEventListener('DOMContentLoaded', () => {

        // 1. Navbar Scroll Effect for Transparent to Blur Gradient Transition
        const navbar = document.getElementById('navbar');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 40) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        // 2. Mobile Hamburger Menu Drawer Toggle
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileDrawer = document.getElementById('mobile-drawer');
        const mobileDrawerClose = document.getElementById('mobile-drawer-close');
        const mobileLinks = document.querySelectorAll('.mobile-link');

        if(mobileMenuBtn && mobileDrawer) {
            mobileMenuBtn.addEventListener('click', () => {
                mobileDrawer.classList.add('active');
            });
        }

        if(mobileDrawerClose) {
            mobileDrawerClose.addEventListener('click', () => {
                mobileDrawer.classList.remove('active');
            });
        }

        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                if(mobileDrawer) mobileDrawer.classList.remove('active');
            });
        });

        // 3. Opening Welcome Video Popup (Shows ONLY on initial website open, NOT on reload)
        const welcomePopup = document.getElementById('welcome-popup');
        const openingVideo = document.getElementById('opening-video');
        const closeWelcomeBtn = document.getElementById('close-welcome');
        const enterSiteBtn = document.getElementById('enter-site-btn');
        const welcomeBookBtn = document.getElementById('welcome-book-btn');
        const inquiryModal = document.getElementById('inquiry-modal');

        // Detect if this page load is a reload or a revisit in the current browser session
        const navEntry = window.performance && performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
        const isPageReload = (navEntry && navEntry.type === 'reload') || (window.performance && performance.navigation && performance.navigation.type === 1);
        const hasAlreadySeenIntro = sessionStorage.getItem('spirit_intro_played') === 'true';

        const closeWelcomePopup = () => {
            if(welcomePopup) {
                if(openingVideo) {
                    openingVideo.pause();
                }
                welcomePopup.classList.add('hidden');
                document.documentElement.classList.add('skip-intro');
            }
            sessionStorage.setItem('spirit_intro_played', 'true');
        };

        const unmuteBtn = document.getElementById('video-unmute-btn');

        const ensureUnmuted = () => {
            if (openingVideo) {
                openingVideo.muted = false;
                openingVideo.volume = 1.0;
                if (openingVideo.paused) {
                    openingVideo.play().catch(() => {});
                }
            }
            if (unmuteBtn) unmuteBtn.style.display = 'none';
        };

        // Unmute immediately on any user interaction with the window/modal
        ['click', 'touchstart', 'pointerdown', 'keydown'].forEach(evtType => {
            window.addEventListener(evtType, () => {
                if (welcomePopup && !welcomePopup.classList.contains('hidden')) {
                    ensureUnmuted();
                }
            }, { capture: true });
        });

        if (unmuteBtn) {
            unmuteBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                ensureUnmuted();
            });
        }

        // If reloading the website or already visited in this session, skip the opening video completely
        if (isPageReload || hasAlreadySeenIntro) {
            if (welcomePopup) {
                welcomePopup.classList.add('hidden');
                if (openingVideo) {
                    openingVideo.pause();
                    openingVideo.removeAttribute('autoplay');
                }
            }
            document.documentElement.classList.add('skip-intro');
            sessionStorage.setItem('spirit_intro_played', 'true');
        } else {
            // First time opening the website: mark as seen and play video with full sound on load
            sessionStorage.setItem('spirit_intro_played', 'true');
            window.addEventListener('load', () => {
                if (welcomePopup && openingVideo && !welcomePopup.classList.contains('hidden') && !document.documentElement.classList.contains('skip-intro')) {
                    openingVideo.muted = false;
                    openingVideo.volume = 1.0;
                    const playPromise = openingVideo.play();
                    if (playPromise !== undefined) {
                        playPromise.then(() => {
                            ensureUnmuted();
                        }).catch(error => {
                            console.log("Browser policy restricted unmuted autoplay before user interaction:", error);
                            // Temporarily allow playback while displaying the prominent Sound button
                            openingVideo.muted = true;
                            openingVideo.play().then(() => {
                                if (unmuteBtn) unmuteBtn.style.display = 'inline-flex';
                            }).catch(() => {});
                        });
                    }
                }
            });
        }

        // Function to manually re-watch the opening video if desired
        window.replayOpeningVideo = () => {
            if (welcomePopup && openingVideo) {
                document.documentElement.classList.remove('skip-intro');
                welcomePopup.classList.remove('hidden');
                openingVideo.currentTime = 0;
                ensureUnmuted();
                openingVideo.play().catch(() => {
                    ensureUnmuted();
                });
            }
        };

        if(openingVideo) {
            openingVideo.addEventListener('ended', () => {
                closeWelcomePopup();
            });
        }

        if(closeWelcomeBtn) {
            closeWelcomeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                closeWelcomePopup();
            });
        }

        if(enterSiteBtn) {
            enterSiteBtn.addEventListener('click', (e) => {
                e.preventDefault();
                closeWelcomePopup();
            });
        }

        // Opens Enquiry Modal when "Enquiry Now" is clicked on the Welcome Popup
        if(welcomeBookBtn) {
            welcomeBookBtn.addEventListener('click', (e) => {
                e.preventDefault();
                closeWelcomePopup();
                if(inquiryModal) {
                    inquiryModal.classList.remove('hidden');
                    inquiryModal.classList.add('active');
                }
            });
        }
        
        window.addEventListener('click', (e) => {
            if (e.target === welcomePopup) {
                closeWelcomePopup();
            }
        });

        // 4. Scroll Reveal Animation Observer
        const reveals = document.querySelectorAll('.reveal');
        const revealOnScroll = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15, rootMargin: "0px 0px -50px 0px" });

        reveals.forEach(reveal => revealOnScroll.observe(reveal));

        // 5. Show More / Show Less Photos Toggle Logic
        const togglePhotosBtn = document.getElementById('toggle-photos-btn');
        const hiddenPhotos = document.querySelectorAll('.hidden-photo');
        const galleryInstaBtn = document.getElementById('gallery-insta-btn');

        if(togglePhotosBtn) {
            let isExpanded = false;
            togglePhotosBtn.addEventListener('click', () => {
                isExpanded = !isExpanded;
                hiddenPhotos.forEach(photo => {
                    if(isExpanded) photo.classList.add('revealed');
                    else photo.classList.remove('revealed');
                });

                // Reveal / Hide Animated Instagram button synchronously with photos expansion
                if(galleryInstaBtn) {
                    if(isExpanded) {
                        galleryInstaBtn.classList.add('revealed');
                    } else {
                        galleryInstaBtn.classList.remove('revealed');
                    }
                }

                if(isExpanded) {
                    togglePhotosBtn.innerHTML = 'Show Less Photos <i class="fas fa-chevron-up" id="toggle-icon"></i>';
                } else {
                    togglePhotosBtn.innerHTML = 'Show More Photos <i class="fas fa-chevron-down" id="toggle-icon"></i>';
                    document.getElementById('gallery').scrollIntoView({ behavior: 'smooth' });
                }
            });
        }

        // Toggle More/Less Reviews Logic
        const toggleReviewsBtn = document.getElementById('toggle-reviews-btn');
        const hiddenReviews = document.querySelectorAll('.hidden-review');

        if(toggleReviewsBtn) {
            let isReviewsExpanded = false;
            toggleReviewsBtn.addEventListener('click', () => {
                isReviewsExpanded = !isReviewsExpanded;
                hiddenReviews.forEach(review => {
                    if(isReviewsExpanded) review.classList.add('revealed');
                    else review.classList.remove('revealed');
                });

                if(isReviewsExpanded) {
                    toggleReviewsBtn.innerHTML = 'Show Less Reviews <i class="fas fa-chevron-up"></i>';
                } else {
                    toggleReviewsBtn.innerHTML = 'Show More Reviews <i class="fas fa-chevron-down"></i>';
                    document.getElementById('reviews').scrollIntoView({ behavior: 'smooth' });
                }
            });
        }

        // 6. Photo Gallery Lightbox Zoom Up Modal Logic
        const lightboxModal = document.getElementById('lightbox-modal');
        const lightboxImg = document.getElementById('lightbox-img');
        const lightboxClose = document.getElementById('lightbox-close');
        
        document.addEventListener('click', (e) => {
            const photoItem = e.target.closest('.photo-item');
            if (photoItem) {
                const img = photoItem.querySelector('img');
                if(lightboxModal && lightboxImg && img) {
                    lightboxImg.src = img.src;
                    lightboxModal.classList.add('active');
                }
            }
        });

        const closeLightbox = () => {
            if(lightboxModal) lightboxModal.classList.remove('active');
        };

        if(lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
        if(lightboxModal) {
            lightboxModal.addEventListener('click', (e) => {
                if(e.target === lightboxModal) closeLightbox();
            });
        }

        // 7. Separate Modals for Online Booking vs Enquiry Form
        const onlineBookingModal = document.getElementById('booking-modal');
        const closeBookingBtn = document.getElementById('close-modal');
        const closeInquiryBtn = document.getElementById('close-inquiry');

        const onlineBookingTriggers = document.querySelectorAll('.book-online-trigger');
        const inquiryTriggers = document.querySelectorAll('.inquiry-trigger');

        onlineBookingTriggers.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                if(mobileDrawer) mobileDrawer.classList.remove('active'); 
                window.location.href = 'booking.html';
            });
        });

        // Helper to reset and open the expanded enquiry form modal
        const openInquiryModal = () => {
            if (inquiryModal) {
                const formBody = document.getElementById('inquiry-form-body');
                const successCard = document.getElementById('inquiry-success-state');
                const dateInput = document.getElementById('inq-date');
                if (formBody) formBody.style.display = 'block';
                if (successCard) successCard.style.display = 'none';

                // Set default travel date to 7 days in the future if not chosen
                if (dateInput && !dateInput.value) {
                    const nextWeek = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
                    dateInput.value = nextWeek.toISOString().split('T')[0];
                }

                inquiryModal.classList.remove('hidden');
                inquiryModal.classList.add('active');

                const nameInput = document.getElementById('inq-name');
                if (nameInput) setTimeout(() => nameInput.focus(), 250);
            }
        };

        inquiryTriggers.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                if(mobileDrawer) mobileDrawer.classList.remove('active'); 
                openInquiryModal();
            });
        });

        // Global helper for closing and resetting modal
        window.resetInquiryModalState = function() {
            if (inquiryModal) {
                inquiryModal.classList.remove('active');
                setTimeout(() => {
                    const formBody = document.getElementById('inquiry-form-body');
                    const successCard = document.getElementById('inquiry-success-state');
                    const form = document.getElementById('inquiry-form');
                    if (form) form.reset();
                    if (formBody) formBody.style.display = 'block';
                    if (successCard) successCard.style.display = 'none';
                }, 300);
            }
        };

        if(closeBookingBtn) {
            closeBookingBtn.addEventListener('click', () => onlineBookingModal.classList.remove('active'));
        }
        if(closeInquiryBtn) {
            closeInquiryBtn.addEventListener('click', () => window.resetInquiryModalState());
        }

        window.addEventListener('click', (e) => {
            if (e.target === onlineBookingModal) onlineBookingModal.classList.remove('active');
            if (e.target === inquiryModal) window.resetInquiryModalState();
        });

        // Form Submissions & Razorpay Test Integration
        const bookingForm = document.getElementById('booking-form');
        if(bookingForm) {
            bookingForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                onlineBookingModal.classList.remove('active');

                const customerNameInput = document.getElementById('booking-name');
                const customerEmailInput = document.getElementById('booking-email');
                const customerPhoneInput = document.getElementById('booking-phone');
                const packageSelect = document.getElementById('booking-package');

                const name = customerNameInput ? customerNameInput.value : "Valued Traveler";
                const email = customerEmailInput ? customerEmailInput.value : "traveler@spiritadventures.in";
                const phone = customerPhoneInput ? customerPhoneInput.value : "9876543210";
                
                let packagePrice = 5000; 
                let selectedPkgName = "Coorg Getaway";
                if (packageSelect) {
                    const val = packageSelect.value;
                    if (val === 'goa') { packagePrice = 8500; selectedPkgName = "Goa Beach Trip"; }
                    else if (val === 'hampi') { packagePrice = 9500; selectedPkgName = "Hampi, Gokarna & Dandeli"; }
                    else if (val === 'ooty') { packagePrice = 14000; selectedPkgName = "Kodaikanal, Ooty & Mysore"; }
                }

                startRazorpayTestPayment(name, email, phone, selectedPkgName, packagePrice);
                bookingForm.reset();
            });
        }

        // Razorpay Test Payment Handler Function with Explicit UPI & QR Enabled
        function startRazorpayTestPayment(name, email, phone, packageName, priceInINR) {
            const amountInPaise = priceInINR * 100;

            var options = {
                "key": "rzp_test_TizOmS3RQSBbdm", 
                "amount": amountInPaise, 
                "currency": "INR",
                "name": "Spirit",
                "description": "Booking: " + packageName,
                "image": "Assests/img/logo.png",
                "handler": function (response){
                    alert("🎉 Test Payment Successful!\nPayment ID: " + response.razorpay_payment_id + "\nYour slot for " + packageName + " is confirmed!");
                },
                "prefill": {
                    "name": name,
                    "email": email,
                    "contact": phone
                },
                "config": {
                    "display": {
                        "blocks": {
                            "banks": {
                                "name": "Pay via UPI, QR & More",
                                "instruments": [
                                    { "method": "upi" },
                                    { "method": "qr" },
                                    { "method": "card" },
                                    { "method": "netbanking" }
                                ]
                            }
                        },
                        "sequence": ["block.banks"],
                        "preferences": {
                            "show_default_blocks": true
                        }
                    }
                },
                "notes": {
                    "address": "Spirit Booking Portal - Test Mode"
                },
                "theme": {
                    "color": "#136a6e"
                }
            };

            if (typeof window.Razorpay === "undefined") {
                alert("Razorpay SDK is loading or missing. Please check your internet connection.");
                return;
            }

            var rzp1 = new window.Razorpay(options);
            
            rzp1.on('payment.failed', function (response){
                alert("Payment simulation failed: " + response.error.description);
            });

            rzp1.open();
        }

        // Enquiry Form Submission with Real-Time Admin Sync & SheetDB Persistence
        const inquiryForm = document.getElementById('inquiry-form');
        if(inquiryForm) {
            inquiryForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const submitBtn = inquiryForm.querySelector('button[type="submit"]');
                const originalBtnText = submitBtn ? submitBtn.innerHTML : "Submit Trip Enquiry";
                if(submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting Enquiry...';
                }

                // 1. Extract All Fields from Expanded Enquiry Form
                const name = (document.getElementById('inq-name')?.value || '').trim() || 'Valued Traveler';
                const phone = (document.getElementById('inq-phone')?.value || '').trim() || 'N/A';
                const email = (document.getElementById('inq-email')?.value || '').trim() || 'N/A';
                const selectedPkg = (document.getElementById('inq-pkg')?.value || '').trim() || 'Custom Tour';
                const travelDate = (document.getElementById('inq-date')?.value || '').trim() || 'Upcoming';
                const travelers = (document.getElementById('inq-pax')?.value || '').trim() || '2 Persons';
                const pickupCity = (document.getElementById('inq-city')?.value || '').trim() || 'Bangalore';
                const tripStyle = (document.getElementById('inq-style')?.value || '').trim() || 'Adventure';
                const message = (document.getElementById('inq-message')?.value || '').trim();

                // 2. Generate Unique Enquiry Booking Ref ID
                const enquiryRef = '#ENQ-' + Math.floor(100000 + Math.random() * 900000);
                const timestamp = new Date().toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' });

                // 3. Construct Unified Booking Record for Admin Console
                const notesSummary = [
                    tripStyle ? `Style: ${tripStyle}` : '',
                    message ? `Query: ${message}` : ''
                ].filter(Boolean).join(' | ') || 'Home page Explore Now enquiry';

                const enquiryRecord = {
                    booking_id: enquiryRef,
                    timestamp: timestamp,
                    name: name,
                    phone: phone,
                    email: email,
                    package: 'Enquiry: ' + selectedPkg,
                    travel_date: travelDate,
                    travelers: travelers,
                    pickup_city: pickupCity,
                    total_amount: 'Enquiry (Quote Req.)',
                    notes: notesSummary,
                    status: 'Pending',
                    source: 'index.html',
                    _isNewRealtime: true
                };

                // 4. Save to Shared Local Storage Cache & Broadcast in Real-Time to admin.html
                try {
                    const stored = JSON.parse(localStorage.getItem('spirit_local_bookings') || '[]');
                    stored.unshift(enquiryRecord);
                    localStorage.setItem('spirit_local_bookings', JSON.stringify(stored));

                    // Storage event trigger for listening admin tabs/windows
                    localStorage.setItem('spirit_last_booking_event', JSON.stringify({
                        time: Date.now(),
                        ref: enquiryRef,
                        name: name,
                        pkg: enquiryRecord.package,
                        amount: 'Enquiry (Quote Req.)',
                        status: 'Pending',
                        source: 'index.html'
                    }));

                    // Real-Time BroadcastChannel Event
                    if (window.BroadcastChannel) {
                        const bc = new BroadcastChannel('spirit_booking_sync');
                        bc.postMessage({
                            type: 'NEW_BOOKING',
                            source: 'index.html',
                            data: enquiryRecord,
                            timestamp: Date.now()
                        });
                        console.log('⚡ Broadcasted Home Enquiry in real time to admin.html:', enquiryRef);
                    }
                } catch (storageErr) {
                    console.warn('Could not cache or broadcast enquiry:', storageErr);
                }

                // 5. Post to SheetDB REST API endpoint if configured
                const sheetDbUrl = localStorage.getItem('spirit_sheetdb_url');
                if (sheetDbUrl && !sheetDbUrl.includes('YOUR_SHEETDB_API_ID')) {
                    try {
                        fetch(sheetDbUrl, {
                            method: 'POST',
                            headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ data: [enquiryRecord] })
                        }).then(() => {
                            console.log('✅ Enquiry synchronized to SheetDB Google Sheet.');
                        }).catch(err => {
                            console.warn('⚠️ SheetDB sync error:', err);
                        });
                    } catch (e) {
                        console.warn('SheetDB request failed:', e);
                    }
                }

                // 6. Asynchronously submit to Formspree
                try {
                    const formData = new FormData(inquiryForm);
                    formData.append('booking_id', enquiryRef);
                    formData.append('source_page', 'index.html (Home Explore Now)');
                    fetch(inquiryForm.action, {
                        method: 'POST',
                        body: formData,
                        headers: { 'Accept': 'application/json' }
                    }).catch(() => {});
                } catch(e) {}

                // 7. Show In-Modal Confirmation State with Ref ID & Direct WhatsApp Link
                if(submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnText;
                }

                const formBody = document.getElementById('inquiry-form-body');
                const successCard = document.getElementById('inquiry-success-state');
                const refDisplay = document.getElementById('inquiry-success-ref');
                const waDirectBtn = document.getElementById('inquiry-wa-direct-btn');

                if (refDisplay) refDisplay.textContent = `Ref: ${enquiryRef}`;
                if (waDirectBtn) {
                    const cleanPhone = phone.replace(/[^0-9]/g, '');
                    const waText = encodeURIComponent(`Hi Spirit Adventures! I submitted a trip enquiry for ${selectedPkg} (Ref: ${enquiryRef}, ${travelers}). Can you share itinerary details and best price quote?`);
                    waDirectBtn.href = `https://wa.me/919666567551?text=${waText}`;
                }

                if (formBody) formBody.style.display = 'none';
                if (successCard) successCard.style.display = 'block';

                inquiryForm.reset();
            });
        }

        // 8. AI Chatbot Logic
        const chatToggleBtn = document.getElementById('chat-toggle');
        const chatWindow = document.getElementById('chat-window');
        const chatCloseBtn = document.getElementById('chat-close');
        const chatInput = document.getElementById('chat-input');
        const chatSendBtn = document.getElementById('chat-send');
        const chatBody = document.getElementById('chat-body');

        if(chatToggleBtn) {
            chatToggleBtn.addEventListener('click', () => {
                chatWindow.classList.toggle('hidden');
                if(!chatWindow.classList.contains('hidden') && chatInput) {
                    setTimeout(() => chatInput.focus(), 300);
                }
            });
        }

        if(chatCloseBtn) chatCloseBtn.addEventListener('click', () => chatWindow.classList.add('hidden'));

        const handleSendMessage = () => {
            if(!chatInput) return;
            const text = chatInput.value.trim();
            if (!text) return;

            addMessage(text, 'user-msg');
            chatInput.value = '';

            const loadingId = addMessage('...', 'bot-msg', true);

            setTimeout(() => {
                const loadingElement = document.getElementById(loadingId);
                if (loadingElement) loadingElement.remove();
                
                let response = "I'm your Spirit AI Guide! We offer packages for Coorg, Goa, Hampi & Gokarna, and Ooty. Want to explore destination details or book a spot?";
                let lowerText = text.toLowerCase();
                
                if (lowerText.includes('coorg')) {
                    response = 'Our 2D 1N Coorg package is very popular! Includes waterfalls and coffee estate stays. <br><a href="package.html?dest=coorg" style="color:var(--yellow);font-weight:700;text-decoration:underline;">Explore Coorg Details &rarr;</a>';
                } else if (lowerText.includes('goa')) {
                    response = 'Our 3D 2N Goa trip covers sunny beaches, water sports, and Portuguese forts! <br><a href="package.html?dest=goa" style="color:var(--yellow);font-weight:700;text-decoration:underline;">Explore Goa Details &rarr;</a>';
                } else if (lowerText.includes('hampi') || lowerText.includes('gokarna') || lowerText.includes('dandeli')) {
                    response = 'Our 4D 3N Hampi, Gokarna & Dandeli tour is our #1 rated adventure circuit! <br><a href="package.html?dest=hampi" style="color:var(--yellow);font-weight:700;text-decoration:underline;">Explore Hampi Details &rarr;</a>';
                } else if (lowerText.includes('ooty') || lowerText.includes('mysore') || lowerText.includes('kodaikanal')) {
                    response = 'Our 6D 5N Kodaikanal, Ooty & Mysore trip is a regal hill station getaway! <br><a href="package.html?dest=ooty" style="color:var(--yellow);font-weight:700;text-decoration:underline;">Explore Ooty Details &rarr;</a>';
                } else if (lowerText.includes('custom') || lowerText.includes('plan') || lowerText.includes('tailor') || lowerText.includes('personal')) {
                    response = 'Looking for a tailor-made vacation? You can choose custom destinations, vehicles, and stays! <br><a href="customize.html" style="color:var(--yellow);font-weight:700;text-decoration:underline;">Design Custom Tour &rarr;</a>';
                } else if (lowerText.includes('contact') || lowerText.includes('address')) {
                    response = 'We are located at Vasantha Sai Apartments, KPHB, Kukatpally, Hyderabad. Call us at +91 966 656 7551!';
                }

                addMessage(response, 'bot-msg', true);
            }, 1200);
        };

        if(chatSendBtn) chatSendBtn.addEventListener('click', handleSendMessage);
        if(chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') handleSendMessage();
            });
        }

        function addMessage(text, className, isHTML = false) {
            if(!chatBody) return;
            const msgDiv = document.createElement('div');
            msgDiv.classList.add('message', className);
            
            if(isHTML) msgDiv.innerHTML = text;
            else msgDiv.textContent = text;

            const id = 'msg-' + Date.now();
            msgDiv.id = id;
            
            chatBody.appendChild(msgDiv);
            chatBody.scrollTop = chatBody.scrollHeight;
            
            return id;
        }

        // 14. Website Visitor Traffic Tracker (Cross-device Real-Time Sync)
        if (window.SpiritTracker && typeof window.SpiritTracker.recordVisit === 'function') {
            window.SpiritTracker.recordVisit('index.html');
        }

        // 15. Ensure Hero Background Video autoplays reliably across all devices
        const heroBgVideo = document.querySelector('.full-bg-video');
        if (heroBgVideo) {
            heroBgVideo.muted = true;
            const playBg = () => {
                const p = heroBgVideo.play();
                if (p !== undefined) {
                    p.catch(() => {});
                }
            };
            playBg();
            document.addEventListener('touchstart', playBg, { once: true });
            document.addEventListener('click', playBg, { once: true });
        }
    });