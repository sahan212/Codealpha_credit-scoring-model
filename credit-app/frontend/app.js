// Preset profiles for rapid testing
const presets = {
  good: {
    age: 46,
    education: "Graduate",
    home_ownership: "Own",
    employment_years: 18.0,
    annual_income: 920000,
    total_debt: 80000,
    loan_amount: 150000,
    loan_term_months: 36,
    credit_history_years: 15.0,
    credit_utilization: 0.12,
    num_credit_cards: 2,
    existing_loans: 1,
    late_payments_12m: 0,
    missed_payments_total: 0
  },
  risky: {
    age: 26,
    education: "High School",
    home_ownership: "Rent",
    employment_years: 1.0,
    annual_income: 240000,
    total_debt: 340000,
    loan_amount: 220000,
    loan_term_months: 48,
    credit_history_years: 2.0,
    credit_utilization: 0.72,
    num_credit_cards: 6,
    existing_loans: 3,
    late_payments_12m: 3,
    missed_payments_total: 5
  }
};

function fillProfile(type) {
  const p = presets[type];
  if (!p) return;
  for (const [key, val] of Object.entries(p)) {
    const el = document.getElementById(key);
    if (el) el.value = val;
  }
}

document.getElementById('assessmentForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const payload = {
    age: parseInt(document.getElementById('age').value),
    education: document.getElementById('education').value,
    home_ownership: document.getElementById('home_ownership').value,
    employment_years: parseFloat(document.getElementById('employment_years').value),
    annual_income: parseFloat(document.getElementById('annual_income').value),
    total_debt: parseFloat(document.getElementById('total_debt').value),
    num_credit_cards: parseInt(document.getElementById('num_credit_cards').value),
    existing_loans: parseInt(document.getElementById('existing_loans').value),
    credit_utilization: parseFloat(document.getElementById('credit_utilization').value),
    credit_history_years: parseFloat(document.getElementById('credit_history_years').value),
    late_payments_12m: parseInt(document.getElementById('late_payments_12m').value),
    missed_payments_total: parseInt(document.getElementById('missed_payments_total').value),
    loan_amount: parseFloat(document.getElementById('loan_amount').value),
    loan_term_months: parseInt(document.getElementById('loan_term_months').value),
  };

  const btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-2"></i> Analyzing...`;

  try {
    const res = await fetch('/api/assess', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error("Evaluation request failed.");
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    alert("Error: " + err.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<i class="fa-solid fa-calculator mr-2"></i> Evaluate Creditworthiness`;
  }
});

function renderResults(data) {
  const verdictBadge = document.getElementById('verdictBadge');
  const riskLevelText = document.getElementById('riskLevelText');
  const riskBar = document.getElementById('riskBar');
  const riskScoreLabel = document.getElementById('riskScoreLabel');
  const dtiValue = document.getElementById('dtiValue');
  const ltiValue = document.getElementById('ltiValue');
  const factorsList = document.getElementById('factorsList');

  // Verdict Styling
  if (data.is_creditworthy) {
    verdictBadge.innerHTML = `<span class="text-emerald-400"><i class="fa-solid fa-circle-check mr-2"></i>APPROVED (Creditworthy)</span>`;
    riskLevelText.innerHTML = `Candidate classified as <strong class="text-emerald-400">${data.risk_level}</strong>`;
    riskBar.className = "h-3 rounded-full bg-emerald-500 transition-all duration-700";
  } else {
    verdictBadge.innerHTML = `<span class="text-rose-400"><i class="fa-solid fa-circle-xmark mr-2"></i>REJECTED (High Risk)</span>`;
    riskLevelText.innerHTML = `Candidate classified as <strong class="text-rose-400">${data.risk_level}</strong>`;
    riskBar.className = "h-3 rounded-full bg-rose-500 transition-all duration-700";
  }

  // Bar progress
  riskBar.style.width = `${Math.min(data.risk_score_pct, 100)}%`;
  riskScoreLabel.innerText = `${data.risk_score_pct}%`;

  // Ratios
  dtiValue.innerText = data.debt_to_income.toFixed(2);
  ltiValue.innerText = data.loan_to_income.toFixed(2);

  // Key factors
  factorsList.innerHTML = data.key_factors.map(f => `<li class="flex items-center space-x-2">
    <i class="fa-solid fa-chevron-right text-indigo-400 text-[10px]"></i>
    <span>${f}</span>
  </li>`).join('');
}
