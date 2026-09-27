// JanSetu AI (जन सेतु) - Digital Public Good for Citizen Infrastructure Governance
let globalDataset = null;
let leafletMap = null;
let mapMarkers = [];
let selectedDistrict = null;
let isRecording = false;
let speechRecognizer = null;

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    initTabs();
    await loadDataset();
    initLeafletMap();
    initSpeechRecognition();
    setupDropzone();
    populateSampleChips();
    populateDistrictSelect();
});

// 1. Navigation Tabs
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanels.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const target = btn.getAttribute('data-tab');
            const panel = document.getElementById(target);
            if (panel) {
                panel.classList.add('active');
                if (target === 'tab-heatmap' && leafletMap) {
                    setTimeout(() => leafletMap.invalidateSize(), 200);
                }
            }
        });
    });
}

// 2. Load Dataset
async function loadDataset() {
    try {
        const res = await fetch('dataset.json');
        globalDataset = await res.json();
    } catch (err) {
        console.warn('Dataset fallback active:', err);
        globalDataset = {
            districts: [
                {
                    id: "DIST-TEL-01",
                    name: "Warangal",
                    state: "Telangana",
                    lat: 17.9689,
                    lng: 79.5941,
                    population: "1,050,000",
                    sdg_index: 68,
                    aspirational_district: false,
                    active_complaints: 47,
                    priority_score: 8.7,
                    top_issue: "Drinking Water Pipeline Burst & Road Cavity",
                    ministry: "Ministry of Jal Shakti / MoRTH",
                    estimated_budget: "₹42.5 Lakhs",
                    impacted_citizens: "18,400"
                }
            ],
            sample_voice_prompts: []
        };
    }
}

// 3. Interactive Leaflet Map for India
function initLeafletMap() {
    const mapElement = document.getElementById('indiaMap');
    if (!mapElement || typeof L === 'undefined') return;

    leafletMap = L.map('indiaMap', {
        center: [22.3511, 78.6677],
        zoom: 5,
        minZoom: 4,
        maxZoom: 12
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://carto.com/">CARTO</a> &bull; JanSetu National GIS'
    }).addTo(leafletMap);

    renderHotspots();
}

function renderHotspots() {
    if (!globalDataset || !globalDataset.districts || !leafletMap) return;

    const listContainer = document.getElementById('hotspotListContainer');
    if (listContainer) listContainer.innerHTML = '';

    mapMarkers.forEach(m => leafletMap.removeLayer(m));
    mapMarkers = [];

    globalDataset.districts.forEach(dist => {
        // Map Marker
        const isUrgent = dist.priority_score >= 8.5;
        const markerColor = isUrgent ? '#EF4444' : '#0284C7';

        const customIcon = L.divIcon({
            className: 'custom-map-pin',
            html: `<div style="background:${markerColor}; width:16px; height:16px; border-radius:50%; border:3px solid #FFFFFF; box-shadow:0 0 10px ${markerColor};"></div>`,
            iconSize: [16, 16]
        });

        const marker = L.marker([dist.lat, dist.lng], { icon: customIcon }).addTo(leafletMap);
        marker.bindPopup(`
            <div style="font-family:sans-serif; min-width:180px;">
                <strong style="color:#0A192F; font-size:0.95rem;">${dist.name}, ${dist.state}</strong><br/>
                <span style="font-size:0.75rem; color:#EF4444; font-weight:700;">● Priority Score: ${dist.priority_score}/10</span><br/>
                <p style="font-size:0.8rem; margin:6px 0; color:#334155;">${dist.top_issue}</p>
                <div style="font-size:0.72rem; color:#64748B;">Active Grievances: <strong>${dist.active_complaints}</strong></div>
                <button onclick="selectDistrictFromMap('${dist.id}')" style="margin-top:8px; width:100%; background:#0284C7; color:#fff; border:none; padding:4px 8px; border-radius:4px; font-size:0.75rem; font-weight:700; cursor:pointer;">
                    Inspect &amp; Generate DPR &rarr;
                </button>
            </div>
        `);
        mapMarkers.push(marker);

        // Sidebar List Card
        if (listContainer) {
            const card = document.createElement('div');
            card.className = `hotspot-item ${isUrgent ? 'urgent' : ''}`;
            card.id = `hotspot-card-${dist.id}`;
            card.innerHTML = `
                <div class="hotspot-item-header">
                    <span class="hotspot-district">${dist.name}, ${dist.state}</span>
                    <span class="priority-chip" style="${isUrgent ? '' : 'background:#E0F2FE; color:#0369A1;'}">Score: ${dist.priority_score}</span>
                </div>
                <div class="hotspot-issue">${dist.top_issue}</div>
                <div class="hotspot-meta-row">
                    <span>${dist.active_complaints} Citizen Grievances</span>
                    <span>Budget: ${dist.estimated_budget}</span>
                </div>
            `;
            card.addEventListener('click', () => {
                selectDistrict(dist);
            });
            listContainer.appendChild(card);
        }
    });

    if (globalDataset.districts.length > 0) {
        selectDistrict(globalDataset.districts[0]);
    }
}

function selectDistrictFromMap(districtId) {
    const dist = globalDataset.districts.find(d => d.id === districtId);
    if (dist) {
        selectDistrict(dist);
        // Switch to DPR tab for seamless policymaker flow
        document.querySelector('[data-tab="tab-copilot"]').click();
    }
}

function selectDistrict(dist) {
    selectedDistrict = dist;

    // Highlight map marker & pan
    if (leafletMap) {
        leafletMap.flyTo([dist.lat, dist.lng], 8, { duration: 1 });
    }

    // Highlight sidebar
    document.querySelectorAll('.hotspot-item').forEach(el => el.classList.remove('selected'));
    const targetCard = document.getElementById(`hotspot-card-${dist.id}`);
    if (targetCard) targetCard.classList.add('selected');

    // Populate DPR Copilot inputs
    updateCopilotView(dist);
}

// 4. Speech Recognition (Web Speech API)
function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        console.warn('Web Speech API not supported on this browser.');
        return;
    }

    speechRecognizer = new SpeechRecognition();
    speechRecognizer.continuous = false;
    speechRecognizer.interimResults = false;

    speechRecognizer.onstart = () => {
        isRecording = true;
        updateMicUI(true);
    };

    speechRecognizer.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('grievanceText').value = transcript;
        processCitizenGrievance(transcript, 'Voice Input (Native Indian Dialect)');
    };

    speechRecognizer.onerror = (event) => {
        console.error('Speech error:', event.error);
        updateMicUI(false);
    };

    speechRecognizer.onend = () => {
        updateMicUI(false);
    };
}

function toggleVoiceRecord() {
    if (!speechRecognizer) {
        alert('Microphone speech recognition is not supported on this browser. Try testing with the quick sample buttons below!');
        return;
    }

    if (isRecording) {
        speechRecognizer.stop();
        updateMicUI(false);
    } else {
        const langCode = document.getElementById('voiceLangSelect').value || 'te-IN';
        speechRecognizer.lang = langCode;
        speechRecognizer.start();
    }
}

function updateMicUI(recording) {
    isRecording = recording;
    const btn = document.getElementById('micBtn');
    const box = document.getElementById('voiceBox');
    const statusText = document.getElementById('voiceStatusText');

    if (recording) {
        btn.classList.add('active');
        box.classList.add('recording');
        statusText.innerText = 'Listening... Speak now in your regional language';
        statusText.style.color = '#EF4444';
    } else {
        btn.classList.remove('active');
        box.classList.remove('recording');
        statusText.innerText = 'Tap to Speak in Any Indian Language';
        statusText.style.color = '#1E293B';
    }
}

// 5. Sample Speech Chips
function populateSampleChips() {
    const container = document.getElementById('sampleChipsContainer');
    if (!container || !globalDataset || !globalDataset.sample_voice_prompts) return;

    container.innerHTML = '';
    globalDataset.sample_voice_prompts.forEach(item => {
        const chip = document.createElement('button');
        chip.type = 'button';
        chip.className = 'sample-chip';
        chip.innerText = item.lang;
        chip.addEventListener('click', () => {
            document.getElementById('grievanceText').value = item.sample;
            if (item.lang.includes('Telugu')) document.getElementById('voiceLangSelect').value = 'te-IN';
            if (item.lang.includes('Hindi')) document.getElementById('voiceLangSelect').value = 'hi-IN';
            if (item.lang.includes('Marathi')) document.getElementById('voiceLangSelect').value = 'mr-IN';
            if (item.lang.includes('Tamil')) document.getElementById('voiceLangSelect').value = 'ta-IN';

            // Auto-trigger Gemini analysis
            processCitizenGrievance(item.sample, item.lang, item);
        });
        container.appendChild(chip);
    });
}

// 6. Image Dropzone
function setupDropzone() {
    const dropzone = document.getElementById('photoDropzone');
    const fileInput = document.getElementById('filePhoto');
    const preview = document.getElementById('previewImg');

    if (!dropzone || !fileInput) return;

    dropzone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (evt) => {
                preview.src = evt.target.result;
                preview.style.display = 'block';
                document.getElementById('dropzoneLabel').innerText = `Photo Attached: ${file.name}`;
            };
            reader.readAsDataURL(file);
        }
    });
}

// 7. Process Citizen Grievance via Google Gemini Engine
async function processCitizenGrievance(text, langContext, presetData = null) {
    const auditCard = document.getElementById('aiAuditCard');
    auditCard.style.opacity = '0.5';

    // Simulated Gemini 1.5 Multimodal inference latency
    await new Promise(r => setTimeout(r, 650));
    auditCard.style.opacity = '1';

    let translation = presetData ? presetData.english_translation : `Translated: "${text}"`;
    let category = presetData ? presetData.category : "Urban Drainage & Road Structural Integrity";
    let severity = presetData ? presetData.severity : 4;
    let confidence = presetData ? "96.4%" : "92.8%";
    let damageType = presetData ? presetData.damage_type : "Structural Subsidance / Public Utility Failure";

    // Update UI
    document.getElementById('aiCategoryVal').innerText = category;
    document.getElementById('aiSeverityVal').innerText = `${severity} / 5 (CRITICAL)`;
    document.getElementById('aiDamageVal').innerText = damageType;
    document.getElementById('aiConfidenceVal').innerText = confidence;
    document.getElementById('aiTranslationText').innerText = translation;

    // Toast feedback
    showToast('Gemini Multimodal Analysis Complete');
}

// 8. Populate District Dropdown
function populateDistrictSelect() {
    const select = document.getElementById('dprDistrictSelect');
    if (!select || !globalDataset || !globalDataset.districts) return;

    select.innerHTML = '';
    globalDataset.districts.forEach(d => {
        const opt = document.createElement('option');
        opt.value = d.id;
        opt.innerText = `${d.name} (${d.state}) - Score ${d.priority_score}`;
        select.appendChild(opt);
    });

    select.addEventListener('change', (e) => {
        const dist = globalDataset.districts.find(d => d.id === e.target.value);
        if (dist) selectDistrict(dist);
    });
}

// 9. Update DPR / Policy Copilot View
function updateCopilotView(dist) {
    document.getElementById('dprTitle').innerText = `Detailed Project Report (DPR): ${dist.name} Municipal Infrastructure Rehabilitation`;
    document.getElementById('dprDistrictName').innerText = `${dist.name}, ${dist.state} (SDG Index: ${dist.sdg_index})`;
    document.getElementById('dprEstimatedCost').innerText = dist.estimated_budget;
    document.getElementById('dprBeneficiaries').innerText = `${dist.impacted_citizens} Citizens`;
    document.getElementById('dprMinistry').innerText = dist.ministry;
    document.getElementById('dprRationale').innerText = `Correlating ${dist.active_complaints} geo-tagged citizen grievances over 30 days indicates severe structural stress on the ${dist.top_issue}. Left unaddressed, failure impacts essential public health and economic arterial transit. Project aligns with PM Gati Shakti National Master Plan.`;
}

// 10. Generate Official DPR Document
function generateDPRDocument() {
    if (!selectedDistrict) {
        alert('Please select a district hotspot first.');
        return;
    }

    const btn = document.getElementById('btnGenerateDPR');
    btn.innerHTML = '<span>⚡ Synthesizing with Gemini 1.5 Pro...</span>';
    btn.disabled = true;

    setTimeout(() => {
        btn.innerHTML = '<span>✓ Official DPR Generated &amp; Signed</span>';
        btn.disabled = false;
        showToast('Official Infrastructure Sanction Note Generated!');
    }, 900);
}

// 11. Cross-Border / BRICS Toggle
let isBricsMode = false;
function toggleBricsMode() {
    isBricsMode = !isBricsMode;
    const btn = document.getElementById('bricsToggleBtn');
    const badge = document.getElementById('nationalBadge');

    if (isBricsMode) {
        btn.innerText = 'Switch to India National Grid';
        btn.style.background = '#0284C7';
        btn.style.color = '#FFFFFF';
        badge.innerText = '🌐 BRICS & Global South Public Good Mode';
        badge.style.background = '#FEF3C7';
        badge.style.color = '#B45309';
        showToast('Switched to BRICS Multilateral Infrastructure Accord (Brazil, South Africa, India)');
    } else {
        btn.innerText = '🌐 Switch to BRICS / Global South Mode';
        btn.style.background = '#F1F5F9';
        btn.style.color = '#334155';
        badge.innerText = '🇮🇳 Digital Public Infrastructure (DPI) • India Stack';
        badge.style.background = '#ECFDF5';
        badge.style.color = '#065F46';
        showToast('Switched to India National Grid');
    }
}

// 12. Submit Grievance Form
function handleGrievanceSubmit(e) {
    e.preventDefault();
    const text = document.getElementById('grievanceText').value.trim();
    if (!text) {
        alert('Please speak or type a grievance first.');
        return;
    }

    const submitBtn = document.getElementById('btnSubmitGrievance');
    submitBtn.innerHTML = '<span>Publishing to National Grid...</span>';
    submitBtn.disabled = true;

    setTimeout(() => {
        submitBtn.innerHTML = '<span>✓ Grievance Registered (ID: JS-2026-8941)</span>';
        submitBtn.style.background = '#10B981';
        showToast('Grievance published to National Infrastructure Heatmap!');

        setTimeout(() => {
            submitBtn.innerHTML = '<span>Submit Grievance to National Infrastructure Grid &rarr;</span>';
            submitBtn.style.background = 'linear-gradient(135deg, #0A192F 0%, #0284C7 100%)';
            submitBtn.disabled = false;
            // Switch to heatmap view to show the result
            document.querySelector('[data-tab="tab-heatmap"]').click();
        }, 1200);
    }, 800);
}

// Toast Utility
function showToast(message) {
    let toast = document.getElementById('janToast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'janToast';
        toast.style.cssText = `
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #0A192F;
            color: #FFFFFF;
            padding: 12px 20px;
            border-radius: 8px;
            border-left: 4px solid #10B981;
            font-size: 0.85rem;
            font-weight: 700;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            z-index: 9999;
            transition: all 0.3s ease;
        `;
        document.body.appendChild(toast);
    }
    toast.innerText = message;
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
    }, 2800);
}
