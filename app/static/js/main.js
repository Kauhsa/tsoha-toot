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
  login: function(arg$){
    var id, password, success, failure, obj, event;
    id = arg$.id, password = arg$.password, success = arg$.success, failure = arg$.failure;
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
      obj.set('loggedUser', id);
      return success();
    });
    return event.fail(function(){
      obj.set('loggedUser', null);
      return failure();
    });
  },
  logout: function(arg$){
    var success, failure, obj, event;
    success = arg$.success, failure = arg$.failure;
    obj = this;
    event = $.ajax({
      type: 'POST',
      url: '/logout'
    });
    event.done(function(){
      obj.set('loggedUser', null);
      return success();
    });
    return event.fail(function(){
      return failure();
    });
  }
});
App.AuthState = AuthState.create();
App.Router.map(function(){
  this.route("index", {
    path: "/"
  });
  return this.route("register", {
    path: '/register'
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
  currentlyLoggingIn: false,
  login: function(){
    var ctrl;
    ctrl = this;
    this.set('currentlyLoggingIn', true);
    return App.AuthState.login({
      id: this.get('loginId'),
      password: this.get('loginPassword'),
      success: function(){
        return ctrl.set('currentlyLoggingIn', false);
      },
      failure: function(){
        return ctrl.set('currentlyLoggingIn', false);
      }
    });
  },
  logout: function(){
    return App.AuthState.logout({
      success: function(){},
      failure: function(){}
    });
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
      $(view.get('contentElement')).show();
      return setTimeout(function(){
        return this.$('input:first').focus();
      }, 100);
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