/**************************************************************/
/* Prepares the cv to be dynamically expandable/collapsible   */
/**************************************************************/
function prepareList() {
    $('#expList').find('li:has(ul)')
    .click( function(event) {
        if (this == event.target) {
	    if (this.className == 'collapsed') {
	      $('.collapsed').removeClass('expanded');
	      $('.collapsed').children().hide('medium');
	      $(this).toggleClass('expanded');
	      $(this).children('ul').toggle('medium');
	    }else if (this.className == 'collapsed expanded'){
	      $(this).toggleClass('expanded');
	      $(this).children('ul').toggle('medium');
	    }
	  
	}
        return false;
    })
    .addClass('collapsed')
    .children('ul').hide();

    //Create the button funtionality
    $('#expandList')
    .unbind('click')
    .click( function() {
        $('.collapsed').addClass('expanded');
        $('.collapsed').children().show('medium');
    })
    $('#collapseList')
    .unbind('click')
    .click( function() {
        $('.collapsed').removeClass('expanded');
        $('.collapsed').children().hide('medium');
    })
    
};


/**************************************************************/
/* Functions to execute on loading the document               */
/**************************************************************/
$(document).ready( function() {
    prepareList()
});