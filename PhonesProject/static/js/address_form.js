document.addEventListener('DOMContentLoaded', function() {
  var addressFormButton = document.getElementById('addressFormButton');
  var addressSpan = document.getElementById('addressSpan');
  var idAddress = document.getElementById('id_address');
  var idCity = document.getElementById('id_city');
  var idRegion = document.getElementById('id_region');
  var idCountry = document.getElementById('id_country');
  var idPostIndex = document.getElementById('id_post_index');
  var checkoutButton = document.getElementById('checkoutButton');

  if (checkoutButton != undefined){
    const href = checkoutButton.href;
  }


  addressFormButton.addEventListener('click', function() {
    let text = idCity.value + ', ' + idRegion.value + ', ' + idCountry.value
    if (idAddress != undefined) {
        text = idAddress.value + ', ' + text;
    }
    addressSpan.textContent = text;

    if (checkoutButton != undefined) {
        var hrefValue = href + '?country=' + idCountry.value + '&city=' + idCity.value + '&region=' + idRegion.value + "&post_index=" + idPostIndex.value;
        checkoutButton.setAttribute('href', hrefValue);
    }
  });

});