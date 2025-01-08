
function setFormFromParams(urlParams) {
  const formElements = document.querySelectorAll('.form-select, .form-check-input');

  formElements.forEach(element => {
    const paramValue = urlParams.get(element.name);
    if (paramValue) {
      if (element.type === 'checkbox') {
        element.checked = paramValue === 'on';
      }
      else {
        element.value = paramValue;
      }
    }
  });
}