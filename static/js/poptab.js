/* * * * * * * * * * * * * * 
 * popTab.js
 * ---------
 * By Chris Neveu
 * Last Edited 2013-08-13
 */

var popTab = function(el)
{
	var tabOpen = false,
		doc = document.documentElement;

	var trim = function(str)
	{
		return str.trim ? str.trim() : str.replace(/^\s+|\s+$/g,'');
	};
	var hasClass = function(el, cn)
	{
		return (' ' + el.className + ' ').indexOf(' ' + cn + ' ') !== -1;
	};
	var addClass = function(el, cn)
	{
		if (!hasClass(el, cn))
		{
			el.className = (el.className === '') ? cn : el.className + ' ' + cn;
		}
	};
	var removeClass = function(el, cn)
	{
		el.className = trim((' ' + el.className + ' ').replace(' ' + cn + ' ', ' '));
	};
	var toggleTab = function(e)
	{
		if(tabOpen)
		{
			removeClass(this.parentNode, "open");
		}
		else
		{
			addClass(this.parentNode, "open");
		}
		if (e) {
			e.preventDefault();
		}
		tabOpen = !tabOpen;
	};

	addClass(doc, 'js-ready');
	removeClass(doc, 'no-js');
	if(document.getElementById(el))
	{
		document.getElementById(el).firstElementChild.addEventListener('click', toggleTab, false);
	}
}

var initJS = function()
{
	popTab('login_form');
	popTab('register_form');
}


window.addEventListener('DOMContentLoaded', initJS, false);