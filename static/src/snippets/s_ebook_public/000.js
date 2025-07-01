odoo.define('ebook_public.snippet', function(require) {
	'use strict';
	var PublicWidget = require('web.public.widget');
	var core = require('web.core');
	var qweb = core.qweb;

	var eBookPublic = PublicWidget.Widget.extend({
    	selector: '.s_ebook_public',
		events: {
			'click div.ebook_filter__tag': '_setTag',
		},
		init: function() {
			this._super.apply(this, arguments);
			this.data = [];
			this.tags = [];
			this.selectedTags = [];
		},
    	willStart: async function() {
			let dataTag = this.$el.find('.s_ebook_main');
			let tags = dataTag[0].dataset.categories ? dataTag[0].dataset.categories : "";
			return new Promise((resolve, reject) => $.ajax({
                url: `/ebook/public?tags=${tags}`,
                success: (data) => { 
					this.data = JSON.parse(data);
					resolve(this.data)
				},
                error: () => {},
            }));
    	},
    	start: function() {
			let tags = [];
			this.data.map((c) => {
				tags.push(...c.tags.map((t) => t[1]))
			})
			this.tags = [...new Set(tags)];
			this._renderContent(this.data);
			this._renderTags();
    	},
		_setTag(ev) {
			let tag = ev.target.id;
			if (this.selectedTags.includes(tag)) {
				const index = this.selectedTags.indexOf(tag);
				this.selectedTags.splice(index, 1);
			} else {
				this.selectedTags.push(tag);
			}
			let filtredData = this.data.filter((e) => this._compareTags(e));
			this._renderContent(this.selectedTags.length > 0 ? filtredData : this.data);
			this._renderTags();
		},
		_renderContent(data) {
			let output = data.map((c) => {
				return qweb.render('ebook.s_ebook_public.item', {"item": c})
			})
        	this.$el.find('#ebook-content').html(output);
		},
		_renderTags() {
			let tag_output = this.tags.map((c) => {
				return qweb.render('ebook.s_ebook_public.tag', {
					"tag": c,
					"active": this.selectedTags.includes(c)
				})
			})
			this.$el.find('#ebook-tags').html(tag_output);
		},
		_compareTags(el){
			var value = 0;
			this.selectedTags.forEach(function(tag){
				value = value + el.tags.map(t => t[1]).includes(tag);
			});
			return (value === this.selectedTags.length)
		}
	});

	PublicWidget.registry.s_ebook_public = eBookPublic;
	return eBookPublic;
});
