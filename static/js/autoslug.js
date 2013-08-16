var autoSlug = function(titleEl, slugEl)
{
	var title = document.getElementById(titleEl)
		slug = document.getElementById(slugEl),
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
	var sanitizeURL = function(url)
	{
		return url.toLowerCase().replace(/\s+/g,'-').replace(/[^abcdefghijklmnopqrstuvwxyz0123456789\-._~:\/#[\]@!$&'()*+,;=]/g,'');
	}
	var updateSlug = function(e)
	{
		slug.value = sanitizeURL(title.value);
	};

	addClass(doc, 'js-ready');
	removeClass(doc, 'no-js');
	if(title)
	{
		title.addEventListener('input', updateSlug, false);
	}
}

var initJS = function()
{
	autoSlug('title_field', 'slug_field');
}

window.addEventListener('DOMContentLoaded', initJS, false);