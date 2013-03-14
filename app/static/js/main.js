var AuthState;
window.App = Ember.Application.create();
AuthState = Ember.Object.extend({
  loggedUser: null,
  init: function(){
    var obj, event;
    obj = this;
    event = $.ajax({
      type: 'GET',
      url: '/logged_user'
    });
    return event.done(function(data){
      if ('logged_user' in data) {
        return obj.set('loggedUser', data['logged_user']);
      } else {
        return obj.set('loggedUser', null);
      }
    });
  },
  login: function(id, password){
    var obj, event;
    obj = this;
    event = $.ajax({
      type: 'POST',
      url: '/login',
      data: {
        id: id,
        password: password
      }
    });
    event.done(function(){
      return obj.set('loggedUser', id);
    });
    return event.fail(function(){
      return obj.set('loggedUser', null);
    });
  },
  logout: function(){
    var obj, event;
    obj = this;
    event = $.ajax({
      type: 'POST',
      url: '/logout'
    });
    return event.done(function(){
      return obj.set('loggedUser', null);
    });
  }
});
App.AuthState = AuthState.create();
App.Router.map(function(){
  return this.route("index", {
    path: "/"
  });
});
App.IndexRoute = Ember.Route.extend({
  renderTemplate: function(){
    return this.render('navbar', {
      controller: 'navbar',
      outlet: 'navbar'
    });
  }
});
App.NavbarController = Ember.Controller.extend({
  loginId: null,
  loginPassword: null,
  login: function(){
    return App.AuthState.login(this.get('loginId'), this.get('loginPassword'));
  },
  logout: function(){
    return App.AuthState.logout();
  }
});
App.Popover = Ember.View.extend({
  tagName: 'a',
  template: Ember.Handlebars.compile('{{ view.label }}'),
  attributeBindings: ['href'],
  href: '#',
  label: 'Popover',
  placement: 'bottom',
  contentElement: '',
  didInsertElement: function(){
    var view;
    view = this;
    $(this.get('contentElement')).hide();
    this.$().click(function(){
      return $(view.get('contentElement')).show();
    });
    return this.$().popover({
      content: $(this.get('contentElement')),
      placement: this.get('placement'),
      html: true
    });
  }
});
App.Dropdown = Ember.View.extend({
  tagName: 'a',
  classNames: ['dropdown-toggle'],
  attributeBindings: ['href', 'id'],
  id: '',
  href: '#',
  didInsertElement: function(){
    return this.$().dropdown();
  }
});