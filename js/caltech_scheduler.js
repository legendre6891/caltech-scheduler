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
	ACM: {str: "ACM"},
	CS: {str: "CS"}
});
var CourseGradeEnum = Object.freeze({
	EITHER: {str: "EITHER"},
	GRADES: {str: "GRADES"},
	PF: {str: "PASS/FAIL"}
});




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

var MasterCourseList = [
new CaltechCourse(0,
	CourseOptionEnum.ACM,
	"95",
	"Introductory Methods of Applied Mathematics",
	12,
	1,
	"Pierce",
	"N",
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
	[[8,9]],
	[[1]],
	[],
	CourseGradeEnum.GRADES
	)
];


var activeCoursesID = [];

var activeCoursesAtomicEvents = [];

var activeCourseEventObject = {
	events: activeCoursesAtomicEvents,
	allDayDefault: false
};




function getCourseFullName (course_id) {
	var cc = MasterCourseList[course_id];
	return cc.course_name;
}

function getCourseFixedTime (course_id) {
	var cc = MasterCourseList[course_id];
	return cc.fixed_time;
}

function getCourseMultiplicity (course_id) {
	var cc = MasterCourseList[course_id];
	return cc.times.length;
}

function getCourseSectionNumber (course_id) {
	var cc = MasterCourseList[course_id];
	return cc.section;
}

function getCourseDays (course_id) {
	var cc = MasterCourseList[course_id];
	return cc.days;
}

function getCourseTimes (course_id) {
	var cc = MasterCourseList[course_id];
	return cc.times;
}

function getCourseDaysAt (course_id, i) {
	return getCourseDays(course_id)[i];
}

function getCourseTimesAt (course_id, i) {
	return getCourseTimes(course_id)[i];
}

function generateCourseShortName (course_id) {
	var cc = MasterCourseList[course_id];
	return cc.course_option.str + " " + cc.course_number;
}


function generateCourseFilterName (course_id) {
	var cc = MasterCourseList[course_id];
	return cc.course_option.str.toLowerCase() + ' ' + cc.course_number;
}

function generateCourseFCTitle (course_id) {
	return generateCourseShortName(course_id) + " - Section " + String(getCourseSectionNumber(course_id));
}

function generateAtomicEvent (course_id, day_of_week, times) {
	// create the begin and end times;
	var momentBegin = moment();
	var momentEnd = moment();

	momentBegin.day(day_of_week);
	momentEnd.day(day_of_week);

	momentBegin.hour(times[0]);
	momentEnd.hour(times[1]);

	momentBegin.minute(0);
	momentEnd.minute(0);

	momentBegin.second(0);
	momentEnd.second(0);

	var e = {
		title : generateCourseFCTitle(course_id),
		start : momentBegin.format(),
		end : momentEnd.format(),
		allDay : false
	};
	return e;


	activeCoursesAtomicEvents.push(e);
	activeCourseEventObject.events = activeCoursesAtomicEvents;

	$("#calendar").fullCalendar('refetchEvents');

	return e;
}


function generateIsotimeEvents (course_id, days, times) {
	var isotimeEvents = [];
	for (var i = days.length - 1; i >= 0; i--) {
		isotimeEvents.push(generateAtomicEvent(course_id, days[i], times));
	};
	return isotimeEvents;
}


function getFilterButtonHTML (course_id) {
	// Converts a CaltechCourse into
	// a "filter button", which is used
	// in conjunction with the filter bar.


	var filtername = generateCourseFilterName(course_id);
	var classname = "list-group-item caltech-course"
	var datacourseid = String(course_id);

	var headingclass = "list-group-item-heading"
	var headingname = generateCourseShortName(course_id);

	var subtitleclass = "list-group-item-text"
	var subtitlename = getCourseFullName(course_id);

	var htmlcode = 
		sprintf('<a href="#" class="%s" data-course-name="%s" data-course-id="%s"><h4 class="%s">%s</h4><p class="%s">%s</p></a>',
			classname, filtername, datacourseid, headingclass, headingname, subtitleclass, subtitlename);


	return htmlcode;
}


function appendCaltechCourse (course_id) {
	$("#course-filter-list").append(getFilterButtonHTML(course_id));
}

function initializeFilterButtonClick () {
		$("#course-filter-list").on('click', 'a.caltech-course', 
			function () {
				console.log( "You wanted to add course with id " + $(this).attr("data-course-id"));
				addCourse(Number($(this).attr("data-course-id")));
			});
}


function populateCourses () {
	for (var i = MasterCourseList.length - 1; i >= 0; i--) {
		appendCaltechCourse(i);
	};
}

function getEventArray (course_id) {
	// returns a list of array objects generated from course_id 

	var eventList = [];
	var temp = [];

	for (var i = getCourseMultiplicity(course_id) - 1; i >= 0; i--) {
		temp = generateIsotimeEvents(course_id, getCourseDaysAt(course_id, i), getCourseTimesAt(course_id, i));

		for (var j = temp.length - 1; j >= 0; j--) {
			eventList.push(temp[j]);
		};
	};

	return eventList;
}

function addAtomicEvents (eventList) {
	activeCoursesAtomicEvents.push.apply(activeCoursesAtomicEvents, eventList);
}


function calendarRefresh () {
	activeCourseEventObject.events = activeCoursesAtomicEvents;

	$("#calendar").fullCalendar('refetchEvents');
}

function addCourse (course_id) {
	addAtomicEvents(getEventArray(course_id));
	calendarRefresh();
}


$(document).ready(
	function()
	{
		// populate courses
		populateCourses();

		// set up click events for filter buttons
		initializeFilterButtonClick();

		// hide initially, and set up
		// the filter box functionality
		// TODO: ordering based on string_score	
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



		// initialize the calendar
		$('#calendar').fullCalendar({
			weekends: false,
			defaultView: 'agendaWeek',
			header: {
				left: false,
				center: false,
				right: false
			},
			allDaySlot: false,
			minTime: 8,
			maxTime: 22,
			columnFormat: {
				week: 'dddd'
			},
			height: 500,

		})

		$("#calendar").fullCalendar('addEventSource', activeCourseEventObject);


	});



// need to the functions
// master_courses = list of classes
// addID(id) -- function;
// active_courses = list of id's
// generate_event_from_id(id) -- generate a FC event corresponding to the course id.