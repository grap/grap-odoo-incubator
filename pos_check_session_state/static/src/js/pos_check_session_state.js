/*
Copyright (C) 2015-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

openerp.pos_check_session_state = function (instance) {
    var module = instance.point_of_sale;

    /* 
        Define : New ErrorClosedSessionPopupWidget Widget.
        This pop up will be shown if the current pos.session of the PoS is not
        in an 'open' state;
        The check will be done depending on a parameter on the PoS config
    */  
    module.ErrorClosedSessionPopupWidget = module.ErrorPopupWidget.extend({
        template:'ErrorClosedSessionPopupWidget',

        session_name: '',

        init: function(parent, options) {
            var self = this;
            this._super(parent, options);

            self.intervalID = setInterval(function() {
                self.pos.fetch('pos.session', ['name','state'], [['id', '=', self.pos.pos_session.id]]) 
                .then(function(sessions){
                    if (sessions[0]['state'] != 'opened') {
                        // warn user if current session is not opened
                        self.session_name = sessions[0]['name'];
                        self.renderElement();
                        self.pos_widget.screen_selector.show_popup('error-closed-session');
                    }
                })
                .fail(function(error, event){
                    // Prevent error if server is unreachable
                    event.preventDefault();
                });
            }, self.pos.config.check_session_state_frequency * 1000);
        },
    });

    /* 
        Overload : PosWidget to include ErrorClosedSessionPopupWidget inside.
    */
    module.PosWidget = module.PosWidget.extend({
        build_widgets: function(){
            this._super();
            // Add a new Popup 'ErrorClosedSessionPopupWidget'
            this.error_closed_session_popup = new module.ErrorClosedSessionPopupWidget(this, {});
            this.error_closed_session_popup.appendTo(this.$el);
            this.screen_selector.popup_set['error-closed-session'] = this.error_closed_session_popup;

            // Hide the popup because all pop up are displayed at the
            // beginning by default
            this.error_closed_session_popup.hide();
        },
    });

};
