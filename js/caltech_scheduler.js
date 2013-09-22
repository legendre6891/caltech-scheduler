function makeStruct(names) {
  var names = names.split(' ');
  var count = names.length;
  function constructor() {
    for (var i = 0; i < count; i++) {
      this[names[i]] = arguments[i];
    }
  }
  return constructor;
}

var CourseOptionEnum = Object.freeze({
	ACM: {},
	CS: {}
});
var CourseGradeEnum = Object.freeze({
	EITHER: {},
	GRADES: {}
})

var CaltechCourse = makeStruct("ID course_option course_number course_name units section prof_first_name prof_last_name subtitle annotations fixed_time times days locations grade");
/*
ID,
course_option,
course_number,
course_name,
units, 
section,
prof_first_name,
prof_last_name,
subtitle,
annotations,
fixed_time,
times,
days, 
locations, 
grades
*/

master_course_list = [
new CaltechCourse(0,
	CourseOptionEnum.ACM,
	"95",
	"Introductory Methods of Applied Mathematics",
	12,
	1,
	"Pierce",
	"Niles",
	"",
	[],
	true,
	[[11, 12], [11,12]],
	[[1,3,5],[2]],
	["119 KRK", "11 DWN"],
	CourseGradeEnum.EITHER
	),

new CaltechCourse(1,
	CourseOptionEnum.CS,
	"156a",
	"Learning Systems",
	9,
	1,
	"Abu-Mostafa",
	"Y",
	"",
	["Organization meeting, M 5-6PM at 070 MRE"],
	false,
	[],
	[],
	[],
	CourseGradeEnum.GRADES
	)
]


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



// need to the functions
// master_courses = list of classes
// addID(id) -- function;
// active_courses = list of id's
// generate_event_from_id(id) -- generate a FC event corresponding to the course id.