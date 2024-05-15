function loadSubcategories(parentCategoryId) {
  console.log('retrieving categories');
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/categories/' + parentCategoryId, true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        var subcategories = xhr.responseText;
        var categoryDropdownItems = document.getElementById('category_dropdown_items');
        categoryDropdownItems.innerHTML = subcategories;


        const buttons = document.querySelectorAll('button.hover-click-toggle');
        console.log(buttons);
        buttons.forEach(button => {
          button.addEventListener('mouseover', () => {
            const divId = button.id;
            const div = document.querySelector(`div[aria-labelledby="${divId}"]`);

            if (div) {
              div.classList.toggle('show');
            }
          });
        });
      } else {
        console.log(xhr.status);
      }
    }
  };
  xhr.send();
}
loadSubcategories('');