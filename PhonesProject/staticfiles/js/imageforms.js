$(document).ready(function(){
    $(".image-form").hide();
    $(".image-form:first").show();

    $(".image-form input[type='file']").change(function(){
        var $thisForm = $(this).closest(".image-form");

        if ($(this).val()){
            $thisForm.next(".image-form").show();
        } else {
            $thisForm.nextAll(".image-form").hide();
        }
    });
});