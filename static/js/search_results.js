// javascript...
"use strict";


$("brand_ing_submit_btn").on("click", function (evt) {
    evt.preventDefualt();
    $("#search_results_table").load("/search_results")
});

$("pr_submit_btn").on("click", function (evt) {
    evt.preventDefualt();
    $("#search_results_table").load("/search_results")
})