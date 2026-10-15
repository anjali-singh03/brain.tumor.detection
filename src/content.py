# content.py
# Contains all medical data and patient cases

DATA = {
    "glioma": {
        "title": "Glioma", "emoji": "🔴",
        "overview": (
            "A tumor that starts in glial cells, the supporting cells of the brain and spinal cord. "
            "Gliomas range from slow-growing (low grade) to aggressive (high grade) and are among "
            "the most common primary brain tumors."
        ),
        "causes": [
            "Exact cause is usually unknown",
            "Past exposure to ionizing radiation (for example radiotherapy to the head)",
            "Rare inherited syndromes: neurofibromatosis, Li-Fraumeni syndrome, tuberous sclerosis",
            "Risk rises with age; no proven link to mobile phones",
        ],
        "symptoms": [
            "Headaches that keep getting worse, often worse in the morning",
            "Seizures", "Nausea or vomiting",
            "Memory, speech or personality changes",
            "Weakness, numbness or balance problems on one side",
        ],
        "treatment": [
            "Surgery to remove as much of the tumor as safely possible",
            "Radiotherapy to destroy remaining tumor cells",
            "Chemotherapy (for example temozolomide in some types)",
            "Medicines for symptom control: anti-seizure drugs, steroids for swelling",
            "Regular follow-up MRI scans; treatment depends on grade, location and patient health",
        ],
        "precautions": [
            "Take anti-seizure medicines exactly as prescribed",
            "Do not miss follow-up MRI scans and appointments",
            "Avoid unnecessary radiation exposure (only medically needed CT/X-ray)",
            "Avoid driving if you have had seizures, until your doctor allows it",
            "Eat balanced meals, sleep well, and ask about safe physical activity",
            "Seek emotional support: counselling and support groups help",
        ],
        "specialists": "Neurologist, neurosurgeon, neuro-oncologist, radiation oncologist",
        "see_doctor": [
            "New or worsening headaches that do not settle",
            "Any seizure, even a single one",
            "Sudden vision, speech or balance problems",
        ],
        "questions": [
            "What grade and type is this tumor?",
            "Is surgery possible, and what are the risks?",
            "What treatment options do I have and what are their side effects?",
            "How often will I need follow-up scans?",
        ],
    },
    "meningioma": {
        "title": "Meningioma", "emoji": "🟠",
        "overview": (
            "A tumor that grows from the meninges, the protective layers covering the brain and "
            "spinal cord. Most meningiomas are benign (non-cancerous) and grow slowly, so some "
            "are only monitored."
        ),
        "causes": [
            "Exact cause is mostly unknown",
            "Previous radiation to the head",
            "Being female and older age (hormonal influence is suspected)",
            "Inherited condition neurofibromatosis type 2 (NF2)",
        ],
        "symptoms": [
            "Slowly worsening headaches",
            "Blurred or double vision",
            "Hearing loss or ringing in the ears",
            "Seizures", "Memory problems or weakness in arms or legs",
        ],
        "treatment": [
            "Watchful waiting with regular MRI for small, symptom-free tumors",
            "Surgery to remove the tumor (often curative for accessible ones)",
            "Radiotherapy or stereotactic radiosurgery when surgery is risky or tumor remains",
            "Medicines for seizures or swelling if needed",
        ],
        "precautions": [
            "Keep all scheduled monitoring scans",
            "Report new symptoms early, especially vision or hearing changes",
            "Avoid unnecessary head radiation",
            "Discuss hormone therapy with your doctor if you use it",
            "Maintain a healthy weight, diet and sleep routine",
        ],
        "specialists": (
            "Neurologist, neurosurgeon, radiation oncologist, "
            "ophthalmologist (if vision is affected)"
        ),
        "see_doctor": [
            "Gradual vision loss or double vision",
            "Persistent headaches or hearing changes",
            "Any seizure",
        ],
        "questions": [
            "Can this be safely monitored instead of treated now?",
            "How fast is it growing?",
            "What are the surgery and radiation options?",
            "What symptoms should make me call you urgently?",
        ],
    },
    "pituitary": {
        "title": "Pituitary Tumor", "emoji": "🟡",
        "overview": (
            "A growth in the pituitary gland at the base of the brain, which controls hormones. "
            "Most are benign adenomas. They can press on nearby nerves or produce too much "
            "(or too little) hormone."
        ),
        "causes": [
            "Usually no clear cause",
            "A few are linked to inherited conditions such as MEN1",
            "Hormone-related gene changes inside the gland's cells",
        ],
        "symptoms": [
            "Headaches",
            "Vision problems, especially loss of side vision",
            "Hormone effects: fatigue, weight change, irregular periods, milk discharge, low sex drive",
            "Growth changes (in some hormone-producing types)",
        ],
        "treatment": [
            "Medicines that shrink some tumors or block hormone excess (for example for prolactinomas)",
            "Transsphenoidal surgery (through the nose) to remove the tumor",
            "Radiotherapy if tumor remains or returns",
            "Hormone replacement if the gland is under-active after treatment",
        ],
        "precautions": [
            "Get regular hormone blood tests as advised",
            "Take hormone medicines on time and never stop suddenly",
            "Get eyesight checked regularly",
            "Report new vision changes or severe sudden headache immediately",
            "Keep follow-up MRI appointments",
        ],
        "specialists": "Endocrinologist, neurosurgeon, ophthalmologist",
        "see_doctor": [
            "Vision loss or narrowing of your side vision",
            "Sudden severe headache with vision change or vomiting",
            "Unexplained hormone symptoms (periods, fatigue, weight)",
        ],
        "questions": [
            "Is the tumor producing hormones?",
            "Can medicine alone treat it?",
            "Will I need lifelong hormone tablets?",
            "How will my vision be monitored?",
        ],
    },
    "notumor": {
        "title": "No Tumor Detected", "emoji": "🟢",
        "overview": (
            "The model did not find a tumor pattern in this scan. This is only an automated "
            "estimate, and it cannot rule out other brain conditions or small abnormalities."
        ),
        "causes": ["Not applicable: no tumor pattern was detected"],
        "symptoms": [
            "A normal-looking result does not explain existing symptoms. "
            "Persisting symptoms still need medical review."
        ],
        "treatment": [
            "No tumor treatment is suggested by this result",
            "Symptoms should be assessed by a doctor",
        ],
        "precautions": [
            "Keep a healthy routine: sleep, hydration, exercise, stress management",
            "Protect your head during sports and driving",
            "Do not ignore ongoing headaches, dizziness or vision changes",
        ],
        "specialists": "General physician or neurologist if symptoms continue",
        "see_doctor": [
            "Headaches that keep returning or worsen",
            "Seizures, fainting or sudden weakness",
            "Vision, speech or balance problems",
        ],
        "questions": [
            "Could my symptoms have another cause?",
            "Do I need a radiologist to review this scan?",
        ],
    },
}

CASES = {
    "glioma": {
        "patient": "Illustrative case: a 42-year-old office worker",
        "happened": (
            "Had weeks of morning headaches, then a first seizure at work. An MRI showed a mass "
            "in the temporal lobe, and a biopsy confirmed a low-grade glioma."
        ),
        "doctors": (
            "The team explained that surgery would remove as much of the tumor as safely possible, "
            "followed by radiotherapy if needed. They started anti-seizure medicine, advised no "
            "driving for a period, and planned MRI scans every few months."
        ),
        "outcome": (
            "Returned to work after recovery and continues regular scans. "
            "Outcomes depend on tumor grade and location."
        ),
        "links": [
            ("PubMed: glioma case reports", "https://pubmed.ncbi.nlm.nih.gov/?term=glioma+case+report"),
            ("NHS: Brain tumours", "https://www.nhs.uk/conditions/brain-tumours/"),
            ("American Brain Tumor Association", "https://www.abta.org"),
        ],
    },
    "meningioma": {
        "patient": "Illustrative case: a 58-year-old woman",
        "happened": (
            "Noticed slowly blurring vision and mild headaches. An MRI found a small meningioma "
            "pressing near the optic nerve."
        ),
        "doctors": (
            "Doctors explained that most meningiomas are benign and slow growing. They started "
            "with regular MRI monitoring, and recommended surgery or radiosurgery once the tumor "
            "grew and vision was affected."
        ),
        "outcome": "Treatment stopped further vision loss. She continues yearly follow-up scans.",
        "links": [
            ("PubMed: meningioma case reports", "https://pubmed.ncbi.nlm.nih.gov/?term=meningioma+case+report"),
            ("NHS: Brain tumours", "https://www.nhs.uk/conditions/brain-tumours/"),
            ("American Brain Tumor Association", "https://www.abta.org"),
        ],
    },
    "pituitary": {
        "patient": "Illustrative case: a 30-year-old woman",
        "happened": (
            "Had irregular periods, unexpected milk discharge and headaches. Blood tests showed "
            "very high prolactin, and an MRI found a small pituitary adenoma."
        ),
        "doctors": (
            "The endocrinologist explained that this type (a prolactinoma) is often treated with "
            "tablets rather than surgery, with blood tests and an eye check to monitor progress."
        ),
        "outcome": (
            "Hormone levels returned to normal on medication and the tumor shrank. "
            "Surgery is kept as a backup option."
        ),
        "links": [
            (
                "PubMed: pituitary adenoma case reports",
                "https://pubmed.ncbi.nlm.nih.gov/?term=pituitary+adenoma+case+report",
            ),
            ("NHS: Brain tumours", "https://www.nhs.uk/conditions/brain-tumours/"),
            ("American Brain Tumor Association", "https://www.abta.org"),
        ],
    },
    "notumor": {
        "patient": "Illustrative case: a 27-year-old student",
        "happened": (
            "Had recurring headaches and worried about a tumor. An MRI showed no tumor or other "
            "serious abnormality."
        ),
        "doctors": (
            "The doctor explained that stress, poor sleep, long screen time and migraine are "
            "common causes. They advised regular sleep, hydration, a headache diary and a review "
            "if symptoms change."
        ),
        "outcome": (
            "Headaches improved with lifestyle changes. The doctor asked her to return "
            "if new symptoms appeared."
        ),
        "links": [
            ("NHS: Headaches", "https://www.nhs.uk/conditions/headaches/"),
        ],
    },
}
