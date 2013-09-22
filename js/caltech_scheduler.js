$(document).ready(
	function()
	{
		$( ".caltech-course" ).hide();
		$("#course-filter-box").keyup(
			function()
			{
				var search_term = $("#course-filter-box").val();
				// console.log(search_term);
				$( ".caltech-course" ).hide();
				$(".caltech-course").filter(function(index){
					// console.log(($(this).attr('data-course-name')).score(search_term));
					return ($(this).attr('data-course-name')).score(search_term) > 0;
				}).show();
				// $( ".caltech-course").dfilter('course-name', search_term + "*.").show();
			});
	});