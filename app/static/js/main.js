var AuthState;
window.App = Ember.Application.create();
AuthState = Ember.Object.extend({
  loggedUser: null,
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
    event.fail(function(){
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
  foo: 'bar'
});