const checkboxBilling = document.getElementById('id_billing_use_billing');
const billingDiv = document.getElementById('billingDiv');
const inputs = billingDiv.querySelectorAll('input');


function getSourceInput(input) {
    const fieldName = input.id.replace('id_billing_', '');
    const sourceInputId = 'id_' + fieldName;
    return document.getElementById(sourceInputId);
}


inputs.forEach(input => {
    const sourceInput = getSourceInput(input);
    if (sourceInput != undefined) {
        sourceInput.addEventListener('change', function() {
            if (checkboxBilling.checked) {
                input.value = sourceInput.value;
            }
        });
    }
});


function f() {
  if (checkboxBilling.checked) {
    billingDiv.classList.add('d-none');
  } else {
    billingDiv.classList.remove('d-none');
  }

  inputs.forEach(input => {
    const sourceInput = getSourceInput(input);
    if (sourceInput != undefined) {
      if (checkboxBilling.checked) {
        input.value = sourceInput.value;
      }
    }
  });
}


checkboxBilling.addEventListener('change', f);
f();