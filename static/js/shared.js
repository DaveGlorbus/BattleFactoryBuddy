
function setFormFromParams(urlParams) {
  const formElements = document.querySelectorAll('.form-select, .form-check-input, .form-control');

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

async function createAndCopyShareLink(initialParams = null, includePathName = false) {
    let params = new URLSearchParams();

    if (initialParams){
        params = initialParams;
    }

    const formElements = document.querySelectorAll('.form-select, .form-check-input, .form-control');


    formElements.forEach(element => {
        if (element.type === 'checkbox') {
            params.append(element.name, element.checked ? 'on' : 'off');
        }
        else {
            params.append(element.name, element.value);
        }
    });

    params.append('Calc', 1);

    let pathname = "/";
    if (includePathName){
      pathname = `${window.location.pathname}`
    }

    const url = `${window.location.protocol}//${window.location.host}${pathname}?${params.toString()}`;
    try {
        await navigator.clipboard.writeText(url);
    } catch (error) {
        console.error(error.message);
    }
}